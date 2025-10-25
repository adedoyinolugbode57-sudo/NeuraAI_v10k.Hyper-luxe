# database.py
"""
Database helper for NeuraAI_v10k Hyper-Luxe
PostgreSQL via SQLAlchemy (sync). Read DATABASE_URL from env or component vars.
Created by ChatGPT + Joshua Dav...
"""

import os
import time
import logging
from typing import Optional, Dict, Any, List
from contextlib import contextmanager

from sqlalchemy import (
    create_engine, MetaData, Table, Column, Integer, String, Text, DateTime, Boolean, JSON, func
)
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import select, and_
from sqlalchemy.engine import Engine

logger = logging.getLogger("neura_db")
logger.setLevel(logging.INFO)

# Read DB url from env (recommended) or build from parts
DATABASE_URL = os.getenv("DATABASE_URL") or None
if not DATABASE_URL:
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS", "postgres")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "neura_v10k")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy engine (sync)
def create_engine_with_retry(url: str, retries: int = 3, backoff: float = 1.0) -> Engine:
    attempt = 0
    while True:
        try:
            engine = create_engine(url, pool_size=5, max_overflow=10, pool_pre_ping=True)
            # quick check
            conn = engine.connect()
            conn.close()
            logger.info("Connected to DB successfully")
            return engine
        except OperationalError as e:
            attempt += 1
            logger.warning("DB connection failed (attempt %s/%s): %s", attempt, retries, e)
            if attempt >= retries:
                raise
            time.sleep(backoff * attempt)

engine = create_engine_with_retry(DATABASE_URL)

metadata = MetaData()

# Tables
users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("uid", String(64), unique=True, nullable=False),        # external id (uuid)
    Column("username", String(128), nullable=True),
    Column("email", String(256), nullable=True),
    Column("created_at", DateTime, server_default=func.now()),
    Column("prefs", JSON, nullable=True)
)

conversations = Table(
    "conversations", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("convo_id", String(64), unique=True, nullable=False),
    Column("user_uid", String(64), nullable=True),
    Column("messages", JSON, nullable=False),   # array of msgs: [{role,content,ts},...]
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now())
)

themes = Table(
    "themes", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("theme_id", String(64), unique=True, nullable=False),
    Column("name", String(128), nullable=False),
    Column("owner_uid", String(64), nullable=True),
    Column("css_vars", JSON, nullable=False),   # dict of CSS variables
    Column("preset", Boolean, nullable=False, default=False),
    Column("created_at", DateTime, server_default=func.now())
)

usage_logs = Table(
    "usage_logs", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("event_type", String(64), nullable=False),
    Column("meta", JSON, nullable=True),
    Column("created_at", DateTime, server_default=func.now())
)

# Create tables if missing
metadata.create_all(engine)

# Database helper class
class Database:
    def __init__(self, engine=engine):
        self.engine = engine

    @contextmanager
    def get_conn(self):
        conn = self.engine.connect()
        try:
            yield conn
        finally:
            conn.close()

    # Users
    def create_user(self, uid: str, username: Optional[str] = None, email: Optional[str] = None, prefs: Optional[Dict] = None):
        with self.get_conn() as conn:
            stmt = users.insert().values(uid=uid, username=username, email=email, prefs=prefs or {})
            conn.execute(stmt)
        return {"ok": True, "uid": uid}

    def get_user(self, uid: str):
        with self.get_conn() as conn:
            stmt = select([users]).where(users.c.uid == uid)
            r = conn.execute(stmt).fetchone()
            return dict(r) if r else None

    # Conversations
    def upsert_conversation(self, convo_id: str, messages: List[Dict[str, Any]], user_uid: Optional[str] = None):
        with self.get_conn() as conn:
            # try update
            existing = conn.execute(select([conversations]).where(conversations.c.convo_id == convo_id)).fetchone()
            if existing:
                stmt = conversations.update().where(conversations.c.convo_id == convo_id).values(messages=messages, user_uid=user_uid)
                conn.execute(stmt)
            else:
                stmt = conversations.insert().values(convo_id=convo_id, user_uid=user_uid, messages=messages)
                conn.execute(stmt)
        return True

    def get_conversation(self, convo_id: str) -> Optional[List[Dict[str, Any]]]:
        with self.get_conn() as conn:
            r = conn.execute(select([conversations.c.messages]).where(conversations.c.convo_id == convo_id)).fetchone()
            return r[0] if r else None

    def list_conversations(self, limit: int = 50):
        with self.get_conn() as conn:
            r = conn.execute(select([conversations.c.convo_id, conversations.c.updated_at]).order_by(conversations.c.updated_at.desc()).limit(limit))
            return [dict(row) for row in r.fetchall()]

    # Themes
    def save_theme(self, theme_id: str, name: str, css_vars: Dict[str, str], owner_uid: Optional[str] = None, preset: bool = False):
        with self.get_conn() as conn:
            existing = conn.execute(select([themes]).where(themes.c.theme_id == theme_id)).fetchone()
            if existing:
                stmt = themes.update().where(themes.c.theme_id == theme_id).values(name=name, css_vars=css_vars, owner_uid=owner_uid, preset=preset)
                conn.execute(stmt)
            else:
                stmt = themes.insert().values(theme_id=theme_id, name=name, css_vars=css_vars, owner_uid=owner_uid, preset=preset)
                conn.execute(stmt)
        return True

    def get_theme(self, theme_id: str):
        with self.get_conn() as conn:
            r = conn.execute(select([themes]).where(themes.c.theme_id == theme_id)).fetchone()
            return dict(r) if r else None

    def list_themes(self, owner_uid: Optional[str] = None):
        with self.get_conn() as conn:
            if owner_uid:
                r = conn.execute(select([themes]).where(themes.c.owner_uid == owner_uid))
            else:
                r = conn.execute(select([themes]).order_by(themes.c.created_at.desc()))
            return [dict(row) for row in r.fetchall()]

    # Usage logs
    def log_event(self, event_type: str, meta: Optional[Dict] = None):
        with self.get_conn() as conn:
            stmt = usage_logs.insert().values(event_type=event_type, meta=meta or {})
            conn.execute(stmt)
        return True

# Single shared DB instance
db = Database()