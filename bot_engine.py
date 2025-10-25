"""
bot_engine.py — NeuraAI_v10k.Hyperluxe Bot Engine

Purpose:
- Provides a single entrypoint for generating AI responses (OpenAI or local fallback).
- Manages conversation memory, caching, rate-limiting, logging, metrics.
- Provides TTS hooks and streaming interfaces for real-time UIs.
- Designed for modular use by `main.py` or as a microservice.

Author: ChatGPT + Joshua Dav
License: MIT-style permissive

Usage:
    from bot_engine import BotEngine
    engine = BotEngine()
    reply = engine.generate("Hello", user_id="user123")
"""

import os
import time
import json
import math
import uuid
import queue
import random
import logging
import inspect
import threading
from dataclasses import dataclass, field
from typing import Any, Dict, Callable, List, Optional, Tuple
from functools import lru_cache

# Optional packages are imported safely; when not installed, we fallback gracefully.
try:
    import openai
except Exception:
    openai = None

try:
    # Local small-model fallback using transformers (optional)
    from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
    transformers_available = True
except Exception:
    transformers_available = False

# Setup a logger for the engine
LOG_PATH = os.getenv("NEURA_BOT_LOG", "bot_engine.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler(LOG_PATH)]
)
logger = logging.getLogger("bot_engine")

# --------------------------
# Dataclasses / Types
# --------------------------
@dataclass
class BotConfig:
    model_name: str = os.getenv("NEURA_MODEL", "gpt-5-mini")
    default_max_tokens: int = 300
    default_temperature: float = 0.6
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    prefer_openai: bool = True  # try OpenAI first, fallback to local
    local_model_name: str = os.getenv("NEURA_LOCAL_MODEL", "gpt2")  # lightweight fallback
    memory_size: int = 10  # per-user short-term memory
    rate_limit_per_minute: int = 120  # requests per minute (global)
    cache_ttl_seconds: int = 300  # default cache TTL for similar prompts
    max_concurrent_requests: int = 8  # concurrency guard
    enable_streaming: bool = True  # whether streaming responses are allowed
    admin_token: Optional[str] = os.getenv("NEURA_ADMIN_TOKEN")
    voice_tts_enabled: bool = os.getenv("ENABLE_TTS", "false").lower() in ("1","true","yes")
    voice_service_url: Optional[str] = os.getenv("VOICE_SERVICE_URL")
    # Add more flags as needed

@dataclass
class MemoryItem:
    role: str
    content: str
    ts: float = field(default_factory=time.time)

# --------------------------
# Simple in-memory components
# --------------------------
class SimpleLRUCache:
    """Small LRU cache with TTL per entry."""
    def __init__(self, maxsize: int = 256):
        self.maxsize = maxsize
        self.store: Dict[str, Tuple[float, Any]] = {}
        self.lock = threading.Lock()

    def _prune(self):
        if len(self.store) <= self.maxsize:
            return
        # remove oldest
        items = sorted(self.store.items(), key=lambda kv: kv[1][0])
        to_remove = len(self.store) - self.maxsize
        for k, _ in items[:to_remove]:
            del self.store[k]

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        expire_at = time.time() + (ttl if ttl else 3600)
        with self.lock:
            self.store[key] = (expire_at, value)
            self._prune()

    def get(self, key: str):
        with self.lock:
            item = self.store.get(key)
            if not item:
                return None
            expire_at, val = item
            if expire_at < time.time():
                del self.store[key]
                return None
            return val

    def clear(self):
        with self.lock:
            self.store.clear()

class RateLimiter:
    """Token-bucket global rate limiter (simple)."""
    def __init__(self, rate_per_minute: int = 120):
        self.rate = rate_per_minute
        self.capacity = rate_per_minute
        self._tokens = rate_per_minute
        self._last_check = time.time()
        self.lock = threading.Lock()

    def allow(self, cost: int = 1) -> bool:
        with self.lock:
            now = time.time()
            elapsed = now - self._last_check
            self._last_check = now
            # refill tokens
            refill = (elapsed / 60.0) * self.rate
            self._tokens = min(self.capacity, self._tokens + refill)
            if self._tokens >= cost:
                self._tokens -= cost
                return True
            return False

