"""
voice_assistant.py — NeuraAI_v10k Hyperluxe (Premium Voice Assistant)
- Wake word ("hey neura")
- Multilingual STT (speech_recognition)
- Async TTS (pyttsx3), optional ElevenLabs integration (comment)
- AI responses via ai_engine
- Local memory_store.json for short-term memory
- Analytics hooks
Created by ChatGPT + Joshua Dav
"""

import os
import json
import time
import threading
import queue
import traceback
from pathlib import Path
from typing import Optional, Dict, Any

# Third-party imports (optional on servers where audio isn't used)
try:
    import speech_recognition as sr
except Exception:
    sr = None

try:
    import pyttsx3
except Exception:
    pyttsx3 = None

# Integrations (existing modules in your project)
try:
    from config import PROJECT_ROOT
except Exception:
    PROJECT_ROOT = Path(__file__).parent

# ai_engine: expects the ai_engine module created earlier (ai_engine.ai_engine.chat)
try:
    from ai_engine import ai_engine
except Exception:
    ai_engine = None

# analytics (optional)
try:
    import analytics
except Exception:
    analytics = None

# Paths
VOICE_SETTINGS_PATH = Path(PROJECT_ROOT) / "voice_settings.json"
MEMORY_STORE_PATH = Path(PROJECT_ROOT) / "memory_store.json"
LOG_PATH = Path(PROJECT_ROOT) / "voice_assistant.log"

# Defaults
DEFAULT_WAKE_WORD = "hey neura"
DEFAULT_LANGUAGE = "en-US"
DEFAULT_TONE = "friendly"

# Ensure memory store exists
if not MEMORY_STORE_PATH.exists():
    MEMORY_STORE_PATH.write_text(json.dumps({"conversations": {}}, indent=2), encoding="utf-8")

# Ensure voice settings exist
if not VOICE_SETTINGS_PATH.exists():
    VOICE_SETTINGS_PATH.write_text(json.dumps({
        "gender": "female",
        "tone": DEFAULT_TONE,
        "language": "en-US",
        "rate": 170,
        "volume": 0.9,
        "wake_word": DEFAULT_WAKE_WORD,
        "enable_listen": True,
        "enable_tts": True,
        "use_elevenlabs": False,
        "elevenlabs_key": ""
    }, indent=2), encoding="utf-8")


# ---------------------------
# Utilities
# ---------------------------
def _log(msg: str):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")


