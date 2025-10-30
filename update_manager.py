"""
update_manager.py
Neura-AI v10k.Hyperluxe — Update manager and changelog system
Author: ChatGPT + Joshua Dav
Purpose: Version management, changelogs, and remote update checking.

Usage:
    from update_manager import (
        UpdateManager, get_local_version, compare_versions
    )
"""

import os
import json
import requests
import time
from datetime import datetime
from typing import Optional, Dict, Any

# -------------------------------
# Configurations
# -------------------------------
LOCAL_VERSION_FILE = "version.json"  # Stored locally in project root
REMOTE_VERSION_URL = os.getenv("UPDATE_JSON_URL") or "https://example.com/neura_update.json"
CACHE_FILE = "update_cache.json"

# -------------------------------
# Helper functions
# -------------------------------
def get_local_version() -> str:
    """Return the current version of the app."""
    if not os.path.exists(LOCAL_VERSION_FILE):
        return "0.0.0"
    try:
        with open(LOCAL_VERSION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("version", "0.0.0")
    except Exception:
        return "0.0.0"

def save_local_version(version: str, notes: str = "") -> None:
    """Save the version locally."""
    data = {"version": version, "last_updated": datetime.utcnow().isoformat(), "notes": notes}
    with open(LOCAL_VERSION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def compare_versions(v1: str, v2: str) -> int:
    """
    Compare two version strings.
    Returns:
        -1 if v1 < v2
         0 if v1 == v2
         1 if v1 > v2
    """
    def normalize(v): return [int(x) for x in v.split(".") if x.isdigit()]
    a, b = normalize(v1), normalize(v2)
    return (a > b) - (a < b)

# -------------------------------
# Update Manager Class
# -------------------------------
class UpdateManager:
    """
    Handles update checking, changelogs, and version syncing.
    Works offline-first; caches last known version check.
    """

    def __init__(self, remote_url: str = REMOTE_VERSION_URL):
        self.remote_url = remote_url
        self.local_version = get_local_version()
        self.last_check = None
        self.cached_data = self._load_cache()

    def _load_cache(self) -> Dict[str, Any]:
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_cache(self, data: Dict[str, Any]) -> None:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def check_for_update(self, force_online: bool = False) -> Dict[str, Any]:
        """
        Checks if a new update is available.
        Tries online first (if allowed), then cache fallback.
        """
        self.last_check = datetime.utcnow().isoformat()
        remote_data = None

        if force_online:
            try:
                r = requests.get(self.remote_url, timeout=5)
                if r.status_code == 200:
                    remote_data = r.json()
                    self.cached_data = remote_data
                    self._save_cache(remote_data)
            except Exception:
                remote_data = None

        # fallback to cache if offline
        if not remote_data:
            remote_data = self.cached_data or {}

        remote_version = remote_data.get("version", "0.0.0")
        changelog = remote_data.get("changelog", "No changelog available.")
        compare_result = compare_versions(self.local_version, remote_version)

        info = {
            "local_version": self.local_version,
            "remote_version": remote_version,
            "is_update_available": compare_result == -1,
            "changelog": changelog,
            "checked_at": self.last_check,
        }
        return info

    def download_update(self, target_path: str = "update_package.zip") -> bool:
        """
        Download update package if available.
        Expects remote JSON to include a 'download_url'.
        """
        try:
            data = self.cached_data or {}
            url = data.get("download_url")
            if not url:
                print("⚠️ No download URL found in update data.")
                return False

            r = requests.get(url, stream=True, timeout=10)
            if r.status_code != 200:
                print(f"❌ Failed to download update. Status {r.status_code}")
                return False

            with open(target_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"✅ Update downloaded to {target_path}")
            return True
        except Exception as e:
            print("❌ Error while downloading:", e)
            return False

    def apply_update(self, new_version: str, notes: str = "") -> None:
        """
        Apply update (mark as installed).
        In production, you'd unpack files or restart your process.
        """
        save_local_version(new_version, notes)
        print(f"✅ Updated to version {new_version}")

    def pretty_print(self, info: Dict[str, Any]) -> None:
        """Display update info cleanly."""
        print("\n--- Neura-AI Update Status ---")
        print(f"Local Version : {info['local_version']}")
        print(f"Remote Version: {info['remote_version']}")
        print(f"Update Available: {'✅ Yes' if info['is_update_available'] else '❌ No'}")
        print(f"Last Checked  : {info['checked_at']}")
        print(f"\nChangelog:\n{info['changelog']}")
        print("------------------------------\n")

# -------------------------------
# Example CLI usage
# -------------------------------
if __name__ == "__main__":
    um = UpdateManager()
    print("Checking for updates...")
    info = um.check_for_update(force_online=False)
    um.pretty_print(info)
    if info["is_update_available"]:
        print("New version available!")
        if um.download_update():
            um.apply_update(info["remote_version"], notes="Auto-applied")