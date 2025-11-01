"""
queue_utils.py
Independent queue utilities for Neuraluxe-AI.
"""
import queue

job_queue = queue.Queue()

def add_job(fn, *args, **kwargs):
    job_queue.put((fn, args, kwargs))

def process_jobs():
    while not job_queue.empty():
        fn, args, kwargs = job_queue.get()
        fn(*args, **kwargs)
        job_queue.task_done()"""
queue_utils.py
Independent queue utilities for Neuraluxe-AI.
"""
import queue

job_queue = queue.Queue()

def add_job(fn, *args, **kwargs):
    job_queue.put((fn, args, kwargs))

def process_jobs():
    while not job_queue.empty():
        fn, args, kwargs = job_queue.get()
        fn(*args, **kwargs)
        job_queue.task_done()