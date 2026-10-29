"""אינדיקטורים טכניים טהורים (בלי רשת). ברים: dict עם המפתחות t,o,h,l,c,v (פורמט Alpaca)."""

def sma(vals, n):
    return sum(vals[-n:]) / n if len(vals) >= n else None

def rsi(closes, n=14):
    if len(closes) < n + 1:
        return None
    gains = [max(closes[i] - closes[i - 1], 0) for i in range(1, len(closes))]
    losses = [max(closes[i - 1] - closes[i], 0) for i in range(1, len(closes))]
    ag, al = sum(gains[:n]) / n, sum(losses[:n]) / n
    for g, l in zip(gains[n:], losses[n:]):
        ag, al = (ag * (n - 1) + g) / n, (al * (n - 1) + l) / n
    if al == 0:
        return 100.0
    return 100 - 100 / (1 + ag / al)

def atr(bars, n=14):
    if len(bars) < n + 1:
        return None
    trs = [max(b["h"] - b["l"], abs(b["h"] - p["c"]), abs(b["l"] - p["c"])) for p, b in zip(bars, bars[1:])]
    a = sum(trs[:n]) / n
    for tr in trs[n:]:
        a = (a * (n - 1) + tr) / n
    return a

def vwap(bars):
    pv = sum((b["h"] + b["l"] + b["c"]) / 3 * b["v"] for b in bars)
    v = sum(b["v"] for b in bars)
    return pv / v if v else None

def vol_spike(bars, recent=3, base=20):
    """ממוצע נפח של הברים האחרונים מול ממוצע הבסיס שלפניהם"""
    if len(bars) < recent + base:
        return None
    r = sum(b["v"] for b in bars[-recent:]) / recent
    b0 = sum(b["v"] for b in bars[-recent - base:-recent]) / base
    return r / b0 if b0 else None
