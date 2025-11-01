"""
pagination.py
Helper for paginating lists.
"""

def paginate(items: list, page: int = 1, per_page: int = 10) -> list:
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end]