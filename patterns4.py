"""v6: גלאים 'ילידיים' לשורט (לא מראה) + עוד אסטרטגיות לונג. (bars, ctx) -> Signal|None.
כל גלאי עובר ולידציה גאומטרית: לונג stop<price<target, שורט target<price<stop, סטופ סביר."""
import patterns as P
from patterns import Signal, body_beyond, BODY_MIN, _vavg
from indicators import sma, ema, rsi, atr, avg, adx, ibs, macd, stoch, bollinger
from structure import pivots, trend_structure

def _cl(bars): return [b["c"] for b in bars]

def bear_beyond(b, level):
    """כמה מגוף נר אדום מתחת לקו (0..1)"""
    body = b["o"] - b["c"]
    if body <= 0 or b["c"] >= level: return 0.0
    return min(1.0, (min(b["o"], level) - b["c"]) / body)

def _bull(b): return b["c"] > b["o"]
def _bear(b): return b["c"] < b["o"]
def _body(b): return abs(b["c"] - b["o"])
def _rng(b): return b["h"] - b["l"]

def _down(bars):
    c = _cl(bars); s = sma(c, 50); sp = sma(c[:-5], 50) if len(c) > 56 else None
    return bool(s and sp and c[-1] < s and s < sp)

def _up(bars):
    c = _cl(bars); s = sma(c, 50); sp = sma(c[:-5], 50) if len(c) > 56 else None
    return bool(s and sp and c[-1] > s and s > sp)

def _short(name, price, stop, target, q, notes, vol=True, rr=None):
    if rr: target = min(target, price - rr * (stop - price)) if target is not None else price - rr * (stop - price)
    return Signal(name, "short", "swing", price, stop, target, q, notes, vol)

def _long(name, price, stop, target, q, notes, vol=True, rr=None):
    if rr: target = max(target, price + rr * (price - stop)) if target is not None else price + rr * (price - stop)
    return Signal(name, "long", "swing", price, stop, target, q, notes, vol)

# =============================== שורט (ילידי) ===============================
def bear_flag(bars, ctx=None):
    if len(bars) < 50: return None
    last, a = bars[-1], atr(bars)
    if not a: return None
    for fl in range(3, 11):
        flag = bars[-1 - fl:-1]; pole = bars[-1 - fl - 12:-1 - fl]
        top, bot = max(b["h"] for b in pole), min(b["l"] for b in pole)
        if (top - bot) / top < 0.10 or pole[0]["h"] < top * 0.97: continue
        fh, fl_ = max(b["h"] for b in flag), min(b["l"] for b in flag)
        if fh - bot > 0.5 * (top - bot) or any(b["c"] < fl_ * 0.995 for b in flag[:-1]): continue
        if last["c"] < fl_ and bear_beyond(last, fl_) >= BODY_MIN and last["v"] > 1.1 * _vavg(bars):
            return _short("bear_flag", last["c"], fh + 0.25 * a, last["c"] - 0.75 * (top - bot), 0.7, f"flag {fl_:.2f}-{fh:.2f}", True)
    return None

def head_shoulders(bars, ctx=None):
    if len(bars) < 90: return None
    seg = bars[-130:]; piv = pivots(seg, 3, 3); a = atr(bars); last = seg[-1]
    hs = [p for p in piv if p[2] == "H"][-3:]
    if len(hs) < 3 or not a: return None
    (i1, l, _), (i2, h, _), (i3, r, _) = hs
    if not (h > l * 1.02 and h > r * 1.02 and abs(l - r) / h < 0.05) or i3 < len(seg) - 25: return None
    ls = [p[1] for p in piv if p[2] == "L" and i1 < p[0] < i3]
    if len(ls) < 2: return None
    neck = sum(sorted(ls)[:2]) / 2
    if any(b["c"] < neck for b in seg[i3 + 1:-1]): return None
    if not (neck * 0.96 <= last["c"] < neck) or bear_beyond(last, neck) < BODY_MIN: return None
    return _short("head_shoulders", last["c"], max(r, last["h"]) + 0.25 * a, neck - (h - neck), 0.75, f"neckline {neck:.2f}", last["v"] > _vavg(bars))

