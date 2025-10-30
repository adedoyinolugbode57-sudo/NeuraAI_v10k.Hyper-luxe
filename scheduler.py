# ==============================================================
# 💎 Neuraluxe-AI — scheduler.py
# Smart AI Task Planner, Reminder, and Scheduler Engine
# Compatible with Flask + JSON (No external DB required)
# ==============================================================

import json
import os
import time
import threading
import random
from datetime import datetime, timedelta
import pyttsx3

SCHEDULE_FILE = "neuraluxe_schedule.json"
VOICE_ALERTS = True   # Set False if you don't want speech output

# --- Voice Engine ---
engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("voice", engine.getProperty("voices")[0].id)

# --- Load / Save Helpers ---
def load_schedules():
    if not os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, "w") as f:
            json.dump({"tasks": []}, f, indent=4)
    with open(SCHEDULE_FILE, "r") as f:
        return json.load(f)

def save_schedules(data):
    with open(SCHEDULE_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- Smart AI Priority Generator ---
def get_priority_level(task_name):
    critical_words = ["urgent", "meeting", "exam", "deadline", "project"]
    if any(w in task_name.lower() for w in critical_words):
        return "High"
    elif any(w in task_name.lower() for w in ["call", "review", "update"]):
        return "Medium"
    else:
        return "Low"

# --- Add Task ---
def add_task(title, description, due_in_minutes):
    schedules = load_schedules()
    due_time = datetime.utcnow() + timedelta(minutes=due_in_minutes)
    priority = get_priority_level(title)

    task = {
        "id": f"tsk_{random.randint(1000,9999)}",
        "title": title,
        "description": description,
        "created_at": datetime.utcnow().isoformat(),
        "due_time": due_time.isoformat(),
        "priority": priority,
        "status": "Pending"
    }

    schedules["tasks"].append(task)
    save_schedules(schedules)
    speak(f"New {priority} priority task added — {title}")
    return task

# --- Speak Helper ---
def speak(text):
    if VOICE_ALERTS:
        engine.say(text)
        engine.runAndWait()

# --- Mark Task Complete ---
def complete_task(task_id):
    schedules = load_schedules()
    for task in schedules["tasks"]:
        if task["id"] == task_id:
            task["status"] = "Completed"
            task["completed_at"] = datetime.utcnow().isoformat()
            speak(f"Task {task['title']} marked complete.")
            save_schedules(schedules)
            return task
    return None

# --- Delete Task ---
def delete_task(task_id):
    schedules = load_schedules()
    new_list = [t for t in schedules["tasks"] if t["id"] != task_id]
    schedules["tasks"] = new_list
    save_schedules(schedules)
    speak(f"Task {task_id} removed.")
    return True

# --- List All Tasks ---
def list_tasks(show_completed=False):
    schedules = load_schedules()
    if show_completed:
        return schedules["tasks"]
    else:
        return [t for t in schedules["tasks"] if t["status"] != "Completed"]

# --- Check Deadlines (Auto Reminder Loop) ---
def reminder_loop():
    while True:
        schedules = load_schedules()
        now = datetime.utcnow()
        for task in schedules["tasks"]:
            if task["status"] == "Pending":
                due_time = datetime.fromisoformat(task["due_time"])
                remaining = (due_time - now).total_seconds()
                if 0 < remaining < 120:
                    speak(f"Reminder: Task {task['title']} is due soon.")
                elif remaining <= 0:
                    speak(f"Alert! Task {task['title']} deadline reached.")
                    task["status"] = "Overdue"
        save_schedules(schedules)
        time.sleep(60)  # Check every minute

# --- Start Background Thread ---
def start_scheduler():
    threading.Thread(target=reminder_loop, daemon=True).start()
    speak("Neuraluxe Scheduler activated.")

# --- Sample Startup Test ---
if __name__ == "__main__":
    start_scheduler()
    add_task("Finish Neuraluxe Docs", "Prepare README for final upload", 1)
    time.sleep(5)
    print(list_tasks())