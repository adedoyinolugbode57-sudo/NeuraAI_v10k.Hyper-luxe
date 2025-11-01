"""
fictional_language_translator.py
Translate text into fictional or constructed languages (mock).
"""

import random

class FictionalTranslator:
    def __init__(self):
        self.languages = ["Elvish", "Klingon", "Dothraki", "Huttese", "Esperanto-Fictional"]
    
    def translate(self, text: str, language: str = None) -> str:
        language = language or random.choice(self.languages)
        words = text.split()
        transformed = [self._fancy_transform(word) for word in words]
        return f"[{language}] " + " ".join(transformed)
    
    def _fancy_transform(self, word: str) -> str:
        # simple mock transformation
        return "".join(random.choice("aeiouy") + c for c in word)
    
    def detect_language(self, text: str) -> str:
        return random.choice(self.languages)

# Example usage
if __name__ == "__main__":
    translator = FictionalTranslator()
    print(translator.translate("Hello world"))
    print(translator.translate("The quick brown fox jumps over the lazy dog", "Dothraki"))