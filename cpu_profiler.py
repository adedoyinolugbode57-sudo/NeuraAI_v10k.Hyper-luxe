"""
cpu_profiler.py
Profiles CPU, memory, and system stats.
"""

import psutil

def profile_system() -> dict:
    """
    Returns CPU, RAM, and Disk usage statistics.
    """
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_count": psutil.cpu_count(logical=True),
        "ram_percent": psutil.virtual_memory().percent,
        "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "disk_percent": psutil.disk_usage("/").percent,
        "disk_total_gb": round(psutil.disk_usage("/").total / (1024**3), 2)
    }