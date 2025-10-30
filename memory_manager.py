"""
memory_manager.py
Neura-AI v10k.Hyperluxe
-------------------------------------
Handles dynamic AI memory:
- Conversation logs
- Long-term user preferences
- Auto-context recall
- Memory optimization for Render
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, Any, List

# Paths for memory files
MEMORY_FILE = "memory_store.json"
CHAT_LOGS_FILE = "chat_logs.json"
USER_PREF_FILE = "user_profiles.json"

# -------------------------------------------------------
# Utility Functions
# -------------------------------------------------------
def _read_json(path: str) -> Any:
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}
    except Exception:
        return {}

def _write_json(path: str, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def _timestamp() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

# -------------------------------------------------------
# MemoryManager Class
# -------------------------------------------------------
class MemoryManager:
    """
    Central class to handle AI memory and context.
    """

    def __init__(self):
        self.memory = _read_json(MEMORY_FILE)
        self.chat_logs = _read_json(CHAT_LOGS_FILE)
        self.user_prefs = _read_json(USER_PREF_FILE)
        self.max_memory_length = 20_000  # characters
        self.last_cleanup = None

    # ----------------------------
    # Conversation Memory
    # ----------------------------
    def add_message(self, user: str, message: str, response: str) -> None:
        """Save conversation pair."""
        entry = {
            "timestamp": _timestamp(),
            "user": user,
            "message": message,
            "response": response
        }

        self.chat_logs.setdefault("history", []).append(entry)
        _write_json(CHAT_LOGS_FILE, self.chat_logs)

        # Add to memory summary
        self.memory.setdefault("context", []).append({
            "msg": message,
            "reply": response
        })
        if len(json.dumps(self.memory)) > self.max_memory_length:
            self.optimize_memory()
        _write_json(MEMORY_FILE, self.memory)

    def get_recent_conversation(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Return recent conversation pairs."""
        return self.chat_logs.get("history", [])[-limit:]

    def summarize_memory(self) -> str:
        """Create a short memory summary for the AI model."""
        context = self.memory.get("context", [])
        if not context:
            return "No prior context."
        summary = " | ".join([f"{m['msg'][:30]}→{m['reply'][:30]}" for m in context[-10:]])
        return summary

    def optimize_memory(self) -> None:
        """Trim old messages if memory grows too large."""
        if "context" in self.memory:
            self.memory["context"] = self.memory["context"][-50:]
        self.last_cleanup = _timestamp()
        _write_json(MEMORY_FILE, self.memory)

    def clear_memory(self) -> None:
        """Reset all AI memory."""
        self.memory = {"context": []}
        self.chat_logs = {"history": []}
        _write_json(MEMORY_FILE, self.memory)
        _write_json(CHAT_LOGS_FILE, self.chat_logs)
        print("🧠 All memory cleared successfully.")

    # ----------------------------
    # User Preferences
    # ----------------------------
    def set_preference(self, user_id: str, key: str, value: Any) -> None:
        """Set user-specific preferences like theme, voice, or language."""
        prefs = self.user_prefs.get(user_id, {})
        prefs[key] = value
        self.user_prefs[user_id] = prefs
        _write_json(USER_PREF_FILE, self.user_prefs)

    def get_preference(self, user_id: str, key: str, default: Any = None) -> Any:
        """Retrieve user preferences."""
        return self.user_prefs.get(user_id, {}).get(key, default)

    def delete_preference(self, user_id: str, key: str) -> None:
        """Remove a preference."""
        if user_id in self.user_prefs and key in self.user_prefs[user_id]:
            del self.user_prefs[user_id][key]
            _write_json(USER_PREF_FILE, self.user_prefs)

    # ----------------------------
    # Analytics / Tracking
    # ----------------------------
    def count_messages(self) -> int:
        """Return total number of stored messages."""
        return len(self.chat_logs.get("history", []))

    def get_active_users(self) -> List[str]:
        """List all user IDs with saved preferences."""
        return list(self.user_prefs.keys())

    def get_last_active(self, user_id: str) -> Optional[str]:
        """Return last active timestamp of user."""
        history = self.chat_logs.get("history", [])
        for msg in reversed(history):
            if msg["user"] == user_id:
                return msg["timestamp"]
        return None

    # ----------------------------
    # Export / Import
    # ----------------------------
    def export_memory(self, export_path: str = "memory_backup.json") -> None:
        """Backup memory and logs to single file."""
        backup = {
            "memory": self.memory,
            "chat_logs": self.chat_logs,
            "user_prefs": self.user_prefs,
            "exported_at": _timestamp()
        }
        _write_json(export_path, backup)
        print(f"📦 Memory backup saved to {export_path}")

    def import_memory(self, import_path: str) -> None:
        """Restore backup from file."""
        if not os.path.exists(import_path):
            print("⚠️ Backup file not found.")
            return
        try:
            with open(import_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.memory = data.get("memory", {})
                self.chat_logs = data.get("chat_logs", {})
                self.user_prefs = data.get("user_prefs", {})
                _write_json(MEMORY_FILE, self.memory)
                _write_json(CHAT_LOGS_FILE, self.chat_logs)
                _write_json(USER_PREF_FILE, self.user_prefs)
            print("✅ Memory restored successfully.")
        except Exception as e:
            print("❌ Failed to restore memory:", e)

# -------------------------------------------------------
# Example CLI usage
# -------------------------------------------------------
if __name__ == "__main__":
    mm = MemoryManager()
    print("💾 Neura-AI Memory Manager Active")
    print("Recent messages:", mm.get_recent_conversation(2))
    print("Total messages:", mm.count_messages())
    print("Users:", mm.get_active_users())