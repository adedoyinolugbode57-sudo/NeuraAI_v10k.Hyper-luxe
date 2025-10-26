#!/usr/bin/env python3
"""
worker.py — NeuraAI Heavy Worker Microservice

Responsibilities:
- Pull jobs from Redis list "neura:jobs" (BRPOP)
- Job types: inference, tts, analytics, image (optional)
- Uses OpenAI (if OPENAI_API_KEY set) or local transformers fallback
- Uses VOICE_SERVICE_URL (microservice) or local TTS fallback (gTTS/pyttsx3)
- Stores results in Redis hash "neura:results:<job_id>" and optionally POSTs to CALLBACK_URL
- Exponential backoff retries and max_retries support
- Graceful shutdown & health logging

Run:
  python worker.py

Environment variables (see .env.example):
  REDIS_URL, OPENAI_API_KEY, VOICE_SERVICE_URL, CALLBACK_URL, WORKER_CONCURRENCY, MAX_RETRIES
"""

import os
import sys
import json
import time
import uuid
import signal
import logging
import traceback
import threading
from typing import Any, Dict, Optional

import requests
import redis

# Optional OpenAI / transformers imports
try:
    import openai
except Exception:
    openai = None

try:
    from transformers import pipeline
    transformers_available = True
except Exception:
    transformers_available = False

# Logging
LOG_FILE = os.getenv("NEURA_WORKER_LOG", "worker.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(LOG_FILE)]
)
logger = logging.getLogger("neura_worker")

# Config from env
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
VOICE_SERVICE_URL = os.getenv("VOICE_SERVICE_URL", "")
CALLBACK_URL = os.getenv("CALLBACK_URL", "")  # optional: where to POST job results
WORKER_CONCURRENCY = int(os.getenv("WORKER_CONCURRENCY", "1"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "5"))
JOB_QUEUE = os.getenv("JOB_QUEUE", "neura:jobs")
RESULT_TTL = int(os.getenv("RESULT_TTL_SECONDS", str(60 * 60 * 24)))  # 24 hours by default
JOB_BLOCK_TIMEOUT = int(os.getenv("JOB_BLOCK_TIMEOUT", "30"))  # BRPOP timeout seconds
INFERENCE_TIMEOUT = int(os.getenv("INFERENCE_TIMEOUT", "60"))  # seconds

# Redis client
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# OpenAI init
if OPENAI_API_KEY and openai:
    try:
        openai.api_key = OPENAI_API_KEY
        logger.info("OpenAI configured for worker.")
    except Exception:
        logger.exception("Failed to set OpenAI API key.")
else:
    if not openai:
        logger.info("openai package not available; worker will fallback to local models or microservices.")
    else:
        logger.info("OPENAI_API_KEY not configured.")

shutdown_event = threading.Event()

def graceful_shutdown(signum, frame):
    logger.info("Received shutdown signal (%s). Stopping worker...", signum)
    shutdown_event.set()

signal.signal(signal.SIGTERM, graceful_shutdown)
signal.signal(signal.SIGINT, graceful_shutdown)

# ---------------------------
# Job processing helpers
# ---------------------------

def store_result(job_id: str, result: Dict[str, Any], ttl: int = RESULT_TTL):
    key = f"neura:results:{job_id}"
    try:
        redis_client.hset(key, mapping={"result": json.dumps(result, ensure_ascii=False), "ts": time.time()})
        redis_client.expire(key, ttl)
        logger.debug("Stored result for job %s", job_id)
    except Exception:
        logger.exception("Failed to store result in Redis for job %s", job_id)

def callback_result(job_id: str, result: Dict[str, Any]):
    if not CALLBACK_URL:
        return
    try:
        cb = CALLBACK_URL.rstrip("/") + "/worker/callback"
        payload = {"job_id": job_id, "result": result}
        r = requests.post(cb, json=payload, timeout=10)
        logger.info("Callback to %s status=%s", cb, getattr(r, "status_code", "err"))
    except Exception:
        logger.exception("Callback failed for job %s", job_id)

def safe_parse_job(raw: str) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(raw)
    except Exception:
        logger.exception("Malformed job JSON: %s", raw[:200])
        return None

