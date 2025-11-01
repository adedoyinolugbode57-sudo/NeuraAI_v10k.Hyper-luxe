# Neuraluxe-AI Hyperluxe — Deployment Guide (quick)

Prereqs:
- Git repo with project root
- Render account (or any host that supports Gunicorn + Python)
- Set environment variables in Render per render.yaml or .env (do NOT commit real keys)

Steps (Render):
1. Push repo to GitHub.
2. Create a new Web Service on Render and connect your repo.
3. Use the provided `render.yaml` or configure:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn main:app --workers=4 --threads=4 --timeout=120`
4. Set environment vars in Render dashboard:
   - `DATABASE_URL` (Render DB or external).
   - `SECRET_KEY` (generated or your own).
   - `NEURA_ADMIN_TOKEN` (generated).
   - `OPENAI_API_KEY` if using OpenAI.
   - `REDIS_URL` if you use redis/worker.
5. Deploy. Watch the logs for errors.

Local quick run:
- Create `.env` from `.env.sample` and set values.
- Install: `pip install -r requirements.txt`
- Run dev: `python main.py` (or `gunicorn main:app` for production)

Notes:
- If using heavy local models (transformers + torch), choose a host/instance with GPUs & sufficient RAM.
- For scale: use a Redis-backed job queue and an autoscaled worker fleet; move static files to S3/cdn.