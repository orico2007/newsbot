"""Mean-reversion long rules found by the systematic sweep (sweep*.py, portfolio_test*.py).
Rule A: uptrend (close > SMA50 > SMA200), RSI(2) < 5 and IBS < 0.25, ATR% < 4.
Rule E: uptrend, RSI(2) < 10 and close < SMA20 - 1.5 ATR, price >= 15.
Exit: close above the prior day's high (or time stop / ATR stop). Long only, bull market only."""
from patterns import Signal

RULES = {"mr_A": {"rank": 90}, "mr_E": {"rank": 65}}

def _rsi(c, n=2):
    if len(c) <= n: return None
    g = l = 0.0
    for i in range(1, n + 1):
        d = c[i] - c[i - 1]; g += max(d, 0); l += max(-d, 0)
    ag, al = g / n, l / n
    for i in range(n + 1, len(c)):
        d = c[i] - c[i - 1]
        ag = (ag * (n - 1) + max(d, 0)) / n; al = (al * (n - 1) + max(-d, 0)) / n
    return 100 - 100 / (1 + ag / al) if al > 0 else 100.0

def _sma(x, n): return sum(x[-n:]) / n if len(x) >= n else None

def _atr(bars, n=14):
    tr = [bars[0]["h"] - bars[0]["l"]] + [max(b["h"] - b["l"], abs(b["h"] - bars[i]["c"]), abs(b["l"] - bars[i]["c"])) for i, b in enumerate(bars[1:])]
    a = sum(tr[:n]) / n
    for x in tr[n:]: a = (a * (n - 1) + x) / n
    return a

def detect(daily, stop_atr=4.0):
    """returns a Signal (long) when rule A or E fires on the last bar, else None"""
    if len(daily) < 205: return None
    c = [b["c"] for b in daily]; b = daily[-1]; px = c[-1]
    s20, s50, s200 = _sma(c, 20), _sma(c, 50), _sma(c, 200)
    r2 = _rsi(c); atr = _atr(daily)
    if None in (s20, s50, s200, r2) or not atr or not (px > s50 > s200): return None
    ibs = (px - b["l"]) / (b["h"] - b["l"]) if b["h"] > b["l"] else 0.5
    name = None
    if r2 < 5 and ibs < 0.25 and atr / px * 100 < 4: name = "mr_A"
    elif r2 < 10 and px < s20 - 1.5 * atr and px >= 15: name = "mr_E"
    if not name: return None
    return Signal(name, "long", "swing", px, px - stop_atr * atr, px + 8 * atr, quality=0.7,
                  notes=f"RSI2={r2:.1f} IBS={ibs:.2f} uptrend pullback", volume_ok=False)

def exit_now(daily):
    """True when the last (today's, near-final) close is above the prior day's high"""
    return len(daily) >= 2 and daily[-1]["c"] > daily[-2]["h"]
