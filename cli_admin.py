# cli_admin.py
"""
Admin CLI for NeuraAI_v10k.Hyperluxe
Usage:
    python cli_admin.py init-db
    python cli_admin.py list-users
    python cli_admin.py add-theme "user123"
    python cli_admin.py alembic-upgrade
"""

import sys
import subprocess
from database import db
from theme_engine import generate_custom_theme, save_theme_to_db

def init_db():
    print("✅ Database tables auto-created via SQLAlchemy metadata.")
    db.log_event("init_db", {"status": "ok"})

def list_users():
    with db.get_conn() as conn:
        r = conn.execute("SELECT uid, username, email FROM users").fetchall()
        print("👤 Registered Users:")
        for row in r:
            print(f" - {row.uid} | {row.username or 'N/A'} | {row.email or 'N/A'}")

def add_theme(uid=None):
    theme = generate_custom_theme()
    tid = save_theme_to_db(theme, owner_uid=uid)
    print(f"🎨 Theme {tid} added for user {uid or 'None'}")

def alembic_upgrade():
    subprocess.run(["alembic", "upgrade", "head"], check=True)

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    if cmd == "init-db":
        init_db()
    elif cmd == "list-users":
        list_users()
    elif cmd == "add-theme":
        add_theme(sys.argv[2] if len(sys.argv) > 2 else None)
    elif cmd == "alembic-upgrade":
        alembic_upgrade()
    else:
        print(__doc__)