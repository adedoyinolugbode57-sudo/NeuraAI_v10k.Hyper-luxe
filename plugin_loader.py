"""
plugin_loader.py
Load and manage external AI plugins.
"""

LOADED_PLUGINS = []

def load_plugin(plugin_name: str):
    LOADED_PLUGINS.append(plugin_name)
    return f"Plugin {plugin_name} loaded."