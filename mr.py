"""Mean-reversion long rules found by the systematic sweep (sweep*.py, portfolio_test*.py).
Rule A: uptrend (close > SMA50 > SMA200), RSI(2) < 5 and IBS < 0.25, ATR% < 4.
Rule E: uptrend, RSI(2) < 10 and close < SMA20 - 1.5 ATR, price >= 15.
Rule F: uptrend, RSI(2) < 5, no 3-day crash (3d return > -12%).
Exit: close above the prior day's high (or time stop / ATR stop). Long only, bull market only."""
from patterns import Signal

RULES = {"mr_A": {"rank": 90}, "mr_E": {"rank": 65}, "mr_F": {"rank": 60}}

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
    if not name and r2 < 5 and len(c) > 3 and (px / c[-4] - 1) * 100 > -12: name = "mr_F"
    if not name: return None
    return Signal(name, "long", "swing", px, px - stop_atr * atr, px + 8 * atr, quality=0.7,
                  notes=f"RSI2={r2:.1f} IBS={ibs:.2f} uptrend pullback", volume_ok=False)

def exit_now(daily):
    """True when the last (today's, near-final) close is above the prior day's high"""
    return len(daily) >= 2 and daily[-1]["c"] > daily[-2]["h"]


def vol60(daily):
    """Standard deviation (in %) of the last 60 daily returns, up to and including the signal day. None if too little history."""
    c = [b["c"] for b in daily]
    if len(c) < 61: return None
    r = [c[j] / c[j - 1] - 1 for j in range(len(c) - 60, len(c))]
    m = sum(r) / 60
    return (sum((x - m) ** 2 for x in r) / 59) ** 0.5 * 100


def zreg(daily, n=20):
    """Regression-residual z-score: how far (in residual std devs) the last close sits below the least-squares line through the last n closes.
    Strongly negative = a real washout versus trend. None if too little history."""
    c = [b["c"] for b in daily][-n:]
    if len(c) < n: return None
    mx = (n - 1) / 2; my = sum(c) / n
    sxx = sum((a - mx) ** 2 for a in range(n))
    slope = sum((a - mx) * (y - my) for a, y in zip(range(n), c)) / sxx
    res = [y - (my + slope * (a - mx)) for a, y in zip(range(n), c)]
    mean = sum(res) / n; sd = (sum((r - mean) ** 2 for r in res) / n) ** 0.5
    return res[-1] / sd if sd else 0.0


def disp_pct(bars_by_sym, window=250):
    """Trailing percentile of today's cross-sectional stdev of 1d returns versus the previous `window` days (None if < 60 days of history)."""
    R = {}
    for daily in bars_by_sym.values():
        for i in range(1, len(daily)):
            R.setdefault(daily[i]["t"][:10], []).append(daily[i]["c"] / daily[i - 1]["c"] - 1)
    D = {d: _pstdev(v) * 100 for d, v in R.items() if len(v) >= 30}
    ds = sorted(D)
    if len(ds) < 61: return None
    w = [D[x] for x in ds[-1 - window:-1]]
    return sum(1 for x in w if x < D[ds[-1]]) / len(w)

def _pstdev(v):
    m = sum(v) / len(v)
    return (sum((x - m) ** 2 for x in v) / len(v)) ** 0.5

def tilt_multiplier(bars_by_sym, spy, hi=1.25, lo=0.75, clip=(0.5, 1.5)):
    """Market-state size tilt (lab runs 58-61, walk-forward audited): product of three 1.25x/0.75x flags, clipped to 0.5-1.5.
    flags: cross-stock dispersion percentile >= 0.5; SPY close location in its day range (IBS) < 0.3; SPY volume >= 1.1 x its prior-20-day mean.
    Returns (multiplier, description). Missing data counts as a False flag (0.75x)."""
    flags = []
    p = disp_pct(bars_by_sym); flags.append(("dispersion", p is not None and p >= 0.5, p))
    ibs = None
    if spy:
        r = spy[-1]["h"] - spy[-1]["l"]; ibs = (spy[-1]["c"] - spy[-1]["l"]) / r if r else 0.5
    flags.append(("SPY IBS", ibs is not None and ibs < 0.3, ibs))
    vr = None
    if spy and len(spy) > 20:
        a = [b.get("v") for b in spy[-21:-1]]
        if all(a) and spy[-1].get("v"): vr = spy[-1]["v"] / (sum(a) / 20)
    flags.append(("SPY volume ratio", vr is not None and vr >= 1.1, vr))
    m = 1.0
    for _, on, _ in flags: m *= hi if on else lo
    m = max(clip[0], min(clip[1], m))
    desc = ", ".join(f"{n} {'hi' if on else 'lo'}" + (f" {v:.2f}" if v is not None else "") for n, on, v in flags)
    return round(m, 3), desc
