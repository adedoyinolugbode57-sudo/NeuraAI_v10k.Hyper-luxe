"""
language_detector.py
Detect and track language changes per session for Neuraluxe-AI.
Supports dynamic language switching and multilingual context handling.
"""

from collections import deque
from langdetect import detect, DetectorFactory

# Fix random seed for consistent detection
DetectorFactory.seed = 0

# Max history to track recent messages
MAX_HISTORY = 20

class LanguageSession:
    """
    Tracks language per session and handles sudden switches.
    """
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.recent_languages = deque(maxlen=MAX_HISTORY)
        self.current_language = "English"  # default

    def detect(self, text: str) -> str:
        """
        Detect the language of the text.
        Updates the current session language intelligently.
        """
        try:
            lang = detect(text)
        except:
            lang = "unknown"

        self.recent_languages.append(lang)
        self._update_current_language()
        return lang

    def _update_current_language(self):
        """
        Update the current language based on recent messages.
        If a user switches temporarily, don't immediately switch.
        """
        if not self.recent_languages:
            return

        # Count frequency of languages in recent messages
        freq = {}
        for l in self.recent_languages:
            freq[l] = freq.get(l, 0) + 1

        # Pick the most frequent language in the window
        most_common_lang = max(freq, key=freq.get)

        # Only switch if a new language appears multiple times
        if most_common_lang != self.current_language and freq[most_common_lang] >= 2:
            self.current_language = most_common_lang

    def get_current_language(self) -> str:
        return self.current_language

# ------------------------
# Example usage
# ------------------------
if __name__ == "__main__":
    session = LanguageSession(user_id="user123")

    texts = [
        "Hello, how are you?",
        "I am fine, thanks!",
        "Bonjour, comment ça va?",
        "Ça va très bien, merci!",
        "Back to English now."
    ]

    for t in texts:
        detected = session.detect(t)
        print(f"Message: {t}")
        print(f"Detected language: {detected}")
        print(f"Session language: {session.get_current_language()}\n")