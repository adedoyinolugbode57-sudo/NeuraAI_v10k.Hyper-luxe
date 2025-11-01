"""
emotion_mixer.py
Blend multiple emotional inputs to generate complex moods.
"""

import random

class EmotionMixer:
    def __init__(self):
        self.emotions = ["happy", "sad", "angry", "excited", "fearful", "calm", "surprised", "disgusted"]
    
    def mix_emotions(self, *input_emotions):
        mixed_score = {}
        for emotion in self.emotions:
            mixed_score[emotion] = 0
        
        for e in input_emotions:
            if e in mixed_score:
                mixed_score[e] += random.uniform(0.5, 1.5)
            else:
                mixed_score[e] = random.uniform(0.1, 0.5)
        
        # Normalize scores
        total = sum(mixed_score.values())
        for e in mixed_score:
            mixed_score[e] /= total
        
        return mixed_score
    
    def dominant_emotion(self, *input_emotions):
        scores = self.mix_emotions(*input_emotions)
        return max(scores, key=scores.get)
    
    def emotional_description(self, *input_emotions):
        scores = self.mix_emotions(*input_emotions)
        description = "The blended emotion is "
        sorted_emotions = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        description += ", ".join([f"{e} ({round(s*100)}%)" for e, s in sorted_emotions[:3]])
        return description

# Example usage
if __name__ == "__main__":
    mixer = EmotionMixer()
    print(mixer.dominant_emotion("happy", "excited", "fearful"))
    print(mixer.emotional_description("sad", "calm", "angry"))