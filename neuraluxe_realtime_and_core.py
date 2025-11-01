neuraluxe_realtime_and_core.py

""" Two independent modules in one file for easy copy/paste:

1. broker_dashboard (real-time streaming dashboard + test broker adapter)

Lightweight Flask app + SSE (server-sent events) stream at /stream

BrokerAdapter class simulates/bridges to real brokers and publishes events

TestBrokerAdapter simulates many bots and sends trade events

HTML dashboard available at /dashboard that listens to SSE



2. neura_core_overview (Neuraluxe Intelligence Core)

Provides a simple JSON status endpoint /core/status that aggregates module health, available AI models, queue lengths, and broker stats

Can be polled by monitoring or used by admin UI




How to use:

Save this file in your project root (e.g. neuraluxe_realtime_and_core.py)

Install Flask: pip install flask

Optionally set REDIS_URL env var to enable Redis pub/sub integration

Run: python neuraluxe_realtime_and_core.py

Open http://127.0.0.1:5055/dashboard to view live events


Notes:

SSE is used so the dashboard works in browsers without websockets.

The TestBrokerAdapter can simulate N bots and N events/sec (adjustable).

The Core overview reads metrics from in-process state; if you integrate with Redis or a database you can enhance persistence and cross-process visibility.


"""

import os import time import json import uuid import random import threading from queue import Queue, Empty from datetime import datetime from typing import Dict, Any, Optional

from flask import Flask, Response, stream_with_context, render_template_string, jsonify, request

-------------------------

Configuration

-------------------------

HOST = os.getenv("HOST", "127.0.0.1") PORT = int(os.getenv("PORT", 5055)) REDIS_URL = os.getenv("REDIS_URL", "")  # optional: if set, the adapter will try to publish there MAX_BOTS_PER_USER = int(os.getenv("MAX_BOTS_PER_USER", 30)) MAX_CONCURRENT_BOTS = int(os.getenv("MAX_CONCURRENT_BOTS", 600))

-------------------------

In-process pub/sub queue

-------------------------