def load_settings() -> Dict[str, Any]:
    try:
        return json.loads(VOICE_SETTINGS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_settings(settings: Dict[str, Any]):
    VOICE_SETTINGS_PATH.write_text(json.dumps(settings, indent=2), encoding="utf-8")


def load_memory():
    try:
        return json.loads(MEMORY_STORE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"conversations": {}}


def save_memory(mem: Dict[str, Any]):
    MEMORY_STORE_PATH.write_text(json.dumps(mem, indent=2), encoding="utf-8")


# ---------------------------
# TTS wrapper (pyttsx3 by default)
# Optional: ElevenLabs / other cloud TTS can be added
# ---------------------------
class TTS:
    def __init__(self):
        self.settings = load_settings()
        self.lock = threading.Lock()
        self.engine = None
        if pyttsx3:
            try:
                self.engine = pyttsx3.init()
                self._apply()
            except Exception as e:
                _log(f"TTS init error: {e}")
                self.engine = None

    def _apply(self):
        if not self.engine:
            return
        s = load_settings()
        try:
            self.engine.setProperty("rate", int(s.get("rate", 170)))
            self.engine.setProperty("volume", float(s.get("volume", 0.9)))
            # voice selection: try to pick male/female heuristically
            voices = self.engine.getProperty("voices")
            gender = s.get("gender", "female").lower()
            if gender == "male" and len(voices) > 1:
                self.engine.setProperty("voice", voices[1].id)
            else:
                self.engine.setProperty("voice", voices[0].id)
        except Exception as e:
            _log(f"TTS apply settings error: {e}")

    def speak(self, text: str):
        if not load_settings().get("enable_tts", True):
            _log("TTS disabled in settings.")
            return
        if self.engine:
            def _play():
                try:
                    with self.lock:
                        self._apply()
                        self.engine.say(text)
                        self.engine.runAndWait()
                except Exception:
                    _log("TTS playback error:\n" + traceback.format_exc())
            threading.Thread(target=_play, daemon=True).start()
            if analytics:
                try:
                    analytics.record_voice_action("play", language=load_settings().get("language", "en"))
                except Exception:
                    pass
            return
        # Optional cloud TTS (ElevenLabs) - commented for safety
        # if load_settings().get("use_elevenlabs") and load_settings().get("elevenlabs_key"):
        #     # implement ElevenLabs TTS call and play via local player
        #     pass
        _log("No TTS engine available; skipping speak.")


# ---------------------------
# Core Voice Assistant
# ---------------------------
class VoiceAssistant:
    def __init__(self):
        self.settings = load_settings()
        self.tts = TTS()
        self.mem = load_memory()
        self.listen_thread: Optional[threading.Thread] = None
        self.worker = queue.Queue()
        self._stop_event = threading.Event()
        self.recognizer = sr.Recognizer() if sr else None
        self.microphone = None
        if sr:
            try:
                self.microphone = sr.Microphone()
            except Exception:
                self.microphone = None
                _log("Microphone initialization failed or unavailable.")

    # -----------------------
    # Memory helpers
    # -----------------------
    def _get_conversation(self, user_id: str = "guest"):
        convs = self.mem.setdefault("conversations", {})
        return convs.setdefault(user_id, {"messages": []})

    def _append_memory(self, user_id: str, role: str, text: str):
        conv = self._get_conversation(user_id)
        conv["messages"].append({"role": role, "content": text, "ts": time.time()})
        save_memory(self.mem)

    # -----------------------
    # AI integration
    # -----------------------
    def ai_reply(self, text: str, user_id: str = "guest", max_tokens: int = 300) -> str:
        # Build context (short)
        context_msgs = []
        conv = self._get_conversation(user_id)
        # include last few messages for context
        for m in conv["messages"][-8:]:
            context_msgs.append({"role": m["role"], "content": m["content"]})
        # add user query
        context_msgs.append({"role": "user", "content": text})
        # call ai_engine if available
        if ai_engine:
            try:
                start = time.time()
                resp = ai_engine.chat(messages=context_msgs, max_tokens=max_tokens)
                # ai_engine API returns an object; try to extract text
                reply = None
                if isinstance(resp, dict) and resp.get("error"):
                    reply = f"(AI Error) {resp['error']}"
                else:
                    # try structured extraction
                    try:
                        # support both modern and wrapper shapes
                        if hasattr(resp, "choices"):
                            reply = resp.choices[0].message.content
                        elif isinstance(resp, dict) and "choices" in resp:
                            reply = resp["choices"][0]["message"]["content"]
                        elif isinstance(resp, dict) and "reply" in resp:
                            reply = resp["reply"]
                        else:
                            reply = str(resp)
                    except Exception:
                        reply = str(resp)
                latency = time.time() - start
                if analytics:
                    try:
                        analytics.record_ai_query(text, latency=round(latency, 3))
                    except Exception:
                        pass
                # store to memory
                self._append_memory(user_id, "user", text)
                self._append_memory(user_id, "assistant", reply)
                return reply
            except Exception as e:
                _log("AI reply error: " + traceback.format_exc())
                return f"(AI error) {e}"
        else:
            # fallback: echo + simple transformation
            reply = f"I heard: {text}"
            self._append_memory(user_id, "user", text)
            self._append_memory(user_id, "assistant", reply)
            return reply

    # -----------------------
    # Command handling
    # -----------------------
    def handle_command(self, text: str) -> Optional[str]:
        # Basic commands the assistant can recognize locally
        t = text.lower()
        if "time" in t:
            return time.strftime("The current time is %H:%M.")
        if "date" in t:
            return time.strftime("Today is %A, %B %d, %Y.")
        if "open book" in t or "read book" in t:
            return "Opening your book library now."
        if "crypto" in t:
            return "Fetching latest crypto insights."
        if "stop listening" in t or "stop" == t.strip():
            self.stop_listening()
            return "Stopped listening. Call me again to resume."
        return None

    # -----------------------
    # Listener loop (wake-word + query)
    # -----------------------
    def _listen_loop(self):
        _log("VoiceAssistant listening thread started.")
        if not self.recognizer or not self.microphone:
            _log("SpeechRecognition not available. Listen disabled.")
            return
        with self.microphone as src:
            self.recognizer.adjust_for_ambient_noise(src, duration=1)
        while not self._stop_event.is_set():
            try:
                with self.microphone as source:
                    # use shorter timeout to remain responsive
                    audio = self.recognizer.listen(source, timeout=6, phrase_time_limit=12)
                try:
                    lang = self.settings.get("language", DEFAULT_LANGUAGE) if (DEFAULT_LANGUAGE := "en-US") else "en-US"
                    text = self.recognizer.recognize_google(audio, language=self.settings.get("language", "en-US"))
                except Exception as e:
                    # ignoring recognition errors
                    continue
                if not text:
                    continue
                _log(f"Recognized: {text}")
                # wake-word detection
                wake = self.settings.get("wake_word", DEFAULT_WAKE_WORD).lower()
                if wake in text.lower():
                    # strip wake word and continue to accept query
                    query = text.lower().replace(wake, "").strip()
                    if not query:
                        # ask user to speak
                        self.tts.speak("Yes? How can I help?")
                        # next iteration will capture next phrase
                        continue
                    # check for simple local commands first
                    local = self.handle_command(query)
                    if local:
                        self.tts.speak(local)
                        continue
                    # otherwise route to AI
                    reply = self.ai_reply(query)
                    self.tts.speak(reply)
                else:
                    # optional: short mode - if direct query without wake-word, process depending on settings
                    if self.settings.get("enable_listen", True) and len(text.split()) > 2:
                        # treat as direct query
                        local = self.handle_command(text)
                        if local:
                            self.tts.speak(local)
                            continue
                        reply = self.ai_reply(text)
                        self.tts.speak(reply)
            except Exception:
                _log("Listen loop exception:\n" + traceback.format_exc())
                time.sleep(0.5)
        _log("VoiceAssistant listening thread ended.")

    # -----------------------
    # Public control
    # -----------------------
    def start_listening(self):
        if self.listen_thread and self.listen_thread.is_alive():
            _log("Listener already running.")
            return
        self._stop_event.clear()
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()
        _log("Started listening thread.")
        return True

    def stop_listening(self):
        self._stop_event.set()
        _log("Stop requested for listening thread.")
        return True

    def speak(self, text: str):
        self.tts.speak(text)

    def set_settings(self, updates: Dict[str, Any]):
        s = load_settings()
        s.update(updates)
        save_settings(s)
        self.settings = s
        self.tts._apply()
        _log(f"Settings updated: {updates}")
        if analytics:
            try:
                analytics.record_voice_action("settings", language=s.get("language", "en"))
            except Exception:
                pass

    def get_settings(self) -> Dict[str, Any]:
        return load_settings()

    # lightweight test method
    def test_speak(self, text: str = "This is a voice test from Neura AI."):
        self.speak(text)
        return True


# Single shared instance for importers
_voice_assistant_instance: Optional[VoiceAssistant] = None


def get_voice_assistant() -> VoiceAssistant:
    global _voice_assistant_instance
    if _voice_assistant_instance is None:
        _voice_assistant_instance = VoiceAssistant()
    return _voice_assistant_instance


# ---------------------------
# Quick CLI usage
# ---------------------------
if __name__ == "__main__":
    va = get_voice_assistant()
    va.speak("Neura voice assistant starting in premium mode.")
    # start listening loop (requires microphone)
    try:
        va.start_listening()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        va.stop_listening()
        _log("Voice assistant stopped by KeyboardInterrupt.")