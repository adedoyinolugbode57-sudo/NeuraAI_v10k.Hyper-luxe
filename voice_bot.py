# voice_bot.py
"""
voice_bot.py
Generates spoken audio from text. Uses gTTS (Google TTS) by default (no heavy deps).
Optional local pyttsx3 fallback.
"""

import os
import logging
from pathlib import Path
from typing import Optional
from config import ENABLE_TTS

logger = logging.getLogger("voice_bot")
logger.setLevel(logging.INFO)

TMP_DIR = Path("/tmp/neura_voice")
TMP_DIR.mkdir(parents=True, exist_ok=True)

def text_to_speech_gtts(text: str, lang: str = "en", filename: Optional[str] = None) -> Optional[str]:
    try:
        from gtts import gTTS
    except Exception:
        logger.exception("gTTS not installed")
        return None
    if not filename:
        filename = f"tts_{int(time.time())}.mp3"
    out = TMP_DIR / filename
    try:
        t = gTTS(text=text, lang=lang)
        t.save(str(out))
        return str(out)
    except Exception:
        logger.exception("gTTS failed")
        return None

def text_to_speech_pyttsx3(text: str, filename: Optional[str] = None) -> Optional[str]:
    # offline fallback (may fail on headless servers)
    try:
        import pyttsx3
    except Exception:
        logger.exception("pyttsx3 not available")
        return None
    engine = pyttsx3.init()
    if not filename:
        filename = f"tts_{int(time.time())}.mp3"
    out = TMP_DIR / filename
    try:
        engine.save_to_file(text, str(out))
        engine.runAndWait()
        return str(out)
    except Exception:
        logger.exception("pyttsx3 failed")
        return None

def speak(text: str, method: str = "gtts", lang: str = "en"):
    if not ENABLE_TTS:
        logger.info("TTS disabled in config")
        return None
    if method == "pyttsx3":
        return text_to_speech_pyttsx3(text)
    return text_to_speech_gtts(text, lang=lang)