_event_queue: "Queue[Dict[str,Any]]" = Queue() _metrics_lock = threading.Lock() _METRICS: Dict[str, Any] = { "total_events": 0, "last_event": None, "active_brokers": {},  # broker_id -> stats }

-------------------------

Broker Adapter

-------------------------

class BrokerAdapter: """Abstract broker adapter interface. Implementations should call publish_event().""" def init(self, broker_id: Optional[str] = None): self.broker_id = broker_id or f"broker_{uuid.uuid4().hex[:8]}" self.connected = False self.stats = {"sent": 0, "errors": 0, "last_sent_ts": None}

def connect(self):
    # In real adapter you'd open API sessions, authenticate, etc.
    self.connected = True
    with _metrics_lock:
        _METRICS["active_brokers"][self.broker_id] = self.stats
    return True

def disconnect(self):
    self.connected = False
    with _metrics_lock:
        _METRICS["active_brokers"].pop(self.broker_id, None)

def publish_event(self, event: Dict[str, Any]):
    try:
        # Real adapter: send to broker or record to Redis / DB
        _event_queue.put(event)
        self.stats["sent"] += 1
        self.stats["last_sent_ts"] = datetime.utcnow().isoformat()
        with _metrics_lock:
            _METRICS["total_events"] += 1
            _METRICS["last_event"] = event
        return True
    except Exception as e:
        self.stats["errors"] += 1
        return False

class TestBrokerAdapter(BrokerAdapter): """Lightweight simulator that generates trade events for many bots/users.

Usage: instantiate and call start_simulation(num_users=..., bots_per_user=..., events_per_second=...)
"""
def __init__(self, broker_id: Optional[str] = None):
    super().__init__(broker_id=broker_id)
    self._running = False
    self._thread = None

def _gen_trade_event(self, user_id: str, bot_id: str) -> Dict[str, Any]:
    side = random.choice(["buy", "sell"])
    symbol = random.choice(["BTCUSD", "ETHUSD", "NEURAUSD", "AAPL", "TSLA"])
    price = round(random.uniform(10, 60000), 2)
    size = round(random.uniform(0.001, 5.0), 6)
    return {
        "event_type": "trade",
        "broker_id": self.broker_id,
        "user_id": user_id,
        "bot_id": bot_id,
        "side": side,
        "symbol": symbol,
        "price": price,
        "size": size,
        "timestamp": datetime.utcnow().isoformat()
    }

def _sim_loop(self, num_users: int, bots_per_user: int, eps: float):
    users = [f"user_{i+1:04d}" for i in range(num_users)]
    bots = {}
    for u in users:
        bots[u] = [f"bot_{u}_{j+1:02d}" for j in range(bots_per_user)]
    self.connect()
    self._running = True
    try:
        while self._running:
            # send events_per_second total events distributed randomly
            for _ in range(max(1, int(eps))):
                u = random.choice(users)
                b = random.choice(bots[u])
                ev = self._gen_trade_event(u, b)
                self.publish_event(ev)
            time.sleep(1.0)
    except Exception:
        self._running = False

def start_simulation(self, num_users: int = 100, bots_per_user: int = 5, events_per_second: float = 20.0):
    """Start the background simulator thread."""
    if self._thread and self._thread.is_alive():
        return False
    # safety caps
    total_bots = num_users * bots_per_user
    if bots_per_user > MAX_BOTS_PER_USER:
        raise ValueError(f"bots_per_user exceed allowed max: {MAX_BOTS_PER_USER}")
    if total_bots > MAX_CONCURRENT_BOTS:
        raise ValueError(f"total bots exceed allowed concurrency: {MAX_CONCURRENT_BOTS}")
    self._thread = threading.Thread(target=self._sim_loop, args=(num_users, bots_per_user, events_per_second), daemon=True)
    self._thread.start()
    return True

def stop_simulation(self):
    self._running = False
    if self._thread:
        self._thread.join(timeout=2)
    self.disconnect()

-------------------------

Flask App + SSE Stream

-------------------------

app = Flask(name)

DASH_TEMPLATE = """ <!doctype html>

<html>
<head>
  <meta charset="utf-8" />
  <title>Neuraluxe Broker Dashboard (Live)</title>
  <style>
    body{font-family:Inter,Arial;background:#071127;color:#e6f0ff;padding:20px}
    .card{background:#0f1a2b;padding:12px;border-radius:8px;margin-bottom:12px}
    pre{white-space:pre-wrap}
  </style>
</head>
<body>
  <h1>Neuraluxe Broker Dashboard — Live Events</h1>
  <div class="card">
    <strong>Total events:</strong> <span id="total">0</span>
    &nbsp;|&nbsp; <strong>Last event:</strong> <span id="last">-</span>
  </div>
  <div class="card" id="events"></div>
  <script>
    const evtSource = new EventSource('/stream');
    const eventsDiv = document.getElementById('events');
    const totalSpan = document.getElementById('total');
    const lastSpan = document.getElementById('last');
    evtSource.onmessage = function(e){
      try{
        const d = JSON.parse(e.data);
        totalSpan.textContent = d.metrics.total_events;
        lastSpan.textContent = d.metrics.last_event ? d.metrics.last_event.symbol + ' @ ' + d.metrics.last_event.price : '-';
        const p = document.createElement('pre');
        p.textContent = JSON.stringify(d.event, null, 2);
        eventsDiv.insertBefore(p, eventsDiv.firstChild);
        if (eventsDiv.childElementCount > 100) eventsDiv.removeChild(eventsDiv.lastChild);
      }catch(err){console.error(err)}
    };
  </script>
</body>
</html>
"""@app.route('/dashboard') def dashboard(): return render_template_string(DASH_TEMPLATE)

@app.route('/stream') def stream(): def event_stream(): # SSE generator while True: try: ev = _event_queue.get(timeout=0.5) with _metrics_lock: metrics_snapshot = json.loads(json.dumps(_METRICS)) payload = {"event": ev, "metrics": metrics_snapshot} yield f"data: {json.dumps(payload)}\n\n" except Empty: # send a heartbeat every 10s to keep connection alive yield 'data: {"heartbeat": true}\n\n' return Response(stream_with_context(event_stream()), mimetype='text/event-stream')

@app.route('/publish_test', methods=['POST']) def publish_test(): """Endpoint to push a test event to the stream (useful for remote tests).""" payload = request.get_json(silent=True) or {} event = payload.get('event') or {"note": "manual test", "ts": datetime.utcnow().isoformat()} _event_queue.put(event) return jsonify({"ok": True, "queued": True})

-------------------------

Neura Intelligence Core overview

-------------------------

@app.route('/core/status', methods=['GET']) def core_status(): """Return aggregated status of important subsystems. This endpoint is intentionally simple so your monitoring tools can poll it frequently. """ # quick snapshot with _metrics_lock: metrics = json.loads(json.dumps(_METRICS)) # determine module list (best-effort: try to read modules.json or modules.txt) modules_list = [] try: if os.path.exists('modules.json'): with open('modules.json', 'r', encoding='utf-8') as f: mj = json.load(f) modules_list = mj.get('modules') or list(mj.keys()) elif os.path.exists('modules.txt'): with open('modules.txt', 'r', encoding='utf-8') as f: modules_list = [l.strip() for l in f.readlines() if l.strip()] except Exception: modules_list = []

# health heuristics
health = {
    'uptime_seconds': int(time.time() - app_start_ts),
    'event_queue_size': _event_queue.qsize(),
    'total_events': metrics.get('total_events', 0),
    'last_event': metrics.get('last_event'),
    'active_brokers_count': len(metrics.get('active_brokers', {})),
    'modules_count': len(modules_list),
    'modules_sample': modules_list[:50]
}
return jsonify({'ok': True, 'health': health})

-------------------------

Small CLI test runner

-------------------------

def run_demo(): # start a TestBrokerAdapter that simulates many bots sim = TestBrokerAdapter(broker_id='test_broker_01') sim.start_simulation(num_users=80, bots_per_user=3, events_per_second=60) print(f"Started test broker simulation (broker_id={sim.broker_id})")

-------------------------

Main

-------------------------

app_start_ts = time.time()

if name == 'main': # If run directly, start simulation and Flask app demo_thread = threading.Thread(target=run_demo, daemon=True) demo_thread.start() print(f"Neuraluxe realtime dashboard running on http://{HOST}:{PORT}/dashboard") app.run(host=HOST, port=PORT, debug=False, threaded=True)