def double_top(bars, ctx=None):
    if len(bars) < 70: return None
    seg = bars[-100:]; piv = pivots(seg, 3, 3); a = atr(bars); last = seg[-1]
    hs = [p for p in piv if p[2] == "H"][-2:]
    if len(hs) < 2 or not a: return None
    (i1, h1, _), (i2, h2, _) = hs
    if abs(h1 - h2) / h1 > 0.02 or not (8 <= i2 - i1 <= 60) or i2 < len(seg) - 20: return None
    mid = min(b["l"] for b in seg[i1:i2 + 1])
    if any(b["c"] < mid for b in seg[i2 + 1:-1]) or not (mid * 0.96 <= last["c"] < mid) or bear_beyond(last, mid) < BODY_MIN: return None
    top = max(h1, h2)
    return _short("double_top", last["c"], top + 0.25 * a, mid - (top - mid), 0.7, f"top {top:.2f} neck {mid:.2f}", last["v"] > _vavg(bars))

def breakdown_support(bars, ctx=None):
    if len(bars) < 60: return None
    last, a = bars[-1], atr(bars)
    lo20, hi20 = min(b["l"] for b in bars[-21:-1]), max(b["h"] for b in bars[-21:-1])
    if not a or not (lo20 * 0.96 <= last["c"] < lo20) or bear_beyond(last, lo20) < BODY_MIN or last["v"] < 1.2 * _vavg(bars) or not _down(bars): return None
    return _short("breakdown_support", last["c"], lo20 + 0.75 * a, last["c"] - 0.6 * (hi20 - lo20), 0.6, f"breaks 20d low {lo20:.2f}", True)

def upthrust(bars, ctx=None):
    if len(bars) < 60: return None
    last, a = bars[-1], atr(bars)
    hi20 = max(b["h"] for b in bars[-21:-1])
    if not a or last["h"] <= hi20 or last["c"] >= hi20 or ibs(last) >= 0.35: return None
    return _short("upthrust", last["c"], last["h"] + 0.25 * a, hi20 - 3 * a, 0.65, f"failed break of {hi20:.2f}", last["v"] > _vavg(bars), rr=2)

def evening_star(bars, ctx=None):
    if len(bars) < 40: return None
    b1, b2, b3 = bars[-3:]; a = atr(bars); c = _cl(bars)
    if not a or not _bull(b1) or _body(b1) < 0.6 * a or _body(b2) > 0.35 * _body(b1) or min(b2["o"], b2["c"]) < b1["c"] * 0.998: return None
    if not _bear(b3) or b3["c"] > (b1["o"] + b1["c"]) / 2 or c[-4] < sma(c, 20) or (c[-4] / c[-14] - 1) < 0.04: return None
    stop = max(b1["h"], b2["h"], b3["h"]) + 0.25 * a
    return _short("evening_star", b3["c"], stop, None, 0.65, "evening star", b3["v"] > _vavg(bars), rr=2)

def bearish_engulfing_top(bars, ctx=None):
    if len(bars) < 40: return None
    p, l = bars[-2], bars[-1]; a = atr(bars)
    if not a or not (_bull(p) and _bear(l)) or l["o"] < p["c"] or l["c"] > p["o"] or _body(l) < 0.8 * a: return None
    if l["h"] < max(b["h"] for b in bars[-21:-1]) * 0.99: return None
    return _short("bearish_engulfing_top", l["c"], l["h"] + 0.25 * a, None, 0.65, "engulfing at highs", l["v"] > _vavg(bars), rr=2)

def shooting_star(bars, ctx=None):
    if len(bars) < 40: return None
    l, a = bars[-1], atr(bars); c = _cl(bars)
    if not a or _rng(l) < 1.2 * a: return None
    up = l["h"] - max(l["o"], l["c"]); dn = min(l["o"], l["c"]) - l["l"]
    if up < 2 * max(_body(l), 0.1 * a) or dn > 0.25 * _rng(l) or (c[-1] / c[-11] - 1) < 0.08 or not _bear(l): return None
    return _short("shooting_star", l["c"], l["h"] + 0.25 * a, None, 0.62, "shooting star after run-up", l["v"] > _vavg(bars), rr=2)

def three_black_crows(bars, ctx=None):
    if len(bars) < 40: return None
    x = bars[-3:]; a = atr(bars); c = _cl(bars)
    if not a or not all(_bear(b) and _body(b) > 0.5 * a for b in x): return None
    if not (x[0]["c"] > x[1]["c"] > x[2]["c"]) or not all(x[i]["c"] < x[i]["o"] and x[i + 1]["o"] <= x[i]["o"] and x[i + 1]["o"] >= x[i]["c"] for i in range(2)): return None
    if c[-4] < sma(c, 20): return None
    return _short("three_black_crows", x[2]["c"], max(b["h"] for b in x) + 0.25 * a, None, 0.62, "three black crows", x[2]["v"] > _vavg(bars), rr=2)

