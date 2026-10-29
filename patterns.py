"""גלאי תבניות (ימי). כל גלאי כתוב ללונג; שורט = אותו גלאי על גרף הפוך (מראה 1/מחיר)."""
from dataclasses import dataclass
from indicators import sma, rsi, atr, avg, bollinger, stdev, vwap
from structure import pivots, trend_structure, key_levels, fib_levels

@dataclass
class Signal:
    name: str
    side: str            # long | short
    kind: str            # swing | day
    price: float
    stop: float
    target: float
    quality: float = 0.6
    notes: str = ""
    volume_ok: bool = False

# ---------- מראה: שורט = לונג על גרף הפוך ----------
def mirror(bars):
    k2 = bars[-1]["c"] ** 2
    return [{"t": b.get("t"), "o": k2 / b["o"], "h": k2 / b["l"], "l": k2 / b["h"], "c": k2 / b["c"], "v": b["v"]} for b in bars], k2

CANDLE_MIRROR = {"hammer": "shooting_star", "bullish_engulfing": "bearish_engulfing", "inverted_hammer": "hanging_man"}

def unmirror(sig, k2):
    sig.price, sig.stop, sig.target = k2 / sig.price, k2 / sig.stop, k2 / sig.target
    sig.side = "short"
    for a, b in CANDLE_MIRROR.items(): sig.notes = sig.notes.replace(a, b)
    return sig

# ---------- נרות ----------
def _parts(b):
    body = abs(b["c"] - b["o"]); rng = b["h"] - b["l"]
    return body, rng, b["h"] - max(b["o"], b["c"]), min(b["o"], b["c"]) - b["l"]

def bull_candle(bars):
    """נר היפוך שורי בבר האחרון: hammer / bullish_engulfing / inverted_hammer מאושר"""
    if len(bars) < 3: return None
    b, p = bars[-1], bars[-2]
    body, rng, up, low = _parts(b)
    if rng <= 0: return None
    if low >= 2 * max(body, rng * 0.03) and up <= 0.35 * max(body, rng * 0.05) + 0.1 * rng and min(b["o"], b["c"]) >= b["l"] + 0.6 * rng:
        return "hammer"
    pb = abs(p["c"] - p["o"])
    if p["c"] < p["o"] and b["c"] > b["o"] and b["c"] >= p["o"] and b["o"] <= p["c"] and body > pb:
        return "bullish_engulfing"
    pbody, prng, pup, plow = _parts(p)
    if prng > 0 and pup >= 2 * max(pbody, prng * 0.03) and plow <= 0.1 * prng and b["c"] > p["h"]:
        return "inverted_hammer"
    return None

def is_doji(b):
    body, rng, _, _ = _parts(b)
    return rng > 0 and body <= 0.1 * rng

def _vavg(bars, n=20):
    return avg(b["v"] for b in bars[-n - 1:-1]) if len(bars) > 2 else 0

# ---------- דגל (flag) ----------
def flag_long(bars, min_pole_pct=12, max_pole=12, min_flag=3, max_flag=10):
    n = len(bars)
    if n < 40: return None
    last, best = bars[-1], None
    for L in range(min_flag, max_flag + 1):
        fs = n - 1 - L
        flag = bars[fs:n - 1]
        fh, fl = max(b["h"] for b in flag), min(b["l"] for b in flag)
        for P in range(3, max_pole + 1):
            ps = fs - P
            if ps < 0: break
            pole = bars[ps:fs]
            lo0, hi1 = min(b["l"] for b in pole), max(b["h"] for b in pole)
            i_lo = min(range(P), key=lambda k: pole[k]["l"]); i_hi = max(range(P), key=lambda k: pole[k]["h"])
            height = hi1 - lo0
            if i_lo >= i_hi or i_hi < P - 2 or height / lo0 * 100 < min_pole_pct: continue
            if (fh - fl) > 0.45 * height or fl < lo0 + 0.5 * height or fh > hi1 * 1.03: continue
            pv, fv = avg(b["v"] for b in pole), avg(b["v"] for b in flag)
            if fv >= pv: continue
            if not (fh < last["c"] <= fh * 1.03): continue
            q = 0.7 + (0.1 if last["v"] >= 1.3 * fv else 0) + (0.05 if fv < 0.7 * pv else 0)
            cand = Signal("flag", "long", "swing", last["c"], fl * 0.995, fh + height, q,
                          f"pole {height / lo0 * 100:.0f}% flag {L}d", last["v"] >= 1.3 * fv)
            if best is None or height / lo0 > best[0]: best = (height / lo0, cand)
    return best[1] if best else None

