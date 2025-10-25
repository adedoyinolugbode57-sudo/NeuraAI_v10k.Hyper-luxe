# theme_engine.py
"""
Theme Engine for NeuraAI_v10k Hyper-Luxe
Generates multi-color themes, exports CSS variables, and stores presets in DB.
Created by ChatGPT + Joshua Dav...
"""

import uuid
import random
from typing import Dict, List, Optional
from colorsys import rgb_to_hls, hls_to_rgb

from database import db  # uses the db instance from database.py

def make_id(prefix: str = "theme") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"

# Helper color utilities
def clamp(v, a=0, b=255): return max(a, min(b, int(v)))

def hex_from_rgb(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(clamp(r), clamp(g), clamp(b))

def rgb_from_hex(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def shift_hue(hex_color: str, deg: float) -> str:
    r, g, b = rgb_from_hex(hex_color)
    h, l, s = rgb_to_hls(r/255.0, g/255.0, b/255.0)
    new_h = (h + deg/360.0) % 1.0
    nr, ng, nb = hls_to_rgb(new_h, l, s)
    return hex_from_rgb(nr*255, ng*255, nb*255)

# Predefined Hyper-Luxe presets (multi-color gradients)
PRESETS = [
    {
        "id": "neon_cyber",
        "name": "Neon Cyber",
        "colors": ["#00e5ff", "#0066ff", "#7f00ff"],
        "accent": "#00e5ff"
    },
    {
        "id": "magenta_pulse",
        "name": "Magenta Pulse",
        "colors": ["#ff33cc", "#a6009e", "#3f007f"],
        "accent": "#ff33cc"
    },
    {
        "id": "sunset_gold",
        "name": "Sunset Gold",
        "colors": ["#ffb347", "#ffcc33", "#ff6b6b"],
        "accent": "#ffd24d"
    },
    {
        "id": "aqua_dream",
        "name": "Aqua Dream",
        "colors": ["#00ffcc", "#00a6ff", "#0066cc"],
        "accent": "#00ffcc"
    },
    {
        "id": "hyper_crystal",
        "name": "Hyper Crystal",
        "colors": ["#b3fffa", "#c0c0ff", "#ffb3ff"],
        "accent": "#a0e9ff"
    },
    {
        "id": "royal_matte",
        "name": "Royal Matte",
        "colors": ["#2b2d42", "#8d99ae", "#ef233c"],
        "accent": "#ef233c"
    },
    # add more presets (aim to create ~20 presets)
]

# Convert theme descriptor to CSS variables
def theme_to_cssvars(theme: Dict) -> Dict[str, str]:
    """
    Accepts a dict with keys: colors (list), accent (single).
    Returns CSS variables map: --bg-gradient, --accent, --accent-2, --accent-3, --text
    """
    colors = theme.get("colors", [])
    accent = theme.get("accent", colors[0] if colors else "#00e5ff")
    # build gradient string (3 or 2 stops)
    stops = ", ".join(colors) if colors else accent
    css = {
        "--bg-gradient": f"linear-gradient(135deg, {stops})",
        "--accent": accent,
        "--accent-2": colors[1] if len(colors) > 1 else accent,
        "--accent-3": colors[2] if len(colors) > 2 else css.get("--accent-2", accent),
        "--text-color": "#e8f0ff"
    }
    return css

# Render CSS text from css-vars dict
def render_css_from_theme(css_vars: Dict[str, str]) -> str:
    lines = [f":root {{"] 
    for k, v in css_vars.items():
        lines.append(f"  {k}: {v};")
    lines.append("}")
    return "\n".join(lines)

# Generate a random multi-color theme
def generate_custom_theme(base_color: Optional[str] = None, stops: int = 3) -> Dict:
    if not base_color:
        base_color = random.choice(["#00e5ff","#ff33cc","#ffd24d","#00ff99","#a070ff"])
    # create gradient by shifting hue
    colors = [base_color]
    for i in range(1, stops):
        deg = (i * (360/stops)) % 360
        colors.append(shift_hue(base_color, deg))
    accent = colors[0]
    return {"id": make_id(), "name": "Custom Theme", "colors": colors, "accent": accent}

# Persistence helpers (save preset to DB)
def save_theme_to_db(theme: Dict, owner_uid: Optional[str] = None, preset: bool = False):
    theme_id = theme.get("id") or make_id()
    css_vars = theme_to_cssvars(theme)
    db.save_theme(theme_id, theme.get("name", "Custom Theme"), css_vars, owner_uid=owner_uid, preset=preset)
    return theme_id

def get_presets() -> List[Dict]:
    # return presets (first check DB for preset overrides)
    # ensure presets are saved in DB once
    saved = {p["id"]: p for p in PRESETS}
    # create and save default presets in DB if missing
    for p in PRESETS:
        css_vars = theme_to_cssvars(p)
        db.save_theme(p["id"], p["name"], css_vars, owner_uid=None, preset=True)
    # fetch from DB
    rows = db.list_themes()
    presets = [r for r in rows if r.get("preset")]
    return presets

def get_user_themes(owner_uid: str):
    return db.list_themes(owner_uid=owner_uid)

# Example: return CSS string for a theme id
def css_for_theme_id(theme_id: str) -> Optional[str]:
    rec = db.get_theme(theme_id)
    if not rec:
        return None
    css_vars = rec.get("css_vars", {})
    return render_css_from_theme(css_vars)

# Optional: A tiny helper that returns a default theme (first preset)
def default_theme_css() -> str:
    presets = get_presets()
    if presets:
        return render_css_from_theme(presets[0]["css_vars"])
    # fallback
    return render_css_from_theme(theme_to_cssvars({"colors":["#00e5ff","#0066ff"], "accent":"#00e5ff"}))