def death_cross(bars, ctx=None):
    if len(bars) < 215: return None
    c = _cl(bars); a = atr(bars)
    s50, s200, p50, p200 = sma(c, 50), sma(c, 200), sma(c[:-5], 50), sma(c[:-5], 200)
    if not (a and s50 and s200 and p50 and p200) or not (p50 >= p200 and s50 < s200 and c[-1] < s200): return None
    return _short("death_cross", c[-1], c[-1] + 2 * a, None, 0.55, "50/200 death cross", bars[-1]["v"] > _vavg(bars), rr=2)

def dead_cat_bounce(bars, ctx=None):
    if len(bars) < 50: return None
    seg = bars[-25:]; last, a = bars[-1], atr(bars)
    pk = max(range(len(seg) - 8), key=lambda i: seg[i]["h"]); top = seg[pk]["h"]
    lo_i = min(range(pk, len(seg) - 3), key=lambda i: seg[i]["l"]); lo = seg[lo_i]["l"]
    if not a or (top - lo) / top < 0.15 or lo_i >= len(seg) - 3: return None
    bh = max(b["h"] for b in seg[lo_i + 1:])
    ret = (bh - lo) / (top - lo)
    if not (0.3 <= ret <= 0.65) or not (_bear(last) and last["c"] < bars[-2]["c"] and _body(last) > 0.5 * a): return None
    return _short("dead_cat_bounce", last["c"], bh + 0.25 * a, lo * 0.99, 0.65, f"bounce {ret:.0%} of drop failed", True, rr=1.5)

def lower_low_breakdown(bars, ctx=None):
    if len(bars) < 60: return None
    st = trend_structure(bars[:-1]); last, a = bars[-1], atr(bars)
    if st["trend"] != "down" or not a or st["last_low"] is None or st["last_high"] is None: return None
    lo, hi = st["last_low"], st["last_high"]
    if not (lo * 0.97 <= last["c"] < lo) or bear_beyond(last, lo) < BODY_MIN or last["v"] < 1.0 * _vavg(bars): return None
    stop = hi + 0.25 * a if hi + 0.25 * a > last["c"] else last["c"] + 2 * a
    return _short("lower_low_breakdown", last["c"], stop, last["c"] - (hi - lo), 0.68, f"breaks LL {lo:.2f}", True)

def rising_wedge(bars, ctx=None):
    if len(bars) < 70: return None
    seg = bars[-60:]; piv = pivots(seg, 3, 3); last, a = seg[-1], atr(bars)
    hs = [p for p in piv if p[2] == "H"][-2:]; ls = [p for p in piv if p[2] == "L"][-2:]
    if len(hs) < 2 or len(ls) < 2 or not a: return None
    if not (hs[1][1] > hs[0][1] and ls[1][1] > ls[0][1]) or (hs[1][1] - ls[1][1]) > 0.85 * (hs[0][1] - ls[0][1]) or ls[1][0] - ls[0][0] < 6: return None
    slope = (ls[1][1] - ls[0][1]) / (ls[1][0] - ls[0][0]); line = ls[1][1] + slope * (len(seg) - 1 - ls[1][0])
    if not (line * 0.97 <= last["c"] < line) or bear_beyond(last, line) < BODY_MIN: return None
    return _short("rising_wedge", last["c"], hs[1][1] + 0.25 * a, last["c"] - (hs[0][1] - ls[0][1]), 0.65, "rising wedge break", last["v"] > _vavg(bars))

def descending_triangle(bars, ctx=None):
    if len(bars) < 60: return None
    seg = bars[-60:]; piv = pivots(seg, 3, 3); last, a = seg[-1], atr(bars)
    hs = [p for p in piv if p[2] == "H"][-2:]; ls = [p for p in piv if p[2] == "L"][-2:]
    if len(hs) < 2 or len(ls) < 2 or not a or abs(ls[1][1] - ls[0][1]) / ls[0][1] > 0.012 or hs[1][1] > hs[0][1] * 0.98: return None
    sup = min(ls[0][1], ls[1][1])
    if not (sup * 0.97 <= last["c"] < sup) or bear_beyond(last, sup) < BODY_MIN or any(b["c"] < sup for b in seg[ls[1][0] + 1:-1]): return None
    return _short("descending_triangle", last["c"], hs[1][1] + 0.25 * a, last["c"] - (hs[0][1] - sup), 0.68, f"support {sup:.2f}", last["v"] > _vavg(bars))

