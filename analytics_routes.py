# analytics_routes.py (v2.0 Premium)
"""
Flask blueprint for premium analytics endpoints for NeuraAI_v10k.Hyperluxe

Features:
- /summary                  -> aggregated summary
- /trends                   -> trending books/games/content
- /voice                    -> voice usage stats
- /chart-data               -> time-series ready for Chart.js / Recharts
- /export-csv               -> export events or selected data as CSV
- /backup                   -> trigger analytics backup (server-side)
- /insights                 -> short AI-generated insights summary (if ai_engine available)
- Admin protection via NEURA_ADMIN_TOKEN environment variable
"""

import os
import io
import csv
import json
import time
from datetime import datetime, timedelta
from functools import wraps
from flask import Blueprint, jsonify, request, current_app, send_file

# Optional project modules (may be missing in some setups)
try:
    import analytics as analytics_mod
except Exception:
    analytics_mod = None

try:
    from ai_engine import generate_insight  # your ai helper that can summarize analytics
except Exception:
    generate_insight = None

# voice assistant optional
try:
    from voice_assistant import get_voice_assistant
except Exception:
    get_voice_assistant = None

analytics_bp = Blueprint("analytics_bp", __name__)

# ---------- Admin protection ----------
def require_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        admin_token = os.getenv("NEURA_ADMIN_TOKEN")
        # If no token set, allow in dev mode (but log)
        if not admin_token:
            current_app.logger.warning("NEURA_ADMIN_TOKEN not set - analytics endpoints are unprotected!")
            return f(*args, **kwargs)
        token = request.headers.get("X-Admin-Token") or request.args.get("admin_token")
        if token != admin_token:
            return jsonify({"ok": False, "error": "unauthorized"}), 401
        return f(*args, **kwargs)
    return wrapper

# ---------- Helpers ----------
def _now_ts():
    return int(time.time())

def _read_events():
    if analytics_mod:
        try:
            return analytics_mod._read().get("events", [])
        except Exception:
            current_app.logger.exception("analytics_mod._read failed")
            return []
    # fallback: look for analytics_data.json file next to this module
    fallback = os.path.join(os.path.dirname(__file__), "analytics_data.json")
    if os.path.exists(fallback):
        try:
            with open(fallback, "r", encoding="utf-8") as f:
                return json.load(f).get("events", [])
        except Exception:
            return []
    return []

# ---------- Routes ----------
@analytics_bp.route("/summary", methods=["GET"])
@require_admin
def summary():
    """Aggregated summary for dashboard."""
    try:
        if analytics_mod:
            s = analytics_mod.summary()
            return jsonify({"ok": True, "summary": s})
        # Fallback minimal summary
        events = _read_events()
        books = {}
        users = set()
        ai_queries = 0
        for e in events:
            t = e.get("type")
            p = e.get("payload", {})
            if t == "book_view":
                books[p.get("book_id")] = books.get(p.get("book_id"), 0) + 1
            if t == "book_purchase":
                books[p.get("book_id")] = books.get(p.get("book_id"), 0) + 3
            if t == "ai_query":
                ai_queries += 1
            users.add(p.get("user") or p.get("ip") or "anon")
        return jsonify({
            "ok": True,
            "summary": {
                "total_events": len(events),
                "unique_users": len(users),
                "ai_queries": ai_queries,
                "tracked_books": len(books),
                "top_books": sorted([{"book_id": k, "score": v} for k, v in books.items()], key=lambda x: x["score"], reverse=True)[:5],
                "last_updated": datetime.utcnow().isoformat()
            }
        })
    except Exception as e:
        current_app.logger.exception("analytics.summary error")
        return jsonify({"ok": False, "error": str(e)}), 500

@analytics_bp.route("/trends", methods=["GET"])
@require_admin
def trends():
    """Return trending items (books, games, tags)."""
    try:
        limit = int(request.args.get("limit", 10))
        if analytics_mod:
            top = analytics_mod.trending_books(limit=limit)
            return jsonify({"ok": True, "trending_books": top})
        # fallback: compute from events
        events = _read_events()
        counts = {}
        for e in events:
            if e.get("type") == "book_view":
                bid = e.get("payload", {}).get("book_id")
                if bid:
                    counts[bid] = counts.get(bid, 0) + 1
        sorted_books = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:limit]
        return jsonify({"ok": True, "trending_books": [{"book_id": b, "views": v} for b,v in sorted_books]})
    except Exception as e:
        current_app.logger.exception("analytics.trends error")
        return jsonify({"ok": False, "error": str(e)}), 500

@analytics_bp.route("/voice", methods=["GET"])
@require_admin
def voice_stats():
    """Voice usage breakdown by language/mood."""
    try:
        if analytics_mod:
            vp = analytics_mod.voice_popularity()
            return jsonify({"ok": True, "voice_popularity": vp})
        # fallback
        events = _read_events()
        voice = {}
        for e in events:
            if e.get("type") == "voice_action":
                lang = e.get("payload", {}).get("language", "unknown")
                voice[lang] = voice.get(lang, 0) + 1
        return jsonify({"ok": True, "voice_popularity": voice})
    except Exception as e:
        current_app.logger.exception("analytics.voice error")
        return jsonify({"ok": False, "error": str(e)}), 500

