import time

TASKS = []

def schedule_task(task_name: str, delay_sec: int):
    TASKS.append((task_name, time.time() + delay_sec))

def get_due_tasks():
    import time
    now = time.time()
    due = [t for t in TASKS if t[1] <= now]
    TASKS[:] = [t for t in TASKS if t[1] > now]
    return [t[0] for t in due]
    def schedule_task(task_name: str, time: str) -> str:
    return f"Task '{task_name}' scheduled at {time}"