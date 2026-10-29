"""ריבוי טווחי זמן: שבועי (מגמה ראשית + תבניות), 15 דקות (מתוך 5), והתנגדות/תמיכה יומית לעסקאות יום."""
from datetime import datetime
from indicators import sma
from structure import trend_structure, key_levels

def _week_key(t):
    d = datetime.fromisoformat(str(t).replace("Z", "+00:00"))
    y, w, _ = d.isocalendar()
    return (y, w)

def resample_weekly(daily):
    """נרות יומיים -> שבועיים (פתיחה ראשונה, שיא/שפל, סגירה אחרונה, נפח מצטבר)"""
    out, cur, key = [], None, None
    for b in daily:
        try: k = _week_key(b["t"])
        except Exception: k = None
        if k != key or cur is None:
            if cur: out.append(cur)
            cur, key = {"t": b.get("t"), "o": b["o"], "h": b["h"], "l": b["l"], "c": b["c"], "v": b["v"]}, k
        else:
            cur["h"] = max(cur["h"], b["h"]); cur["l"] = min(cur["l"], b["l"]); cur["c"] = b["c"]; cur["v"] += b["v"]
    if cur: out.append(cur)
    return out

def resample_n(bars, n):
    """מקבץ n נרות רצופים לנר אחד (5 דקות -> 15 דקות עם n=3). נר חלקי בסוף נשמר רק אם מלא"""
    out = []
    for i in range(0, len(bars) - n + 1, n):
        g = bars[i:i + n]
        out.append({"t": g[0].get("t"), "o": g[0]["o"], "h": max(x["h"] for x in g), "l": min(x["l"] for x in g), "c": g[-1]["c"], "v": sum(x["v"] for x in g)})
    return out

def weekly_trend(daily):
    """up / down / range לפי SMA10 שבועי ומבנה שיאים-שפלים; None אם אין מספיק נתונים"""
    w = resample_weekly(daily)
    if len(w) < 15: return None
    closes = [b["c"] for b in w]
    s10 = sma(closes, 10)
    st = trend_structure(w, 2, 2)["trend"]
    if closes[-1] > s10 and st != "down": return "up"
    if closes[-1] < s10 and st != "up": return "down"
    return "range"

def htf_points(daily, side):
    """+1 כשהטווח השבועי מסכים עם הצד, -1 כשהוא נגדו, 0 אם ניטרלי/לא ידוע"""
    t = weekly_trend(daily)
    if t is None or t == "range": return 0.0
    return 1.0 if (t == "up") == (side == "long") else -1.0

def near_level(daily, price, side, pct=1.0):
    """עסקת יום לונג ממש מתחת להתנגדות יומית (או שורט ממש מעל תמיכה). מחזיר את הרמה או None"""
    for lv in key_levels(daily, min_touches=3):
        p = lv["price"]
        if side == "long" and 0 < (p - price) / price * 100 <= pct: return p
        if side == "short" and 0 < (price - p) / price * 100 <= pct: return p
    return None