@analytics_bp.route("/chart-data", methods=["GET"])
@require_admin
def chart_data():
    """
    Returns timeseries data for charts.
    Query params:
      - timeframe: hours|days (default hours)
      - bucket: int (bucket size in minutes for 'hours' or days for 'days')
    """
    try:
        timeframe = request.args.get("timeframe", "hours")
        bucket = int(request.args.get("bucket", 1))
        events = _read_events()
        now = datetime.utcnow()
        points = {}
        if timeframe == "hours":
            start = now - timedelta(hours=24)
            # buckets in minutes
            for e in events:
                ts = e.get("timestamp") or e.get("payload", {}).get("timestamp") or time.time()
                dt = datetime.utcfromtimestamp(ts if isinstance(ts,(int,float)) else float(ts))
                if dt < start:
                    continue
                # bucket key
                minute = (dt.hour * 60 + dt.minute) // bucket * bucket
                key = f"{dt.hour:02d}:{(minute%60):02d}"
                points[key] = points.get(key, 0) + 1
        else:
            # days (last 30)
            start = now - timedelta(days=30)
            for e in events:
                ts = e.get("timestamp") or e.get("payload", {}).get("timestamp") or time.time()
                dt = datetime.utcfromtimestamp(ts if isinstance(ts,(int,float)) else float(ts))
                if dt < start:
                    continue
                key = dt.strftime("%Y-%m-%d")
                points[key] = points.get(key, 0) + 1
        # build sorted series
        series = [{"label": k, "value": v} for k, v in sorted(points.items())]
        return jsonify({"ok": True, "series": series})
    except Exception as e:
        current_app.logger.exception("analytics.chart_data error")
        return jsonify({"ok": False, "error": str(e)}), 500

@analytics_bp.route("/export-csv", methods=["GET"])
@require_admin
def export_csv():
    """
    Export events as CSV.
    Query params:
      - type: event type filter (optional)
      - limit: max rows (default 5000)
    """
    try:
        ev_type = request.args.get("type")
        limit = int(request.args.get("limit", 5000))
        events = _read_events()
        if ev_type:
            events = [e for e in events if e.get("type") == ev_type]
        events = events[:limit]
        # create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        # collect header keys
        header = ["timestamp", "type", "payload"]
        writer.writerow(header)
        for e in events:
            ts = e.get("timestamp") or time.time()
            writer.writerow([datetime.utcfromtimestamp(ts).isoformat() if isinstance(ts,(int,float)) else ts, e.get("type"), json.dumps(e.get("payload", {}), ensure_ascii=False)])
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode("utf-8")),
            mimetype="text/csv",
            as_attachment=True,
            download_name=f"analytics_export_{int(time.time())}.csv"
        )
    except Exception as e:
        current_app.logger.exception("analytics.export_csv error")
        return jsonify({"ok": False, "error": str(e)}), 500

@analytics_bp.route("/backup", methods=["POST"])
@require_admin
def backup():
    """Trigger analytics backup (writes a timestamped file in backups/)."""
    try:
        if analytics_mod:
            out = analytics_mod.backup_analytics()
            return jsonify({"ok": True, "backup_path": out})
        # fallback: write raw events to backups/
        events = _read_events()
        backup_dir = os.path.join(os.path.dirname(__file__), "backups")
        os.makedirs(backup_dir, exist_ok=True)
        fname = os.path.join(backup_dir, f"analytics_backup_{int(time.time())}.json")
        with open(fname, "w", encoding="utf-8") as f:
            json.dump({"events": events}, f, indent=2, ensure_ascii=False)
        return jsonify({"ok": True, "backup_path": fname})
    except Exception as e:
        current_app.logger.exception("analytics.backup error")
        return jsonify({"ok": False, "error": str(e)}), 500

@analytics_bp.route("/insights", methods=["GET"])
@require_admin
def insights():
    """
    Generate a short AI insight summary of analytics.
    Requires an insight generator in ai_engine (generate_insight) to be available.
    Falls back to a simple heuristic if not present.
    """
    try:
        if generate_insight:
            # attempt to call ai-powered insight generator
            try:
                insight = generate_insight()
                return jsonify({"ok": True, "insight": insight})
            except Exception:
                current_app.logger.exception("generate_insight failed")
        # fallback heuristic insight
        events = _read_events()
        total = len(events)
        last_24h = 0
        cutoff = time.time() - 24 * 3600
        types = {}
        for e in events:
            ts = e.get("timestamp") or e.get("payload", {}).get("timestamp") or time.time()
            try:
                tsv = float(ts)
            except Exception:
                tsv = time.time()
            if tsv >= cutoff:
                last_24h += 1
            typ = e.get("type")
            types[typ] = types.get(typ, 0) + 1
        top_types = sorted(types.items(), key=lambda x: x[1], reverse=True)[:3]
        insight = {
            "summary": f"{last_24h} events in the last 24 hours (total {total}).",
            "top_event_types": [{ "type": t, "count": c } for t,c in top_types]
        }
        return jsonify({"ok": True, "insight": insight})
    except Exception as e:
        current_app.logger.exception("analytics.insights error")
        return jsonify({"ok": False, "error": str(e)}), 500

# Optional simple voice control endpoints to trigger voice assistant for testing
@analytics_bp.route("/voice/test-speak", methods=["POST"])
@require_admin
def voice_test_speak():
    """Trigger the voice assistant to speak a phrase (for system checks)."""
    try:
        data = request.get_json(silent=True) or {}
        text = data.get("text", "This is a system voice test from NeuraAI analytics.")
        if get_voice_assistant:
            va = get_voice_assistant()
            va.test_speak(text)
            return jsonify({"ok": True, "spoken": text})
        return jsonify({"ok": False, "error": "voice assistant not available"}), 500
    except Exception as e:
        current_app.logger.exception("analytics.voice_test_speak error")
        return jsonify({"ok": False, "error": str(e)}), 500

# Health endpoint (non-admin)
@analytics_bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "ok": True,
        "analytics_loaded": analytics_mod is not None,
        "voice_loaded": get_voice_assistant is not None,
        "timestamp": datetime.utcnow().isoformat()
    })