def blowoff_top(bars, ctx=None):
    if len(bars) < 50: return None
    c = _cl(bars); last, a = bars[-1], atr(bars); s20 = sma(c, 20); r = rsi(c)
    if not (a and s20 and r) or not (c[-1] > s20 + 3 * a and r > 75 and _bear(last) and ibs(last) < 0.4): return None
    return _short("blowoff_top", c[-1], last["h"] + 0.25 * a, s20, 0.6, f"stretched {(c[-1] / s20 - 1) * 100:.0f}% over SMA20, RSI {r:.0f}", True)

def rsi2_overbought(bars, ctx=None):
    if len(bars) < 210: return None
    c = _cl(bars); a = atr(bars); s5, s200 = sma(c, 5), sma(c, 200); r2 = rsi(c, 2)
    if not (a and s5 and s200 and r2) or not (c[-1] < s200 and r2 >= 95 and c[-1] > s5 and c[-1] - s5 > 0.7 * a): return None
    return _short("rsi2_overbought", c[-1], c[-1] + 2 * a, s5, 0.55, f"RSI2 {r2:.0f} below SMA200", True)

def bb_upper_fade(bars, ctx=None):
    if len(bars) < 40: return None
    c = _cl(bars); last, a = bars[-1], atr(bars); bb = bollinger(c)
    if not (a and bb): return None
    mid, up, _, _ = bb
    if not (last["h"] > up and last["c"] < up and _bear(last) and last["c"] - mid > 0.8 * a): return None
    return _short("bb_upper_fade", last["c"], last["h"] + 0.25 * a, mid, 0.55, "rejected at upper Bollinger", True, rr=1.2)

def macd_bear_cross(bars, ctx=None):
    if len(bars) < 70: return None
    c = _cl(bars); a = atr(bars); m = macd(c); s50 = sma(c, 50)
    if not (a and m and s50): return None
    line, sig, h, ph = m
    if not (ph > 0 >= h and line < 0 and c[-1] < s50): return None
    return _short("macd_bear_cross", c[-1], c[-1] + 1.5 * a, c[-1] - 3 * a, 0.5, "MACD cross down below zero", True)

def sma50_rejection(bars, ctx=None):
    if len(bars) < 70: return None
    c = _cl(bars); last, a = bars[-1], atr(bars); s50 = sma(c, 50)
    if not (a and s50) or not _down(bars) or not (last["h"] >= s50 * 0.995 and last["c"] < s50 and _bear(last) and bars[-2]["c"] < s50): return None
    return _short("sma50_rejection", last["c"], last["h"] + 0.25 * a, None, 0.62, f"rejected at falling SMA50 {s50:.2f}", True, rr=2)

def gap_up_fade(bars, ctx=None):
    if len(bars) < 40: return None
    p, l = bars[-2], bars[-1]; a = atr(bars)
    if not a or l["o"] < p["c"] * 1.03 or not (_bear(l) and ibs(l) < 0.4 and l["c"] < l["o"] - 0.3 * a) or l["c"] <= p["c"]: return None
    return _short("gap_up_fade", l["c"], l["h"] + 0.25 * a, p["c"], 0.6, f"gap {(l['o'] / p['c'] - 1) * 100:.1f}% faded", l["v"] > _vavg(bars), rr=1.2)

def bear_divergence(bars, ctx=None):
    if len(bars) < 80: return None
    seg = bars[-70:]; piv = pivots(seg, 3, 3); last, a = seg[-1], atr(bars)
    hs = [p for p in piv if p[2] == "H"][-2:]
    if len(hs) < 2 or not a or hs[1][1] <= hs[0][1] or hs[1][0] < len(seg) - 15: return None
    r1, r2 = rsi(_cl(seg[:hs[0][0] + 1])), rsi(_cl(seg[:hs[1][0] + 1]))
    if not (r1 and r2 and r2 < r1 - 4 and r1 > 60) or not (_bear(last) and last["c"] < bars[-2]["l"]): return None
    return _short("bear_divergence", last["c"], hs[1][1] + 0.25 * a, None, 0.62, f"RSI {r1:.0f}->{r2:.0f} on higher high", True, rr=2)

def distribution_breakdown(bars, ctx=None):
    if len(bars) < 60: return None
    last, a = bars[-1], atr(bars); base = bars[-30:-10]; rec = bars[-11:-1]
    if not a or max(b["h"] for b in rec) < max(b["h"] for b in bars[-60:]) * 0.97: return None
    if avg(b["v"] for b in rec) < 1.4 * avg(b["v"] for b in base) or avg(_rng(b) for b in rec) > 1.0 * a: return None
    lo5 = min(b["l"] for b in bars[-6:-1])
    if not (_bear(last) and last["c"] < lo5 and last["v"] > _vavg(bars)): return None
    return _short("distribution_breakdown", last["c"], max(b["h"] for b in rec) + 0.25 * a, None, 0.62, "high-volume churn at highs then breakdown", True, rr=2)

