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

def avg(vals):
    vals = list(vals)
    return sum(vals) / len(vals) if vals else 0.0

def stdev(vals):
    vals = list(vals)
    if len(vals) < 2: return 0.0
    m = sum(vals) / len(vals)
    return (sum((v - m) ** 2 for v in vals) / len(vals)) ** 0.5

def bollinger(closes, n=20, k=2.0):
    """(mid, upper, lower, width%) של הבר האחרון"""
    if len(closes) < n: return None
    w = closes[-n:]; m = sum(w) / n; sd = stdev(w)
    return m, m + k * sd, m - k * sd, (2 * k * sd) / m * 100

def pct_return(closes, n):
    if len(closes) <= n or closes[-n - 1] == 0: return None
    return (closes[-1] / closes[-n - 1] - 1) * 100

def ema(vals, n):
    if len(vals) < n: return None
    k = 2 / (n + 1); e = sum(vals[:n]) / n
    for v in vals[n:]: e = v * k + e * (1 - k)
    return e

def adx(bars, n=14):
    """Wilder ADX: עוצמת מגמה (מעל ~20 = מגמה אמיתית)"""
    if len(bars) < 2 * n + 1: return None
    tr, pdm, mdm = [], [], []
    for p, b in zip(bars, bars[1:]):
        up, dn = b["h"] - p["h"], p["l"] - b["l"]
        pdm.append(up if up > dn and up > 0 else 0.0); mdm.append(dn if dn > up and dn > 0 else 0.0)
        tr.append(max(b["h"] - b["l"], abs(b["h"] - p["c"]), abs(b["l"] - p["c"])))
    def smooth(x):
        s = sum(x[:n]); out = [s]
        for v in x[n:]: s = s - s / n + v; out.append(s)
        return out
    st, sp, sm = smooth(tr), smooth(pdm), smooth(mdm)
    dx = []
    for t, p, m in zip(st, sp, sm):
        if t == 0: dx.append(0.0); continue
        pi, mi = 100 * p / t, 100 * m / t
        dx.append(100 * abs(pi - mi) / (pi + mi) if pi + mi else 0.0)
    if len(dx) < n: return None
    a = sum(dx[:n]) / n
    for v in dx[n:]: a = (a * (n - 1) + v) / n
    return a

def keltner(bars, n=20, mult=1.5):
    """(mid, upper, lower) סביב SMA20 עם ATR"""
    if len(bars) < n + 1: return None
    mid = sum(b["c"] for b in bars[-n:]) / n; a = atr(bars) or 0
    return mid, mid + mult * a, mid - mult * a

def ibs(b):
    """Internal Bar Strength: איפה הסגירה בטווח הנר (0=בשפל, 1=בשיא)"""
    r = b["h"] - b["l"]
    return (b["c"] - b["l"]) / r if r > 0 else 0.5
