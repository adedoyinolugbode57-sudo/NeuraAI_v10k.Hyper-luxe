import importlib
import os
from flask import Blueprint

def register_all_blueprints(app):
    """Auto-register all blueprints in the current directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))

    for filename in os.listdir(current_dir):
        if filename.endswith(".py") and filename not in ["main.py", "__init__.py", "auto_register.py"]:
            module_name = filename[:-3]
            try:
                module = importlib.import_module(module_name)
                for item in dir(module):
                    obj = getattr(module, item)
                    if isinstance(obj, Blueprint):
                        app.register_blueprint(obj, url_prefix=f"/{module_name}")
                        print(f"✅ Registered blueprint from: {filename}")
            except Exception as e:
                print(f"⚠️ Skipped {filename}: {e}")