def stoch_overbought_cross(bars, ctx=None):
    if len(bars) < 70: return None
    c = _cl(bars); a = atr(bars); s = stoch(bars); s50 = sma(c, 50)
    if not (a and s and s50): return None
    k, d, pk, pd = s
    if not (pk >= pd and k < d and pd > 80 and c[-1] < s50): return None
    return _short("stoch_overbought_cross", c[-1], c[-1] + 1.5 * a, c[-1] - 3 * a, 0.5, "Stoch cross down from overbought in downtrend", True)

def ema21_rejection(bars, ctx=None):
    if len(bars) < 70: return None
    c = _cl(bars); last, a = bars[-1], atr(bars); e, ep = ema(c, 21), ema(c[:-3], 21)
    if not (a and e and ep) or not (e < ep and last["h"] >= e * 0.998 and last["c"] < e and _bear(last) and _down(bars)): return None
    return _short("ema21_rejection", last["c"], last["h"] + 0.25 * a, None, 0.58, "rejected at falling EMA21", True, rr=2)

def range_breakdown(bars, ctx=None):
    if len(bars) < 50: return None
    last, a = bars[-1], atr(bars); rg = bars[-16:-1]
    hi, lo = max(b["h"] for b in rg), min(b["l"] for b in rg)
    if not a or (hi - lo) / last["c"] > 0.08 or not (lo * 0.97 <= last["c"] < lo) or bear_beyond(last, lo) < BODY_MIN or last["v"] < 1.2 * _vavg(bars): return None
    return _short("range_breakdown", last["c"], (hi + lo) / 2, last["c"] - (hi - lo), 0.6, "tight range breaks down", True)

def parabolic_reversal(bars, ctx=None):
    if len(bars) < 40: return None
    c = _cl(bars); last, a = bars[-1], atr(bars)
    if not a or c[-1] / c[-6] < 1.25 or not (_bear(last) and ibs(last) < 0.3): return None
    e10 = ema(c, 10)
    return _short("parabolic_reversal", c[-1], last["h"] + 0.25 * a, e10 if e10 and e10 < c[-1] - a else c[-1] - 3 * a, 0.6, "+25% in 5d then reversal", True, rr=1.2)

def gap_and_crap(bars, ctx=None):
    if len(bars) < 60: return None
    p, l = bars[-2], bars[-1]; a = atr(bars)
    if not a or l["o"] > p["c"] * 0.98 or ibs(l) > 0.25 or not _down(bars) or l["v"] < 1.5 * _vavg(bars): return None
    return _short("gap_and_crap", l["c"], l["h"] + 0.2 * a, None, 0.6, f"gap down {(l['o'] / p['c'] - 1) * 100:.1f}% closing at lows", True, rr=2)

def low52_breakdown(bars, ctx=None):
    if len(bars) < 210: return None
    last, a = bars[-1], atr(bars); lo = min(b["l"] for b in bars[-251:-1])
    if not a or not (lo * 0.97 <= last["c"] < lo) or bear_beyond(last, lo) < BODY_MIN or last["v"] < 1.2 * _vavg(bars): return None
    return _short("low52_breakdown", last["c"], lo + a, None, 0.62, f"breaks 52w low {lo:.2f}", True, rr=2)

def volume_climax_top(bars, ctx=None):
    if len(bars) < 40: return None
    c = _cl(bars); last, a = bars[-1], atr(bars)
    if not a or last["v"] < 3 * _vavg(bars) or not (c[-2] > c[-3] > c[-4] > c[-5]) or not (_bear(last) and last["c"] < bars[-2]["l"]): return None
    return _short("volume_climax_top", last["c"], last["h"] + 0.25 * a, None, 0.62, "volume climax after run", True, rr=2)

# =============================== לונג (חדשים) ===============================
def ascending_triangle(bars, ctx=None):
    if len(bars) < 60: return None
    seg = bars[-60:]; piv = pivots(seg, 3, 3); last, a = seg[-1], atr(bars)
    hs = [p for p in piv if p[2] == "H"][-2:]; ls = [p for p in piv if p[2] == "L"][-2:]
    if len(hs) < 2 or len(ls) < 2 or not a or abs(hs[1][1] - hs[0][1]) / hs[0][1] > 0.012 or ls[1][1] < ls[0][1] * 1.02: return None
    res = max(hs[0][1], hs[1][1])
    if not (res < last["c"] <= res * 1.04) or body_beyond(last, res) < BODY_MIN or any(b["c"] > res for b in seg[hs[1][0] + 1:-1]): return None
    return _long("ascending_triangle", last["c"], ls[1][1] - 0.25 * a, last["c"] + (res - ls[0][1]), 0.68, f"resistance {res:.2f}", last["v"] > 1.1 * _vavg(bars))

