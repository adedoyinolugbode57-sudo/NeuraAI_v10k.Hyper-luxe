STORY_PATHS = {}

def add_story_segment(segment_id: str, text: str, next_ids: list):
    STORY_PATHS[segment_id] = {"text": text, "next": next_ids}

def get_segment(segment_id: str):
    return STORY_PATHS.get(segment_id, {"text": "The end.", "next": []})