# ---------- בסיס + פריצה בנפח ----------
def base_breakout_long(bars, max_range_pct=14, min_len=15, max_len=60):
    n = len(bars)
    if n < min_len + 25: return None
    last, a = bars[-1], atr(bars) or 0
    for B in range(min(max_len, n - 2), min_len - 1, -1):
        base = bars[-B - 1:-1]
        bh, bl = max(b["h"] for b in base), min(b["l"] for b in base)
        if (bh - bl) / bl * 100 > max_range_pct: continue
        bv = avg(b["v"] for b in base)
        if not (bh < last["c"] <= bh * 1.04) or last["v"] < 1.5 * bv: continue
        dry = avg(b["v"] for b in base[-8:]) <= 0.9 * bv
        stop = max(bl, bh - 2 * a) if a else bl
        q = 0.65 + (0.15 if dry else 0) + (0.1 if last["v"] >= 2 * bv else 0)
        return Signal("base_breakout", "long", "swing", last["c"], stop, bh + (bh - bl), q, f"base {B}d range {((bh - bl) / bl * 100):.0f}%", True)
    return None

# ---------- תחתית כפולה (W) ----------
def double_bottom_long(bars, tol=3.0, min_sep=8, max_sep=50, min_depth=6.0):
    n = len(bars)
    if n < 40: return None
    seg = bars[-140:]; off = n - len(seg)
    lows = [p for p in pivots(seg) if p[2] == "L"]
    last, a, va = bars[-1], atr(bars) or 0, _vavg(bars)
    for ai in range(len(lows) - 2, -1, -1):
        A, C = lows[ai], lows[-1]
        if C is A: continue
        sep = C[0] - A[0]
        if not (min_sep <= sep <= max_sep) or abs(A[1] - C[1]) / A[1] * 100 > tol: continue
        mid = seg[A[0]:C[0] + 1]
        B = max(b["h"] for b in mid); lo = min(A[1], C[1])
        if (B - lo) / lo * 100 < min_depth: continue
        if not (B < last["c"] <= B * 1.05) or last["v"] < 1.1 * va: continue
        if any(b["c"] > B for b in seg[C[0] + 1:-3]): continue      # פריצה טרייה
        return Signal("double_bottom", "long", "swing", last["c"], lo - 0.25 * a, B + (B - lo),
                      0.7 + (0.1 if C[1] >= A[1] else 0), f"W A={A[1]:.2f} C={C[1]:.2f} neck={B:.2f}", True)
    return None

# ---------- ראש וכתפיים הפוך ----------
def inverse_hs_long(bars):
    n = len(bars)
    if n < 50: return None
    seg = bars[-160:]
    lows = [p for p in pivots(seg) if p[2] == "L"]
    if len(lows) < 3: return None
    ls, h, rs = lows[-3:]
    last, a, va = bars[-1], atr(bars) or 0, _vavg(bars)
    if not (h[1] < ls[1] * 0.98 and h[1] < rs[1] * 0.98 and abs(ls[1] - rs[1]) / ls[1] <= 0.05): return None
    if h[0] - ls[0] < 4 or rs[0] - h[0] < 4: return None
    p1 = max(b["h"] for b in seg[ls[0]:h[0] + 1]); p2 = max(b["h"] for b in seg[h[0]:rs[0] + 1])
    if abs(p1 - p2) / p1 > 0.04: return None
    neck = (p1 + p2) / 2
    if not (neck < last["c"] <= neck * 1.05) or last["v"] < 1.0 * va: return None
    if any(b["c"] > neck for b in seg[rs[0] + 1:-3]): return None
    return Signal("inverse_head_shoulders", "long", "swing", last["c"], rs[1] - 0.25 * a, neck + (neck - h[1]), 0.7,
                  f"H={h[1]:.2f} neck={neck:.2f}", last["v"] >= 1.3 * va)