def triple_bottom(bars, ctx=None):
    if len(bars) < 80: return None
    seg = bars[-110:]; piv = pivots(seg, 3, 3); last, a = seg[-1], atr(bars)
    ls = [p for p in piv if p[2] == "L"][-3:]
    if len(ls) < 3 or not a: return None
    lo, hi = min(p[1] for p in ls), max(p[1] for p in ls)
    if (hi - lo) / lo > 0.03 or ls[0][0] < len(seg) - 90: return None
    neck = max(b["h"] for b in seg[ls[0][0]:ls[2][0] + 1])
    if not (neck < last["c"] <= neck * 1.04) or body_beyond(last, neck) < BODY_MIN: return None
    return _long("triple_bottom", last["c"], lo - 0.25 * a, last["c"] + (neck - lo), 0.7, f"neckline {neck:.2f}", last["v"] > _vavg(bars))

def bullish_engulfing_support(bars, ctx=None):
    if len(bars) < 40: return None
    p, l = bars[-2], bars[-1]; a = atr(bars)
    if not a or not (_bear(p) and _bull(l)) or l["o"] > p["c"] or l["c"] < p["o"] or _body(l) < 0.8 * a: return None
    if l["l"] > min(b["l"] for b in bars[-21:-1]) * 1.01: return None
    return _long("bullish_engulfing_support", l["c"], l["l"] - 0.25 * a, None, 0.65, "engulfing at lows", l["v"] > _vavg(bars), rr=2)

def hammer_support(bars, ctx=None):
    if len(bars) < 40: return None
    l, a = bars[-1], atr(bars); c = _cl(bars)
    if not a or _rng(l) < 1.2 * a: return None
    dn = min(l["o"], l["c"]) - l["l"]; up = l["h"] - max(l["o"], l["c"])
    if dn < 2 * max(_body(l), 0.1 * a) or up > 0.25 * _rng(l) or (c[-1] / c[-11] - 1) > -0.06 or not _bull(l): return None
    return _long("hammer_support", l["c"], l["l"] - 0.25 * a, None, 0.62, "hammer after decline", l["v"] > _vavg(bars), rr=2)

def three_inside_up(bars, ctx=None):
    if len(bars) < 40: return None
    b1, b2, b3 = bars[-3:]; a = atr(bars); c = _cl(bars)
    if not a or not _bear(b1) or _body(b1) < 0.6 * a or not _bull(b2) or b2["o"] < b1["c"] or b2["c"] > b1["o"] or not _bull(b3) or b3["c"] <= b1["o"] or c[-4] > sma(c, 20): return None
    return _long("three_inside_up", b3["c"], min(b1["l"], b2["l"]) - 0.25 * a, None, 0.62, "three inside up", b3["v"] > _vavg(bars), rr=2)

def rsi_oversold_uptrend(bars, ctx=None):
    if len(bars) < 210: return None
    c = _cl(bars); last, a = bars[-1], atr(bars); r = rsi(c); s200 = sma(c, 200)
    if not (a and r and s200) or not (c[-1] > s200 and min(rsi(c[:-1]) or 99, rsi(c[:-2]) or 99) < 35 and _bull(last) and c[-1] > c[-2]): return None
    return _long("rsi_oversold_uptrend", c[-1], min(b["l"] for b in bars[-4:]) - 0.25 * a, None, 0.62, f"RSI dip bought above SMA200", True, rr=2)

def cum_rsi2(bars, ctx=None):
    """Connors: RSI(2) מצטבר של יומיים < 35 מעל SMA200"""
    if len(bars) < 210: return None
    c = _cl(bars); a = atr(bars); s200 = sma(c, 200); r0, r1 = rsi(c, 2), rsi(c[:-1], 2)
    if not (a and s200 and r0 is not None and r1 is not None) or not (c[-1] > s200 and r0 + r1 < 35): return None
    return _long("cum_rsi2", c[-1], c[-1] - 2 * a, sma(c, 5) if sma(c, 5) and sma(c, 5) > c[-1] + 0.7 * a else c[-1] + 2 * a, 0.58, f"cumRSI2 {r0 + r1:.0f}", True)

