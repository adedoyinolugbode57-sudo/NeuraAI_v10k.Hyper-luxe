TREND_DB = {}

def add_keyword(keyword: str):
    TREND_DB[keyword] = TREND_DB.get(keyword, 0) + 1

def top_trends(n: int = 5):
    return sorted(TREND_DB.items(), key=lambda x: -x[1])[:n]