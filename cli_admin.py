# cli_admin.py
"""
🎛️ NeuraAI v10k Hyperluxe Admin CLI

Usage:
    python cli_admin.py init-db
    python cli_admin.py list-users
    python cli_admin.py add-theme [uid]
    python cli_admin.py bulk-add-themes <count> [uid]
    python cli_admin.py update-user-theme <uid>
    python cli_admin.py delete-user <uid>
    python cli_admin.py list-themes
    python cli_admin.py alembic-upgrade
"""

import sys
import subprocess
from database import db
from theme_engine import generate_custom_theme, save_theme_to_db, list_all_themes

# -----------------------
# Database & CLI Helpers
# -----------------------

def init_db():
    """Initialize DB tables using SQLAlchemy metadata"""
    try:
        print("🔧 Initializing database...")
        db.create_all()
        db.log_event("init_db", {"status": "ok"})
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"⚠️ DB init failed: {e}")

def list_users():
    """List all registered users"""
    try:
        with db.get_conn() as conn:
            users = conn.execute("SELECT uid, username, email FROM users").fetchall()
        print("👤 Registered Users:")
        for u in users:
            print(f" - {u.uid} | {u.username or 'N/A'} | {u.email or 'N/A'}")
    except Exception as e:
        print(f"⚠️ Error listing users: {e}")

def add_theme(uid=None):
    """Add a single custom theme"""
    try:
        theme = generate_custom_theme()
        tid = save_theme_to_db(theme, owner_uid=uid)
        print(f"🎨 Theme {tid} added for user {uid or 'None'}")
    except Exception as e:
        print(f"⚠️ Failed to add theme: {e}")

def bulk_add_themes(count, uid=None):
    """Add multiple themes at once"""
    try:
        count = int(count)
        print(f"⚡ Generating {count} custom themes for user {uid or 'None'}...")
        for i in range(count):
            theme = generate_custom_theme()
            tid = save_theme_to_db(theme, owner_uid=uid)
            print(f"  - Theme {tid} added")
        print(f"✅ Bulk addition complete ({count} themes).")
    except ValueError:
        print("⚠️ Invalid count. Must be a number.")
    except Exception as e:
        print(f"⚠️ Bulk add failed: {e}")

def update_user_theme(uid):
    """Assign a new theme to a user"""
    if not uid:
        print("⚠️ Please provide a user UID.")
        return
    try:
        theme = generate_custom_theme()
        tid = save_theme_to_db(theme, owner_uid=uid)
        print(f"✨ User {uid} updated with new theme {tid}")
    except Exception as e:
        print(f"⚠️ Failed to update user theme: {e}")

def delete_user(uid):
    """Delete a user from DB"""
    if not uid:
        print("⚠️ Please provide a user UID.")
        return
    try:
        with db.get_conn() as conn:
            res = conn.execute("DELETE FROM users WHERE uid = ?", (uid,))
            if res.rowcount:
                print(f"🗑️ User {uid} deleted successfully.")
            else:
                print(f"⚠️ User {uid} not found.")
    except Exception as e:
        print(f"⚠️ Failed to delete user: {e}")

def list_themes():
    """List all saved themes"""
    try:
        themes = list_all_themes()
        if not themes:
            print("🎨 No themes found.")
            return
        print("🎨 Saved Themes:")
        for t in themes:
            print(f" - {t['tid']} | Owner UID: {t.get('owner_uid','None')} | Colors: {t['colors']}")
    except Exception as e:
        print(f"⚠️ Error listing themes: {e}")

def alembic_upgrade():
    """Run Alembic migrations"""
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("✅ Alembic migrations applied successfully.")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Alembic upgrade failed: {e}")

# -----------------------
# Command Dispatcher
# -----------------------

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    arg1 = sys.argv[2] if len(sys.argv) > 2 else None
    arg2 = sys.argv[3] if len(sys.argv) > 3 else None

    if cmd == "init-db":
        init_db()
    elif cmd == "list-users":
        list_users()
    elif cmd == "add-theme":
        add_theme(arg1)
    elif cmd == "bulk-add-themes":
        if not arg1:
            print("⚠️ Please provide a count of themes to generate.")
        else:
            bulk_add_themes(arg1, arg2)
    elif cmd == "update-user-theme":
        update_user_theme(arg1)
    elif cmd == "delete-user":
        delete_user(arg1)
    elif cmd == "list-themes":
        list_themes()
    elif cmd == "alembic-upgrade":
        alembic_upgrade()
    else:
        print(__doc__)