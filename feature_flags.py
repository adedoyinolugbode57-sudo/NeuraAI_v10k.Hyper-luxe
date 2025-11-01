"""
feature_flags.py
Manage experimental feature flags.
"""
FEATURES = {"beta_chat": False, "dark_mode": True}
def is_enabled(feature: str) -> bool:
    return FEATURES.get(feature, False)