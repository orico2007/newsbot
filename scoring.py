"""ציון מפגש (Confluence): כמה סימנים שונים מסכימים. הציון קובע אם נכנסים וכמה גדול."""

def confluence(sig_quality, align, volume_ok, news_score=None, news_dir_ok=None, fund_ok=None, rs=0.0):
    pts = 55 * sig_quality
    pts += 20 * max(-1, min(1, align))
    pts += 10 if volume_ok else 0
    if news_score is not None and news_dir_ok: pts += 4 * max(0, news_score - 5)      # 8→12, 10→20
    if news_score is not None and news_dir_ok is False: pts -= 15
    if fund_ok is True: pts += 8
    if fund_ok is False: pts -= 12
    pts += max(-5, min(5, rs / 4))
    return round(max(0, min(100, pts)), 1)

def size_mult(score, lo=0.5, hi=1.5, floor=40, top=85):
    if score <= floor: return lo
    if score >= top: return hi
    return round(lo + (hi - lo) * (score - floor) / (top - floor), 2)