def sma200_reclaim(bars, ctx=None):
    if len(bars) < 215: return None
    c = _cl(bars); last, a = bars[-1], atr(bars); s200 = sma(c, 200)
    if not (a and s200) or not (all(x < s200 * 1.002 for x in c[-8:-1]) and last["c"] > s200 and body_beyond(last, s200) >= BODY_MIN and last["v"] > 1.2 * _vavg(bars)): return None
    return _long("sma200_reclaim", last["c"], s200 - 1.5 * a, None, 0.62, "reclaims SMA200", True, rr=2)

def sma50_bounce(bars, ctx=None):
    if len(bars) < 70: return None
    c = _cl(bars); last, a = bars[-1], atr(bars); s50 = sma(c, 50)
    if not (a and s50) or not _up(bars) or not (last["l"] <= s50 * 1.005 and last["c"] > s50 and _bull(last) and bars[-2]["c"] > s50 * 0.995): return None
    return _long("sma50_bounce", last["c"], min(last["l"], s50) - 0.5 * a, None, 0.62, f"bounce off rising SMA50 {s50:.2f}", True, rr=2)

def bb_lower_bounce(bars, ctx=None):
    if len(bars) < 40: return None
    c = _cl(bars); last, a = bars[-1], atr(bars); bb = bollinger(c)
    if not (a and bb): return None
    mid, _, lo, _ = bb
    if not (last["l"] < lo and last["c"] > lo and _bull(last) and mid - last["c"] > 0.8 * a and _up(bars)): return None
    return _long("bb_lower_bounce", last["c"], last["l"] - 0.25 * a, mid, 0.55, "rejected at lower Bollinger in uptrend", True, rr=1.2)

def seven_day_low_confirm(bars, ctx=None):
    if len(bars) < 210: return None
    c = _cl(bars); last, a = bars[-1], atr(bars); s200 = sma(c, 200)
    if not (a and s200) or not (c[-1] > s200 and c[-2] <= min(c[-9:-1]) and _bull(last) and c[-1] > bars[-2]["h"]): return None
    return _long("seven_day_low_confirm", c[-1], bars[-2]["l"] - 0.25 * a, None, 0.58, "7-day low then close above prior high", True, rr=2)

def outside_day_reversal(bars, ctx=None):
    if len(bars) < 40: return None
    p, l = bars[-2], bars[-1]; a = atr(bars)
    if not a or not (l["h"] > p["h"] and l["l"] < p["l"] and _bull(l) and l["c"] > p["h"] and ibs(l) > 0.7) or l["l"] > min(b["l"] for b in bars[-11:-1]): return None
    return _long("outside_day_reversal", l["c"], l["l"] - 0.25 * a, None, 0.62, "bullish outside day at lows", l["v"] > _vavg(bars), rr=2)

def gap_up_hold(bars, ctx=None):
    if len(bars) < 40: return None
    p, l = bars[-2], bars[-1]; a = atr(bars); hi20 = max(b["h"] for b in bars[-22:-2])
    if not a or l["o"] < p["c"] * 1.02 or l["o"] < hi20 or not (_bull(l) and ibs(l) > 0.7 and l["l"] >= p["h"] * 0.995) or l["v"] < 1.5 * _vavg(bars): return None
    return _long("gap_up_hold", l["c"], p["h"] - 0.25 * a, None, 0.65, f"gap {(l['o'] / p['c'] - 1) * 100:.1f}% above range holds", True, rr=2)

def volume_dry_up_breakout(bars, ctx=None):
    if len(bars) < 70: return None
    last, a = bars[-1], atr(bars); rg = bars[-16:-1]; hi = max(b["h"] for b in rg)
    if not a or not (hi < last["c"] <= hi * 1.03) or body_beyond(last, hi) < BODY_MIN: return None
    if avg(b["v"] for b in bars[-8:-1]) > 0.7 * avg(b["v"] for b in bars[-40:-8]) or last["v"] < 1.5 * _vavg(bars) or not _up(bars): return None
    return _long("volume_dry_up_breakout", last["c"], min(b["l"] for b in rg[-6:]) - 0.25 * a, None, 0.68, "quiet base breaks out on volume", True, rr=2.5)

def oversold_atr_stretch(bars, ctx=None):
    if len(bars) < 60: return None
    c = _cl(bars); last, a = bars[-1], atr(bars); s20 = sma(c, 20)
    if not (a and s20) or not (c[-1] < s20 - 2.5 * a and _bull(last) and sma(c, 50) and c[-1] > sma(c, 50) * 0.9): return None
    return _long("oversold_atr_stretch", c[-1], last["l"] - 0.25 * a, s20, 0.55, "stretched 2.5 ATR under SMA20", True, rr=1.2)

