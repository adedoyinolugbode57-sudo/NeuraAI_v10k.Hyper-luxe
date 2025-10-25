# automation.py
"""
automation.py
Simple scheduler + webhook trigger helpers for background automation jobs.
Not a full cron replacement — small, reliable worker queue.
"""

import threading
import time
import logging
import requests
from typing import Callable, Any, Dict

logger = logging.getLogger("automation")
logger.setLevel(logging.INFO)

_jobs = []
_jobs_lock = threading.Lock()
_worker_running = True

def schedule(interval_seconds: int, func: Callable, run_immediately: bool = False, kwargs: Dict = None):
    """
    Schedule a repeating job. Returns job id (int).
    """
    if kwargs is None:
        kwargs = {}
    job = {"interval": interval_seconds, "func": func, "kwargs": kwargs, "next": time.time() + (0 if run_immediately else interval_seconds)}
    with _jobs_lock:
        _jobs.append(job)
    return id(job)

def start_worker():
    """
    Start background worker in a daemon thread.
    """
    def loop():
        while _worker_running:
            now = time.time()
            with _jobs_lock:
                for job in _jobs:
                    if now >= job["next"]:
                        try:
                            job["func"](**job["kwargs"])
                        except Exception:
                            logger.exception("Job failed")
                        job["next"] = now + job["interval"]
            time.sleep(0.5)
    t = threading.Thread(target=loop, daemon=True)
    t.start()
    return t

def stop_worker():
    global _worker_running
    _worker_running = False

def trigger_webhook(url: str, payload: dict, headers: dict = None, timeout: int = 8):
    try:
        r = requests.post(url, json=payload, headers=headers or {}, timeout=timeout)
        return {"status": r.status_code, "body": r.text}
    except Exception as e:
        logger.exception("Webhook trigger failed")
        return {"error": str(e)}