# ---------- משולשים ----------
def _tri_points(bars, window=70):
    seg = bars[-window:]
    piv = pivots(seg, 2, 2)
    return seg, [p for p in piv if p[2] == "H"], [p for p in piv if p[2] == "L"]

def ascending_triangle_long(bars):
    if len(bars) < 40: return None
    seg, hs, ls = _tri_points(bars)
    if len(hs) < 2 or len(ls) < 2 or len(hs) + len(ls) < 5: return None
    prices = [h[1] for h in hs]; res = avg(prices)
    if (max(prices) - min(prices)) / res > 0.015: return None
    lp = [l[1] for l in ls]
    if not all(lp[i] < lp[i + 1] for i in range(len(lp) - 1)) or (lp[-1] - lp[0]) / lp[0] < 0.02: return None
    last, a, va = bars[-1], atr(bars) or 0, _vavg(bars)
    if not (res * 1.002 < last["c"] <= res * 1.04) or last["v"] < 1.1 * va: return None
    if any(b["c"] > res * 1.003 for b in seg[hs[-1][0] + 1:-1]): return None
    return Signal("ascending_triangle", "long", "swing", last["c"], lp[-1] - 0.25 * a, res + (res - lp[0]), 0.7,
                  f"touches={len(hs) + len(ls)} res={res:.2f}", True)

def symmetrical_triangle_up(bars):
    if len(bars) < 40: return None
    seg, hs, ls = _tri_points(bars)
    if len(hs) < 2 or len(ls) < 2 or len(hs) + len(ls) < 5: return None
    hp, lp = [h[1] for h in hs], [l[1] for l in ls]
    if not (all(hp[i] > hp[i + 1] for i in range(len(hp) - 1)) and all(lp[i] < lp[i + 1] for i in range(len(lp) - 1))): return None
    (i1, p1), (i2, p2) = (hs[-2][0], hs[-2][1]), (hs[-1][0], hs[-1][1])
    slope = (p2 - p1) / (i2 - i1)
    line = p2 + slope * (len(seg) - 1 - i2)
    last, a, va = bars[-1], atr(bars) or 0, _vavg(bars)
    if not (line * 1.002 < last["c"] <= line * 1.04) or last["v"] < 1.1 * va: return None
    return Signal("symmetrical_triangle", "long", "swing", last["c"], lp[-1] - 0.25 * a, last["c"] + (hp[0] - lp[0]), 0.6,
                  f"touches={len(hs) + len(ls)}", True)

# ---------- גאפים ----------
def gap_breakaway_long(bars, min_gap=2.5):
    n = len(bars)
    if n < 30: return None
    b, p = bars[-1], bars[-2]
    gap = (b["o"] / p["c"] - 1) * 100
    if gap < min_gap or b["c"] <= p["c"] or b["c"] < b["o"]: return None
    base = bars[-27:-1]
    bh, bl = max(x["h"] for x in base), min(x["l"] for x in base)
    if (bh - bl) / bl * 100 > 18 or p["c"] < bh * 0.97: return None
    va = _vavg(bars)
    if b["v"] < 2 * va: return None
    a = atr(bars) or 0
    stop = (b["l"] - 0.1 * a) if b["l"] > p["c"] else p["c"]
    return Signal("breakaway_gap", "long", "swing", b["c"], stop, b["c"] + (bh - bl), 0.7 + (0.1 if gap >= 5 else 0),
                  f"gap {gap:.1f}% vol {b['v'] / va:.1f}x", True)

