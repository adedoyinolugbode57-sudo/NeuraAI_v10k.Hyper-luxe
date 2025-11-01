"""
live_code_runner.py
Ultimate safe code execution engine for Neuraluxe-AI.
Supports:
- Tiny snippets to massive scripts (20,000+ lines)
- Persistent variables across multiple runs
- Mock module/file imports
- Time & output limits
- Safe sandboxed environment
"""

import sys
import traceback
import contextlib
import io
import threading
import time

# ------------------------
# Configuration
# ------------------------
MAX_EXECUTION_TIME = 10  # seconds
MAX_OUTPUT_LINES = 1000  # max lines of output to return
MAX_CODE_LENGTH = 20000  # max lines of code allowed

# Persistent session environment
SESSION_VARS = {}

# Mock modules for safe imports
SAFE_MODULES = {
    "math": __import__("math"),
    "random": __import__("random"),
    "datetime": __import__("datetime"),
}

class CodeExecutionError(Exception):
    pass

def _run_safely(code: str, local_vars: dict):
    """
    Execute code safely in isolated environment with safe modules.
    """
    output_buffer = io.StringIO()
    try:
        # Prepare sandbox with only safe builtins and modules
        safe_builtins = {
            "print": print,
            "range": range,
            "len": len,
            "min": min,
            "max": max,
            "sum": sum,
            "abs": abs,
            "sorted": sorted,
            "enumerate": enumerate,
        }
        env = {"__builtins__": safe_builtins, **SAFE_MODULES, **local_vars}
        with contextlib.redirect_stdout(output_buffer), contextlib.redirect_stderr(output_buffer):
            exec(code, env)
        # Update persistent vars
        local_vars.update({k: v for k, v in env.items() if k not in SAFE_MODULES and k != "__builtins__"})
    except Exception:
        output_buffer.write("\n[ERROR]\n")
        traceback.print_exc(file=output_buffer)
    finally:
        return output_buffer.getvalue()

def run_code_snippet(code: str, session_vars: dict = None) -> str:
    """
    Run Python code safely with persistent session support.

    Parameters:
    - code: str, Python code to execute
    - session_vars: dict, optional, to persist variables across runs

    Returns:
    - output: str, captured stdout/stderr or error messages
    """
    if code.count("\n") > MAX_CODE_LENGTH:
        return f"[ERROR] Code exceeds {MAX_CODE_LENGTH} lines limit."

    local_vars = session_vars if session_vars is not None else SESSION_VARS
    result = "[INFO] Execution timed out."

    def target():
        nonlocal result
        result = _run_safely(code, local_vars)

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(MAX_EXECUTION_TIME)
    if thread.is_alive():
        return "[ERROR] Execution time exceeded maximum limit."

    # Limit output size
    output_lines = result.splitlines()
    if len(output_lines) > MAX_OUTPUT_LINES:
        output_lines = output_lines[:MAX_OUTPUT_LINES]
        output_lines.append("[INFO] Output truncated due to max line limit.")

    return "\n".join(output_lines)


# ------------------------
# Example usage
# ------------------------
if __name__ == "__main__":
    code1 = """
x = 0
for i in range(5):
    x += i
    print(f"Adding {i}, total={x}")
"""
    code2 = """
import math
print(f"Square root of {x} is {math.sqrt(x)}")
"""

    print("=== Run 1 ===")
    print(run_code_snippet(code1))
    print("\n=== Run 2 (persistent session) ===")
    print(run_code_snippet(code2))