# --------------------------
# BotEngine
# --------------------------
class BotEngine:
    """
    Main class to generate responses. Designed to be instantiated once and reused.
    """

    def __init__(self, config: BotConfig = None):
        self.config = config or BotConfig()
        self.memory: Dict[str, List[MemoryItem]] = {}  # per-user memory
        self.cache = SimpleLRUCache(maxsize=1024)
        self.rate_limiter = RateLimiter(rate_per_minute=self.config.rate_limit_per_minute)
        self.concurrent_semaphore = threading.BoundedSemaphore(self.config.max_concurrent_requests)
        self.metrics = {
            "requests_total": 0,
            "requests_success": 0,
            "requests_failed": 0,
            "avg_latency": 0.0
        }
        self._init_openai()
        self._init_local_model()
        logger.info("BotEngine initialized: prefer_openai=%s, local_model=%s",
                    self.config.prefer_openai, self.config.local_model_name)

    # ----------------------
    # Initialization helpers
    # ----------------------
    def _init_openai(self):
        if self.config.openai_api_key and openai:
            try:
                openai.api_key = self.config.openai_api_key
                # Optionally configure client (proxy, organization)
                logger.info("OpenAI configured (key present).")
            except Exception as e:
                logger.exception("Failed to initialize OpenAI: %s", e)
        else:
            if not openai:
                logger.info("OpenAI python package not installed; skipping OpenAI setup.")
            else:
                logger.info("OPENAI_API_KEY not set; skipping OpenAI setup.")

    def _init_local_model(self):
        if transformers_available:
            try:
                # It's intentionally light: only create a pipeline for text-generation if needed
                # Loading large models may consume lots of memory; choose small model by default.
                self.local_pipeline = pipeline("text-generation", model=self.config.local_model_name, device=-1)
                logger.info("Local transformers pipeline initialized with model '%s'.", self.config.local_model_name)
            except Exception as e:
                logger.exception("Failed to init local transformers pipeline: %s", e)
                self.local_pipeline = None
        else:
            self.local_pipeline = None
            logger.info("transformers not available, local fallback will be text templates.")

    # ----------------------
    # Memory management
    # ----------------------
    def remember(self, user_id: str, role: str, content: str):
        """Add a memory item for a given user. Role is 'user' or 'assistant'."""
        mem_list = self.memory.setdefault(user_id, [])
        mem_list.append(MemoryItem(role=role, content=content, ts=time.time()))
        # enforce memory size
        if len(mem_list) > self.config.memory_size * 2:
            # keep last memory_size items (approx half user half assistant)
            self.memory[user_id] = mem_list[-(self.config.memory_size * 2):]

    def recall(self, user_id: str) -> List[MemoryItem]:
        """Return short term memory for the user."""
        return list(self.memory.get(user_id, []))

    def clear_memory(self, user_id: Optional[str] = None):
        if user_id:
            self.memory.pop(user_id, None)
        else:
            self.memory.clear()

    # ----------------------
    # Prompt utilities
    # ----------------------
    def _build_messages(self, prompt: str, user_id: Optional[str], system_instructions: Optional[str] = None,
                        extra_context: Optional[List[Dict[str, str]]] = None) -> List[Dict[str, str]]:
        """
        Compose message sequence for chat-style models.
        - system_instructions: high-level direction for the assistant
        - memory: per-user memory items appended as "assistant"/"user" messages
        - extra_context: list of dicts with role/content to append before the user's prompt
        """
        messages = []
        if system_instructions:
            messages.append({"role": "system", "content": system_instructions})
        # include memory in a summarized form
        if user_id:
            mem = self.recall(user_id)
            # include last N memory items (up to memory_size)
            for m in mem[-self.config.memory_size:]:
                messages.append({"role": m.role, "content": m.content})
        # extra context
        if extra_context:
            messages.extend(extra_context)
        # finally the user's prompt
        messages.append({"role": "user", "content": prompt})
        return messages

    def _normalize_prompt(self, prompt: str) -> str:
        # Basic normalization: trim, remove excessive whitespace
        return " ".join(prompt.strip().split())

    # ----------------------
    # Caching & dedupe
    # ----------------------
    def _cache_key(self, prompt: str, user_id: Optional[str], temperature: float, max_tokens: int) -> str:
        key = f"{user_id or 'anon'}|t={temperature}|m={max_tokens}|{hash(prompt)}"
        return key

    def _get_cached(self, key: str):
        return self.cache.get(key)

    def _set_cached(self, key: str, value: Any, ttl: Optional[int] = None):
        self.cache.set(key, value, ttl or self.config.cache_ttl_seconds)

    # ----------------------
    # Rate limiting & concurrency
    # ----------------------
    def _check_rate_limit(self) -> bool:
        allowed = self.rate_limiter.allow(1)
        if not allowed:
            logger.warning("Rate limiter blocked a request.")
        return allowed

    # ----------------------
    # OpenAI wrapper
    # ----------------------
    def _openai_chat(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float) -> Dict[str, Any]:
        """
        Use modern openai.chat.completions when available; gracefully handle SDK differences.
        Returns dict with keys: ok, reply, raw
        """
        if not openai or not self.config.openai_api_key:
            return {"ok": False, "error": "openai_not_configured"}
        try:
            # Different OpenAI SDK versions have different interfaces. Try the newest pattern first.
            # This does not send user API key in code; openai was already configured on init.
            logger.debug("Calling OpenAI chat with model %s", self.config.model_name)
            # Some versions: openai.chat.completions.create(...)
            # Some versions: openai.ChatCompletion.create(...)
            # We'll attempt both in a defensive manner.
            resp = None
            try:
                # preferred modern call
                resp = openai.chat.completions.create(
                    model=self.config.model_name,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
            except Exception:
                # fallback older naming
                try:
                    resp = openai.ChatCompletion.create(
                        model=self.config.model_name,
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature
                    )
                except Exception as e:
                    logger.exception("OpenAI chat call failed (both modern and legacy attempts): %s", e)
                    raise

            # parse response robustly
            if not resp:
                return {"ok": False, "error": "empty_response"}

            # Many returned objects are dict-like or an object with attributes.
            # Try to extract text safely.
            content = None
            try:
                choices = getattr(resp, "choices", None) or resp.get("choices")
                if choices:
                    first = choices[0]
                    # support object.attribute style
                    message_obj = getattr(first, "message", None) or first.get("message")
                    if message_obj:
                        content = getattr(message_obj, "content", None) or message_obj.get("content")
                    else:
                        # older models
                        content = getattr(first, "text", None) or first.get("text")
            except Exception:
                logger.exception("Failed to parse OpenAI response structure.")

            if not content and isinstance(resp, dict):
                # try navigate dictionary
                try:
                    content = resp["choices"][0]["message"]["content"]
                except Exception:
                    try:
                        content = resp["choices"][0]["text"]
                    except Exception:
                        content = None

            if not content:
                return {"ok": False, "error": "no_content_in_response", "raw": resp}

            return {"ok": True, "reply": content, "raw": resp}
        except Exception as e:
            logger.exception("OpenAI error: %s", e)
            return {"ok": False, "error": str(e)}

    # ----------------------
    # Local transformer fallback call
    # ----------------------
    def _local_generate(self, prompt: str, max_tokens: int, temperature: float) -> Dict[str, Any]:
        if self.local_pipeline:
            try:
                # transformers pipeline returns list of dicts with 'generated_text'
                logger.debug("Calling local pipeline for prompt length %d", len(prompt))
                out = self.local_pipeline(prompt, max_length=max_tokens, do_sample=True, temperature=temperature, num_return_sequences=1)
                if out and isinstance(out, list):
                    text = out[0].get("generated_text", "")
                    # cut off original prompt if model echoes it
                    if text.startswith(prompt):
                        text = text[len(prompt):].strip()
                    return {"ok": True, "reply": text, "raw": out}
                return {"ok": False, "error": "no_output"}
            except Exception as e:
                logger.exception("Local generation failed: %s", e)
                return {"ok": False, "error": str(e)}
        # very small fallback: template-based response
        return {"ok": True, "reply": f"I don't have OpenAI here — but I heard: {prompt[:200]}"}

    # ----------------------
    # Public generate method (sync)
    # ----------------------
    def generate(self, prompt: str, user_id: Optional[str] = None, *,
                 max_tokens: Optional[int] = None, temperature: Optional[float] = None,
                 system_instructions: Optional[str] = None, extra_context: Optional[List[Dict[str, str]]] = None,
                 use_cache: bool = True, prefer: str = "auto") -> Dict[str, Any]:
        """
        Generate a reply to a prompt.
        Parameters:
          - prompt: user prompt text
          - user_id: id for per-user memory
          - max_tokens: override default
          - temperature: override default
          - system_instructions: extra system-level instruction
          - extra_context: prebuilt messages appended before prompt
          - use_cache: check + store in cache
          - prefer: "openai", "local", "microservice", "auto"
        Returns a dict: {ok, reply, meta}
        """
        prompt = self._normalize_prompt(prompt)
        max_tokens = max_tokens or self.config.default_max_tokens
        temperature = temperature if temperature is not None else self.config.default_temperature

        # Rate limit
        if not self._check_rate_limit():
            return {"ok": False, "error": "rate_limited"}

        cache_key = self._cache_key(prompt, user_id, temperature, max_tokens)
        if use_cache:
            cached = self._get_cached(cache_key)
            if cached:
                logger.debug("Cache hit for key %s", cache_key)
                return {"ok": True, "reply": cached, "cached": True}

        # Acquire concurrency semaphore
        acquired = self.concurrent_semaphore.acquire(blocking=False)
        if not acquired:
            # gracefully reject if too many concurrent
            logger.warning("Max concurrency reached.")
            return {"ok": False, "error": "concurrency_limit"}

        start_ts = time.time()
        try:
            # build messages for chat-style APIs
            messages = self._build_messages(prompt, user_id, system_instructions, extra_context)

            # Decide which backend to call
            reply_result = None

            # Prefer: microservice -> openai -> local
            # Microservice hook: if environment variable AI_SERVICE_URL present, try it first.
            ai_service_url = os.getenv("AI_SERVICE_URL")  # dynamic lookup for microservice mode
            if ai_service_url and prefer in ("auto", "microservice"):
                try:
                    url = ai_service_url.rstrip("/") + "/chat"
                    payload = {"prompt": prompt, "user": user_id, "messages": messages, "max_tokens": max_tokens, "temperature": temperature}
                    logger.debug("Proxying prompt to AI microservice: %s", url)
                    r = requests.post(url, json=payload, timeout=30)
                    if r.ok:
                        data = r.json()
                        if data.get("ok") and data.get("reply"):
                            reply_result = {"ok": True, "reply": data.get("reply"), "raw": data}
                            logger.debug("Microservice responded OK")
                        else:
                            logger.debug("Microservice returned non-ok")
                    else:
                        logger.warning("Microservice responded status %s", r.status_code)
                except Exception:
                    logger.exception("AI microservice call failed, falling back.")

            # If reply_result still None, try OpenAI if configured and either preferred or auto
            if not reply_result and (prefer in ("auto", "openai") or (self.config.prefer_openai and prefer != "local")):
                reply_result = self._openai_chat(messages, max_tokens, temperature)
                if reply_result and not reply_result.get("ok"):
                    logger.debug("OpenAI attempt failed: %s", reply_result.get("error"))

            # If still not ok, try local generator
            if not reply_result or not reply_result.get("ok"):
                reply_result = self._local_generate(prompt, max_tokens, temperature)

            # Final safety: ensure reply exists
            if not reply_result or not reply_result.get("ok"):
                # fallback text
                reply_text = f"Sorry — I'm having trouble generating a response right now."
                reply_result = {"ok": False, "error": "generation_failed", "reply": reply_text}
                logger.error("Generation failed, returning fallback text.")

            # Normalize reply
            reply_text = reply_result.get("reply", "")
            # store memory
            if user_id:
                try:
                    self.remember(user_id, "user", prompt)
                    self.remember(user_id, "assistant", reply_text)
                except Exception:
                    logger.debug("Memory store failed (non-fatal).")

            # cache reply
            if use_cache and reply_text:
                try:
                    self._set_cached(cache_key, reply_text)
                except Exception:
                    logger.debug("Cache set failed.")

            # metrics
            latency = time.time() - start_ts
            self.metrics["requests_total"] += 1
            if reply_result.get("ok"):
                self.metrics["requests_success"] += 1
            else:
                self.metrics["requests_failed"] += 1
            # update rolling average
            prev_avg = self.metrics["avg_latency"]
            n = self.metrics["requests_total"]
            self.metrics["avg_latency"] = ((prev_avg * (n-1)) + latency) / n if n > 0 else latency

            return {"ok": reply_result.get("ok", True), "reply": reply_text, "latency": latency, "meta": reply_result.get("raw", {})}
        finally:
            try:
                self.concurrent_semaphore.release()
            except Exception:
                pass

    # ----------------------
    # Streaming-like generator (yields chunks)
    # ----------------------
    def stream_generate(self, prompt: str, user_id: Optional[str] = None, *,
                        max_tokens: Optional[int] = None, temperature: Optional[float] = None,
                        system_instructions: Optional[str] = None, extra_context: Optional[List[Dict[str, str]]] = None):
        """
        Yields incremental chunks of the reply. This is a simulated streaming method if the underlying provider
        doesn't support streaming. If OpenAI streaming is available, you could wire into it here.
        Usage:
            for chunk in engine.stream_generate("Hello"):
                send_chunk_to_client(chunk)
        """
        # Use normal generate to get full reply, then yield slices to emulate streaming.
        res = self.generate(prompt, user_id, max_tokens=max_tokens, temperature=temperature,
                            system_instructions=system_instructions, extra_context=extra_context)
        if not res.get("ok"):
            yield {"ok": False, "error": res.get("error")}
            return
        full = res.get("reply", "")
        # yield header
        yield {"ok": True, "chunk": "", "status": "begin"}
        # heuristics: split into reasonable sized chunks
        chunk_size = 120
        for i in range(0, len(full), chunk_size):
            piece = full[i:i+chunk_size]
            time.sleep(0.02)  # tiny delay to simulate streaming
            yield {"ok": True, "chunk": piece, "status": "continue"}
        # done
        yield {"ok": True, "chunk": "", "status": "done"}

    # ----------------------
    # Bulk helpers
    # ----------------------
    def bulk_generate(self, prompts: List[Dict[str, Any]], user_id: Optional[str] = None, *,
                      concurrency: int = 4) -> List[Dict[str, Any]]:
        """
        Generate for many prompts concurrently. Prompts is a list of dicts with keys: prompt, max_tokens, temperature.
        Returns list of result dicts (same order).
        """
        results = [None] * len(prompts)
        q = queue.Queue()
        for idx, p in enumerate(prompts):
            q.put((idx, p))

        def worker():
            while not q.empty():
                try:
                    idx, item = q.get_nowait()
                except Exception:
                    break
                try:
                    prm = item.get("prompt")
                    mx = item.get("max_tokens")
                    temp = item.get("temperature")
                    r = self.generate(prm, user_id or item.get("user"), max_tokens=mx, temperature=temp)
                    results[idx] = r
                except Exception as e:
                    logger.exception("bulk generate exception: %s", e)
                    results[idx] = {"ok": False, "error": str(e)}
                finally:
                    q.task_done()

        threads = []
        for _ in range(min(concurrency, max(1, len(prompts)))):
            t = threading.Thread(target=worker, daemon=True)
            threads.append(t)
            t.start()
        q.join()
        for t in threads:
            t.join(timeout=0.1)
        return results

    # ----------------------
    # Admin / Debug helpers
    # ----------------------
    def stats(self) -> Dict[str, Any]:
        return {
            "metrics": self.metrics,
            "memory_users": len(self.memory),
            "cache_size": len(self.cache.store),
            "rate": {"tokens": self.rate_limiter._tokens, "capacity": self.rate_limiter.capacity},
            "concurrency_limit": self.config.max_concurrent_requests,
            "avg_latency": self.metrics.get("avg_latency")
        }

    def dump_memory(self, user_id: Optional[str] = None):
        if user_id:
            mem = self.memory.get(user_id, [])
            return [{"role": m.role, "content": m.content, "ts": m.ts} for m in mem]
        return {uid: [{"role": m.role, "content": m.content, "ts": m.ts} for m in mem] for uid, mem in self.memory.items()}

    def reset(self):
        self.memory.clear()
        self.cache.clear()
        self.metrics = {"requests_total": 0, "requests_success": 0, "requests_failed": 0, "avg_latency": 0.0}
        logger.info("BotEngine state reset by admin call.")

    # ----------------------
    # Voice integration helper
    # ----------------------
    def speak(self, text: str, lang: str = "en", mood: str = "cheerful") -> Optional[str]:
        """
        Generate speech audio and return URL or path.
        This method tries in order:
          1) VOICE_SERVICE_URL microservice (if env set)
          2) local ai_voice_assistant module (if imported)
        """
        # Microservice mode
        voice_service = os.getenv("VOICE_SERVICE_URL") or self.config.voice_service_url
        if voice_service:
            try:
                url = voice_service.rstrip("/") + "/speak"
                r = requests.post(url, json={"text": text, "language": lang, "mood": mood}, timeout=30)
                if r.ok:
                    data = r.json()
                    return data.get("audio")
            except Exception:
                logger.exception("Voice microservice call failed.")
        # try local module if available
        try:
            mod = safe_import("ai_voice_assistant")
            if mod and hasattr(mod, "speak_text"):
                return mod.speak_text(text, lang=lang, mood=mood)
        except Exception:
            logger.exception("Local voice assistant failed.")
        # no TTS available
        logger.warning("TTS not available (microservice/local).")
        return None

# --------------------------
# Helper safe_import at module-level for speak()
# --------------------------
def safe_import(name: str):
    try:
        return __import__(name)
    except Exception:
        return None

# --------------------------
# Simple CLI when run directly
# --------------------------
def _cli_main():
    import argparse
    parser = argparse.ArgumentParser(prog="bot_engine.py", description="NeuraAI Bot Engine CLI")
    parser.add_argument("--prompt", "-p", help="Prompt text to send to the engine", default=None)
    parser.add_argument("--user", "-u", help="User id", default="cli-user")
    parser.add_argument("--stream", "-s", action="store_true", help="Stream output chunks")
    parser.add_argument("--reset", action="store_true", help="Reset memory/cache then exit")
    args = parser.parse_args()

    engine = BotEngine()
    if args.reset:
        engine.reset()
        print("Engine state reset.")
        return
    if not args.prompt:
        print("Interactive mode. Type messages (CTRL+C to quit).")
        try:
            while True:
                text = input("You: ")
                if not text:
                    continue
                if args.stream:
                    for chunk in engine.stream_generate(text, args.user):
                        if chunk.get("status") == "continue":
                            print(chunk.get("chunk"), end="", flush=True)
                    print("\n--- done")
                else:
                    res = engine.generate(text, args.user)
                    print("NeuraAI:", res.get("reply"))
        except KeyboardInterrupt:
            print("\nbye")
            return
    else:
        if args.stream:
            for chunk in engine.stream_generate(args.prompt, args.user):
                if chunk.get("status") == "continue":
                    print(chunk.get("chunk"), end="", flush=True)
            print("\n--- done")
        else:
            out = engine.generate(args.prompt, args.user)
            print(out.get("reply"))

# --------------------------
# Exported singleton convenience
# --------------------------
_default_engine: Optional[BotEngine] = None

def get_default_engine() -> BotEngine:
    global _default_engine
    if _default_engine is None:
        _default_engine = BotEngine()
    return _default_engine

# --------------------------
# Minimal unit tests / smoke checks (do not run on import)
# --------------------------
def _self_test():
    e = BotEngine()
    print("Stats:", e.stats())
    r = e.generate("Hello there! What's up?", user_id="test-user")
    print("Reply:", r.get("reply"))
    s = list(e.stream_generate("Stream test, say hi in many words.", "stream-user"))
    print("Stream produced", len(s), "chunks.")

# --------------------------
# Allow running module directly
# --------------------------
if __name__ == "__main__":
    _cli_main()