def gap_runaway_long(bars, min_gap=2.0):
    n = len(bars)
    if n < 60: return None
    b, p = bars[-1], bars[-2]
    gap = (b["o"] / p["c"] - 1) * 100
    if gap < min_gap or b["c"] < b["o"] or b["c"] <= p["c"]: return None
    if trend_structure(bars[:-1])["trend"] != "up" or b["v"] < 1.5 * _vavg(bars): return None
    a = atr(bars) or 0
    return Signal("runaway_gap", "long", "swing", b["c"], b["l"] - 0.1 * a, b["c"] + 3 * a, 0.55, f"gap {gap:.1f}% mid-trend", True)

def island_bottom_long(bars, max_island=6, min_gap=1.5):
    n = len(bars)
    if n < 30: return None
    i_up = n - 1
    if (bars[i_up]["o"] / bars[i_up - 1]["h"] - 1) * 100 < min_gap * 0.5 or bars[i_up]["c"] < bars[i_up]["o"]: return None
    for j in range(i_up - 1, max(i_up - max_island - 1, 1), -1):
        if (1 - bars[j]["o"] / bars[j - 1]["l"]) * 100 >= min_gap:
            island = bars[j:i_up]
            if all(b["h"] < bars[j - 1]["l"] and b["h"] < bars[i_up]["l"] for b in island):
                lo = min(b["l"] for b in island)
                return Signal("island_bottom", "long", "swing", bars[-1]["c"], lo, bars[j - 1]["h"], 0.7, f"island {i_up - j}d", True)
    return None

# ---------- מגמה + נסיגה ----------
def trend_pullback_long(bars):
    n = len(bars)
    if n < 60: return None
    closes = [b["c"] for b in bars]
    s20, s50, r = sma(closes, 20), sma(closes, 50), rsi(closes)
    st = trend_structure(bars)
    last = bars[-1]
    if st["trend"] != "up" or not s50 or last["c"] <= s50 or r is None or not (38 <= r <= 60): return None
    if not (last["l"] <= s20 * 1.015 and last["c"] >= s20 * 0.985): return None
    cand = bull_candle(bars)
    if not cand and last["c"] <= bars[-2]["h"]: return None
    stop = st["last_low"] * 0.995
    if stop >= last["c"] or (last["c"] - stop) / last["c"] > 0.10: return None
    a = atr(bars) or 0
    hi = st["last_high"]
    tgt = hi + 0.27 * (hi - st["last_low"]) if hi > last["c"] else last["c"] + 3 * a
    dry = avg(b["v"] for b in bars[-3:]) < _vavg(bars)
    return Signal("trend_pullback", "long", "swing", last["c"], stop, tgt, 0.6 + (0.15 if cand else 0) + (0.05 if dry else 0),
                  f"pullback to SMA20 candle={cand}", dry)

def fib_pullback_long(bars):
    n = len(bars)
    if n < 60: return None
    piv = pivots(bars)
    lows = [p for p in piv if p[2] == "L"]; highs = [p for p in piv if p[2] == "H"]
    if not lows or not highs: return None
    H = highs[-1]
    prior = [l for l in lows if l[0] < H[0]]
    if not prior: return None
    L = prior[-1]
    last = bars[-1]
    if H[1] <= L[1] or last["c"] >= H[1] or H[0] - L[0] < 5: return None
    ret = (H[1] - last["c"]) / (H[1] - L[1])
    if not (0.382 <= ret <= 0.65): return None
    cand = bull_candle(bars)
    if not cand: return None
    a = atr(bars) or 0
    return Signal("fib_pullback", "long", "swing", last["c"], L[1] - 0.25 * a, H[1] + 0.272 * (H[1] - L[1]),
                  0.65 + (0.1 if 0.5 <= ret <= 0.62 else 0), f"retrace {ret * 100:.0f}% candle={cand}", False)