def tight_closes_breakout(bars, ctx=None):
    if len(bars) < 60: return None
    last, a = bars[-1], atr(bars); c = _cl(bars); hi = max(b["h"] for b in bars[-21:-1])
    t = c[-4:-1]
    if not a or (max(t) - min(t)) / c[-2] > 0.012 or max(b["h"] for b in bars[-4:-1]) < hi * 0.985 or not (hi < last["c"] <= hi * 1.03) or body_beyond(last, hi) < BODY_MIN: return None
    return _long("tight_closes_breakout", last["c"], min(b["l"] for b in bars[-4:-1]) - 0.25 * a, None, 0.66, "3 tight closes at highs then breakout", last["v"] > _vavg(bars), rr=2)

def adx_pullback(bars, ctx=None):
    if len(bars) < 70: return None
    c = _cl(bars); last, a = bars[-1], atr(bars); s20 = sma(c, 20); ax = adx(bars)
    if not (a and s20 and ax) or not (ax > 25 and _up(bars) and last["l"] <= s20 * 1.003 and last["c"] > s20 and _bull(last)): return None
    return _long("adx_pullback", last["c"], min(last["l"], s20) - 0.5 * a, None, 0.62, f"ADX {ax:.0f} pullback to SMA20", True, rr=2)

def three_line_strike_bull(bars, ctx=None):
    if len(bars) < 40: return None
    x = bars[-4:]; a = atr(bars)
    if not a or not (all(_bear(b) for b in x[:3]) and x[0]["c"] > x[1]["c"] > x[2]["c"] and _bull(x[3]) and x[3]["c"] > x[0]["o"] and _up(bars)): return None
    return _long("three_line_strike_bull", x[3]["c"], min(b["l"] for b in x) - 0.25 * a, None, 0.6, "bullish three-line strike in uptrend", x[3]["v"] > _vavg(bars), rr=2)

def bullish_harami_support(bars, ctx=None):
    if len(bars) < 40: return None
    p, l = bars[-2], bars[-1]; a = atr(bars)
    if not a or not (_bear(p) and _body(p) > 0.8 * a and _bull(l) and l["o"] > p["c"] and l["c"] < p["o"] and _body(l) < 0.5 * _body(p)): return None
    if p["l"] > min(b["l"] for b in bars[-21:-2]) * 1.01: return None
    return _long("bullish_harami_support", l["c"], min(p["l"], l["l"]) - 0.25 * a, None, 0.55, "harami at lows", True, rr=2)

# ---------------- רישום + ולידציה ----------------
SHORTS = {f.__name__: f for f in (bear_flag, head_shoulders, double_top, breakdown_support, upthrust, evening_star, bearish_engulfing_top, shooting_star,
                                  three_black_crows, death_cross, dead_cat_bounce, lower_low_breakdown, rising_wedge, descending_triangle, blowoff_top,
                                  rsi2_overbought, bb_upper_fade, macd_bear_cross, sma50_rejection, gap_up_fade, bear_divergence, distribution_breakdown,
                                  stoch_overbought_cross, ema21_rejection, range_breakdown, parabolic_reversal, gap_and_crap, low52_breakdown, volume_climax_top)}
LONGS = {f.__name__: f for f in (ascending_triangle, triple_bottom, bullish_engulfing_support, hammer_support, three_inside_up, rsi_oversold_uptrend, cum_rsi2,
                                 sma200_reclaim, sma50_bounce, bb_lower_bounce, seven_day_low_confirm, outside_day_reversal, gap_up_hold,
                                 volume_dry_up_breakout, oversold_atr_stretch, tight_closes_breakout, adx_pullback, three_line_strike_bull, bullish_harami_support)}

def valid(s):
    if s is None: return None
    p, st, tg = s.price, s.stop, s.target
    if not all(isinstance(x, (int, float)) and x == x and x > 0 for x in (p, st, tg)): return None
    risk = abs(p - st)
    if s.side == "long" and not (st < p < tg): return None
    if s.side == "short" and not (tg < p < st): return None
    if not (0.002 <= risk / p <= 0.12) or abs(tg - p) < 0.5 * risk: return None
    return s

def _guard(f): return lambda b, c=None: valid(f(b, c or {}))

P.NATIVE_SHORT = {k: _guard(f) for k, f in SHORTS.items()}
for _k, _f in LONGS.items(): P.LONG_DETECTORS[_k] = _guard(_f)
