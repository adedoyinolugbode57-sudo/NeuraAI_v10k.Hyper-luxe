"""
ad_tracker.py
Tracks ad impressions and clicks.
"""
def track_ad(ad_id: str, clicks: int, impressions: int) -> str:
    ctr = (clicks / impressions * 100) if impressions else 0
    return f"Ad {ad_id}: CTR={ctr:.2f}%"