def breakout_retest_long(bars):
    n = len(bars)
    if n < 60: return None
    levels = key_levels(bars[:-14])
    last, a = bars[-1], atr(bars) or 0
    for lv in sorted(levels, key=lambda x: -x["touches"]):
        L = lv["price"]
        for k in range(n - 12, n - 2):
            va = avg(b["v"] for b in bars[max(0, k - 20):k])
            if bars[k]["c"] > L * 1.01 and bars[k - 1]["c"] <= L * 1.003 and bars[k]["v"] >= 1.3 * va:
                if any(b["c"] < L * 0.985 for b in bars[k:]): break
                if last["l"] <= L * 1.012 and last["c"] >= L * 0.997 and (last["c"] > last["o"] or bull_candle(bars)):
                    return Signal("breakout_retest", "long", "swing", last["c"], L - a, last["c"] + 3 * a, 0.7,
                                  f"retest of {L:.2f} ({lv['touches']} touches)", False)
                break
    return None

# ---------- שיאי 52 שבועות / מומנטום ----------
def high52_breakout_long(bars, rs=0.0):
    n = len(bars)
    if n < 130: return None
    look = min(252, n - 1)
    hh = max(b["h"] for b in bars[-look - 1:-1])
    last, a = bars[-1], atr(bars) or 0
    closes = [b["c"] for b in bars]
    s50 = sma(closes, 50)
    if not (hh < last["c"] <= hh * 1.04) or last["v"] < 1.4 * _vavg(bars) or not s50 or last["c"] < s50: return None
    return Signal("high52_breakout", "long", "swing", last["c"], last["c"] - 2.5 * a, last["c"] + 5 * a,
                  0.6 + (0.15 if rs >= 10 else 0) + (0.05 if last["v"] >= 2 * _vavg(bars) else 0), f"new {look}d high rs={rs:.0f}", True)

def oversold_bounce_long(bars):
    n = len(bars)
    if n < 205: return None
    closes = [b["c"] for b in bars]
    s200, s20, r = sma(closes, 200), sma(closes, 20), rsi(closes)
    last, a = bars[-1], atr(bars) or 0
    if r is None or r > 32 or last["c"] <= s200: return None
    cand = bull_candle(bars)
    if cand not in ("hammer", "bullish_engulfing"): return None
    return Signal("oversold_bounce", "long", "swing", last["c"], last["l"] - 0.5 * a, s20 if s20 > last["c"] else last["c"] + 2 * a,
                  0.55, f"RSI {r:.0f} above SMA200 candle={cand}", False)

def bollinger_squeeze_long(bars):
    n = len(bars)
    if n < 145: return None
    closes = [b["c"] for b in bars]
    widths = [bollinger(closes[:i], 20)[3] for i in range(n - 122, n - 1)]
    cur = bollinger(closes, 20)
    last, a = bars[-1], atr(bars) or 0
    if widths[-1] > min(widths) * 1.15 or last["c"] <= cur[1] or last["v"] < 1.3 * _vavg(bars): return None
    return Signal("bollinger_squeeze", "long", "swing", last["c"], cur[0], last["c"] + 3 * a, 0.6, f"squeeze width {widths[-1]:.1f}%", True)

LONG_DETECTORS = {
    "flag": lambda b, c: flag_long(b),
    "base_breakout": lambda b, c: base_breakout_long(b),
    "double_bottom": lambda b, c: double_bottom_long(b),
    "head_shoulders": lambda b, c: inverse_hs_long(b),
    "ascending_triangle": lambda b, c: ascending_triangle_long(b),
    "symmetrical_triangle": lambda b, c: symmetrical_triangle_up(b),
    "breakaway_gap": lambda b, c: gap_breakaway_long(b),
    "runaway_gap": lambda b, c: gap_runaway_long(b),
    "island": lambda b, c: island_bottom_long(b),
    "trend_pullback": lambda b, c: trend_pullback_long(b),
    "fib_pullback": lambda b, c: fib_pullback_long(b),
    "breakout_retest": lambda b, c: breakout_retest_long(b),
    "high52_breakout": lambda b, c: high52_breakout_long(b, c.get("rs", 0.0)),
    "oversold_bounce": lambda b, c: oversold_bounce_long(b),
    "bollinger_squeeze": lambda b, c: bollinger_squeeze_long(b),
}