# ---------------------------
# Inference implementations
# ---------------------------
def inference_openai(prompt: str, model: str = "gpt-4o", max_tokens: int = 300, temperature: float = 0.6) -> Dict[str, Any]:
    if not openai:
        return {"ok": False, "error": "openai_not_installed"}
    try:
        resp = None
        # attempt modern interface; many SDK versions differ — be defensive
        try:
            resp = openai.chat.completions.create(
                model=model,
                messages=[{"role":"system","content":"You are NeuraAI worker."},{"role":"user","content":prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
            )
        except Exception:
            try:
                resp = openai.ChatCompletion.create(model=model, messages=[{"role":"user","content":prompt}], max_tokens=max_tokens)
            except Exception as e:
                logger.exception("OpenAI call failed: %s", e)
                raise

        # parse
        text = None
        if resp:
            try:
                choices = getattr(resp, "choices", None) or resp.get("choices")
                if choices:
                    first = choices[0]
                    message = getattr(first, "message", None) or first.get("message")
                    if message:
                        text = getattr(message, "content", None) or message.get("content")
                    else:
                        text = getattr(first, "text", None) or first.get("text")
            except Exception:
                logger.exception("Failed parsing OpenAI response")
        if not text and isinstance(resp, dict):
            try:
                text = resp["choices"][0]["message"]["content"]
            except Exception:
                text = None
        if not text:
            return {"ok": False, "error": "no_text", "raw": str(resp)[:400]}
        return {"ok": True, "reply": text}
    except Exception as e:
        logger.exception("OpenAI inference error: %s", e)
        return {"ok": False, "error": str(e)}

_local_pipeline = None
def init_local_model(local_model_name: str = "gpt2"):
    global _local_pipeline
    if transformers_available:
        try:
            _local_pipeline = pipeline("text-generation", model=local_model_name, device=-1)
            logger.info("Local transformer pipeline initialized: %s", local_model_name)
        except Exception:
            logger.exception("Failed to initialize local transformer pipeline")
            _local_pipeline = None
    else:
        _local_pipeline = None

def inference_local(prompt: str, max_tokens: int = 200, temperature: float = 0.7):
    if not _local_pipeline:
        return {"ok": False, "error": "no_local_model"}
    try:
        out = _local_pipeline(prompt, max_length=max_tokens, do_sample=True, temperature=temperature, num_return_sequences=1)
        if isinstance(out, list) and out:
            text = out[0].get("generated_text", "")
            # remove prompt repetition
            if text.startswith(prompt):
                text = text[len(prompt):].strip()
            return {"ok": True, "reply": text}
        return {"ok": False, "error": "no_output"}
    except Exception:
        logger.exception("Local inference failed")
        return {"ok": False, "error": "local_failed"}

# ---------------------------
# TTS implementations
# ---------------------------
def tts_via_microservice(text: str, language: str = "en", mood: str = "neutral") -> Dict[str, Any]:
    if not VOICE_SERVICE_URL:
        return {"ok": False, "error": "no_voice_service"}
    try:
        r = requests.post(VOICE_SERVICE_URL.rstrip("/") + "/speak", json={"text": text, "language": language, "mood": mood}, timeout=30)
        if r.ok:
            return {"ok": True, "audio": r.json().get("audio")}
        return {"ok": False, "error": f"service_status_{r.status_code}"}
    except Exception:
        logger.exception("Voice microservice call failed")
        return {"ok": False, "error": "voice_service_error"}

def tts_local_gtts(text: str, language: str = "en", out_path: Optional[str] = None):
    try:
        # use gTTS as a fallback (requires network)
        from gtts import gTTS
        if not out_path:
            out_path = f"static/audio/tts_{int(time.time())}_{uuid.uuid4().hex[:6]}.mp3"
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        tts = gTTS(text=text, lang=language)
        tts.save(out_path)
        return {"ok": True, "audio": out_path}
    except Exception:
        logger.exception("gTTS TTS failed")
        return {"ok": False, "error": "gtts_failed"}

# ---------------------------
# Job processing core
# ---------------------------
def process_job(job: Dict[str, Any]) -> Dict[str, Any]:
    job_id = job.get("job_id") or f"job_{int(time.time())}_{uuid.uuid4().hex[:8]}"
    jtype = job.get("type", "inference")
    payload = job.get("payload", {})
    attempt = int(job.get("attempt", 0))
    logger.info("Processing job %s type=%s attempt=%d", job_id, jtype, attempt)

    try:
        if jtype == "inference":
            prompt = payload.get("prompt", "")
            model = payload.get("model") or os.getenv("NEURA_MODEL") or "gpt-4o"
            max_tokens = int(payload.get("max_tokens", 300))
            temperature = float(payload.get("temperature", 0.6))
            # prefer microservice if present
            ai_service = os.getenv("AI_SERVICE_URL")
            if ai_service:
                try:
                    r = requests.post(ai_service.rstrip("/") + "/chat", json={"prompt": prompt, "max_tokens": max_tokens, "temperature": temperature}, timeout=INFERENCE_TIMEOUT)
                    if r.ok:
                        data = r.json()
                        reply = data.get("reply") or data.get("result") or data.get("text")
                        res = {"ok": True, "reply": reply}
                        logger.info("Microservice inference ok for job %s", job_id)
                        return res
                except Exception:
                    logger.exception("AI microservice call failed for job %s", job_id)
            # try OpenAI
            if OPENAI_API_KEY and openai:
                return inference_openai(prompt, model=model, max_tokens=max_tokens, temperature=temperature)
            # local fallback
            local_model = os.getenv("NEURA_LOCAL_MODEL", "gpt2")
            if transformers_available and _local_pipeline is None:
                init_local_model(local_model)
            return inference_local(prompt, max_tokens=max_tokens, temperature=temperature)

        elif jtype == "tts":
            text = payload.get("text", "")
            language = payload.get("language", "en")
            mood = payload.get("mood", "neutral")
            # prefer microservice
            if VOICE_SERVICE_URL:
                return tts_via_microservice(text, language, mood)
            return tts_local_gtts(text, language)

        elif jtype == "analytics":
            # example: payload contains {event_name, data}; we simply store in Redis list for analytics consumers
            event = payload.get("event", "custom")
            data = payload.get("data", {})
            try:
                redis_client.rpush("neura:analytics", json.dumps({"event": event, "data": data, "ts": time.time()}))
            except Exception:
                logger.exception("Failed to push analytics event")
            return {"ok": True, "message": "analytics_recorded"}

        elif jtype == "image":
            # proxy to IMAGE_SERVICE_URL if available
            txt = payload.get("prompt", "")
            if os.getenv("IMAGE_SERVICE_URL"):
                try:
                    r = requests.post(os.getenv("IMAGE_SERVICE_URL").rstrip("/") + "/generate", json={"prompt": txt}, timeout=60)
                    if r.ok:
                        return {"ok": True, "image": r.json().get("image")}
                except Exception:
                    logger.exception("Image microservice failed")
            return {"ok": False, "error": "no_image_service"}

        else:
            logger.warning("Unknown job type: %s", jtype)
            return {"ok": False, "error": "unknown_job_type"}

    except Exception as e:
        logger.exception("Unhandled exception processing job %s: %s", job_id, e)
        return {"ok": False, "error": str(e)}

# ---------------------------
# Worker loop (single thread worker function)
# ---------------------------
def worker_loop(worker_id: int = 0):
    logger.info("Worker[%d] started, listening on %s", worker_id, JOB_QUEUE)
    while not shutdown_event.is_set():
        try:
            # BRPOP returns (queue, jobstr) or None when timed out
            res = redis_client.brpop(JOB_QUEUE, timeout=JOB_BLOCK_TIMEOUT)
            if not res:
                continue
            _, job_raw = res
            job = safe_parse_job(job_raw)
            if not job:
                continue
            job_id = job.get("job_id") or f"job_{int(time.time())}_{uuid.uuid4().hex[:8]}"
            job.setdefault("job_id", job_id)
            job.setdefault("attempt", 0)

            result = process_job(job)
            # on failure and retry allowed
            if not result.get("ok") and job.get("attempt", 0) < MAX_RETRIES:
                job["attempt"] = job.get("attempt", 0) + 1
                backoff = min(60, 2 ** job["attempt"])
                logger.info("Job %s failed, scheduling retry #%d after %ds", job_id, job["attempt"], backoff)
                # schedule by pushing to a retry queue with delay (simple sleep then push in a separate thread)
                def schedule_retry(j, delay):
                    time.sleep(delay)
                    try:
                        redis_client.lpush(JOB_QUEUE, json.dumps(j, ensure_ascii=False))
                        logger.info("Retry requeued for job %s", j.get("job_id"))
                    except Exception:
                        logger.exception("Failed to requeue job %s", j.get("job_id"))
                threading.Thread(target=schedule_retry, args=(job, backoff), daemon=True).start()
                # store partial failure result
                store_result(job_id, {"ok": False, "error": result.get("error", "failed"), "attempt": job["attempt"]})
                callback_result(job_id, {"ok": False, "error": result.get("error", "failed"), "attempt": job["attempt"]})
                continue

            # store success/final result
            store_result(job_id, result)
            callback_result(job_id, result)
            logger.info("Job %s completed. ok=%s", job_id, result.get("ok"))

        except Exception:
            logger.exception("Top-level worker loop error")
            time.sleep(1)

    logger.info("Worker[%d] graceful exit.", worker_id)

# ---------------------------
# Main: spawn concurrency workers
# ---------------------------
def main():
    logger.info("Starting NeuraAI Worker Service (concurrency=%d)", WORKER_CONCURRENCY)
    # initialize local model if requested
    if transformers_available and os.getenv("NEURA_LOCAL_MODEL"):
        try:
            init_local_model(os.getenv("NEURA_LOCAL_MODEL"))
        except Exception:
            logger.exception("Local model init failed at startup")

    threads = []
    for i in range(WORKER_CONCURRENCY):
        t = threading.Thread(target=worker_loop, args=(i,), daemon=True)
        threads.append(t)
        t.start()

    try:
        # main thread simply waits until shutdown
        while not shutdown_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        shutdown_event.set()
    # join
    for t in threads:
        t.join(timeout=2)
    logger.info("All worker threads stopped. Exiting.")

if __name__ == "__main__":
    main()