def detect_all(bars, enabled=None, ctx=None, shorts=True):
    """כל הגלאים הימיים, לונג ושורט. מחזיר רשימת Signal"""
    ctx = ctx or {}
    out = []
    names = [n for n in LONG_DETECTORS if enabled is None or enabled.get(n, True)]
    for name in names:
        try:
            s = LONG_DETECTORS[name](bars, ctx)
            if s: out.append(s)
        except Exception:
            pass
    if shorts and len(bars) > 40:
        mb, k2 = mirror(bars)
        mctx = dict(ctx); mctx["rs"] = -ctx.get("rs", 0.0)
        for name in names:
            if name in ("runaway_gap",) and False: continue
            try:
                s = LONG_DETECTORS[name](mb, mctx)
                if s: out.append(unmirror(s, k2))
            except Exception:
                pass
    return out

# =================== אסטרטגיות יום (נרות 5 דקות) ===================
def orb_long(bars5, ctx=None, or_bars=3):
    """Opening Range Breakout: פריצת שיא 15 הדקות הראשונות, מעל VWAP ובנפח"""
    ctx = ctx or {}
    n = len(bars5)
    if n < or_bars + 3: return None
    rng = bars5[:or_bars]
    oh, ol = max(b["h"] for b in rng), min(b["l"] for b in rng)
    last = bars5[-1]
    if (oh - ol) / ol * 100 < 0.3 or (oh - ol) / ol * 100 > 6: return None
    if not (oh < last["c"] <= oh * 1.02): return None
    if any(b["c"] > oh for b in bars5[or_bars:-1]): return None        # פריצה טרייה בלבד
    vw = vwap(bars5)
    base_v = avg(b["v"] for b in bars5[:-1])
    if (vw and last["c"] < vw) or last["v"] < 1.3 * base_v: return None
    gap = ((bars5[0]["o"] / ctx["prev_close"] - 1) * 100) if ctx.get("prev_close") else 0
    name = "gap_and_go" if gap >= 2.0 else "orb"
    q = 0.6 + (0.1 if last["v"] >= 2 * base_v else 0) + (0.1 if name == "gap_and_go" else 0)
    h = oh - ol
    return Signal(name, "long", "day", last["c"], max(ol, last["c"] - 1.5 * h) - 0.02, last["c"] + 2 * h, q,
                  f"OR {ol:.2f}-{oh:.2f} gap {gap:.1f}%", True)

def vwap_reclaim_long(bars5, ctx=None):
    n = len(bars5)
    if n < 12: return None
    last, vw_now = bars5[-1], vwap(bars5)
    if not vw_now or last["c"] <= vw_now: return None
    for k in range(n - 5, n - 1):                       # 4 הברים הקודמים סגרו מתחת ל-VWAP
        v = vwap(bars5[:k + 1])
        if not v or bars5[k]["c"] >= v: return None
    if last["v"] < 1.3 * avg(b["v"] for b in bars5[:-1]): return None
    lo = min(b["l"] for b in bars5[-5:])
    r = last["c"] - lo
    if r <= 0 or r / last["c"] > 0.05: return None
    return Signal("vwap_reclaim", "long", "day", last["c"], lo - 0.02, last["c"] + 2 * r, 0.6, f"reclaim vwap {vw_now:.2f}", True)

DAY_DETECTORS = {"orb": orb_long, "vwap_reclaim": vwap_reclaim_long}

def detect_day(bars5, ctx=None, enabled=None, shorts=True):
    ctx = ctx or {}
    out, seen = [], set()
    def run(bars, c, mirrored, k2=None):
        for name, fn in DAY_DETECTORS.items():
            if enabled is not None and not enabled.get(name, True): continue
            try: s = fn(bars, c)
            except Exception: continue
            if not s: continue
            if mirrored: s = unmirror(s, k2)
            out.append(s)
    run(bars5, ctx, False)
    if shorts and len(bars5) > 8:
        mb, k2 = mirror(bars5)
        mc = dict(ctx)
        if ctx.get("prev_close"): mc["prev_close"] = k2 / ctx["prev_close"]
        run(mb, mc, True, k2)
    return out
