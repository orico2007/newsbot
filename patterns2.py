"""אסטרטגיות נוספות (v4): ממוצע-חוזר, פריצות קלאסיות, תבניות מינרוויני/או'ניל, נרות היפוך, PEAD, וסטאפים ליום.
כל גלאי: (bars, ctx) -> Signal|None, כתוב ללונג; שורט נוצר במראה (detect_all / detect_day). נרשמים ל-patterns.LONG_DETECTORS / DAY_DETECTORS."""
import patterns as P
from patterns import Signal, body_beyond, BODY_MIN, bull_candle, _vavg
from indicators import sma, ema, rsi, atr, avg, adx, keltner, ibs, vwap, bollinger
from structure import pivots, key_levels, trend_structure

def _cl(bars): return [b["c"] for b in bars]

# =============== ממוצע-חוזר (Mean reversion) ===============
def rsi2_reversion(bars, ctx=None):
    """Connors: RSI(2) < 10 בתוך מגמת עלייה ארוכה (מעל SMA200), סגירה מתחת ל-SMA5"""
    if len(bars) < 205: return None
    c = _cl(bars); s200, s5, r2, a = sma(c, 200), sma(c, 5), rsi(c, 2), atr(bars)
    if not (a and r2 is not None) or c[-1] <= s200 or r2 >= 10 or c[-1] >= s5: return None
    s10 = sma(c, 10)
    tgt = s10 if s10 > c[-1] + 0.5 * a else c[-1] + 1.5 * a
    q = 0.55 + (0.1 if r2 < 5 else 0) + (0.05 if c[-1] < c[-2] < c[-3] else 0)
    return Signal("rsi2_reversion", "long", "swing", c[-1], c[-1] - 2.5 * a, tgt, q, f"RSI2={r2:.1f} above SMA200", False)

def ibs_reversion(bars, ctx=None):
    """IBS נמוך (סגירה ליד שפל הנר) + סגירה מתחת לשפל אתמול, בתוך מגמת עלייה"""
    if len(bars) < 205: return None
    c = _cl(bars); last, prev, a = bars[-1], bars[-2], atr(bars)
    if not a or c[-1] <= sma(c, 200) or ibs(last) >= 0.2 or last["c"] >= prev["l"]: return None
    return Signal("ibs_reversion", "long", "swing", last["c"], last["c"] - 2.5 * a, max(prev["h"], last["c"] + a), 0.55, f"IBS={ibs(last):.2f}", False)

# =============== פריצות קלאסיות ===============
def _donchian(bars, n, name, quality):
    if len(bars) < n + 60: return None
    c, last, a = _cl(bars), bars[-1], atr(bars)
    hh = max(b["h"] for b in bars[-n - 1:-1])
    if not a or not (hh < last["c"] <= hh * 1.04) or body_beyond(last, hh) < BODY_MIN or last["v"] < 1.2 * _vavg(bars): return None
    if c[-1] <= sma(c, 100): return None
    low10 = min(b["l"] for b in bars[-10:])
    return Signal(name, "long", "swing", last["c"], max(low10, last["c"] - 3 * a), last["c"] + 5 * a, quality, f"{n}-day high {hh:.2f}", True)

def donchian55(bars, ctx=None): return _donchian(bars, 55, "donchian55", 0.65)
def donchian20(bars, ctx=None): return _donchian(bars, 20, "donchian20", 0.55)

def nr7_breakout(bars, ctx=None):
    """נר ביניים צר (NR7) או נר פנימי, ואז סגירה מעל השיא שלו (חצי גוף)"""
    if len(bars) < 60: return None
    s, last, a = bars[-2], bars[-1], atr(bars)
    c = _cl(bars)
    rng = lambda b: b["h"] - b["l"]
    nr7 = rng(s) <= min(rng(b) for b in bars[-8:-1]) and rng(s) > 0
    inside = s["h"] <= bars[-3]["h"] and s["l"] >= bars[-3]["l"]
    if not (a and (nr7 or inside)) or c[-1] <= sma(c, 50): return None
    if not (s["h"] < last["c"] <= s["h"] + 1.5 * a) or body_beyond(last, s["h"]) < BODY_MIN or last["v"] < 1.1 * _vavg(bars): return None
    stop = min(s["l"], last["c"] - a)
    return Signal("nr7_breakout" if nr7 else "inside_bar_breakout", "long", "swing", last["c"], stop, last["c"] + 3 * a, 0.6, "narrow-range setup", True)

def pocket_pivot(bars, ctx=None):
    """O'Neil/Morales: יום ירוק בנפח גדול מכל נפח ימי הירידה ב-10 הקודמים, ליד ממוצע 10 ביום, בתוך מגמה"""
    if len(bars) < 210: return None
    c, last, a = _cl(bars), bars[-1], atr(bars)
    prior = bars[-11:-1]
    down_v = [b["v"] for b, p in zip(prior, bars[-12:-2]) if b["c"] < p["c"]]
    s10, s50, s200 = sma(c, 10), sma(c, 50), sma(c, 200)
    if not a or last["c"] <= last["o"] or last["c"] <= bars[-2]["c"] or not down_v or last["v"] <= max(down_v): return None
    if not (c[-1] > s50 > s200) or (c[-1] / s10 - 1) * 100 > 5 or ibs(last) < 0.5: return None
    return Signal("pocket_pivot", "long", "swing", last["c"], min(last["l"], s10) - 0.25 * a, last["c"] + 3 * a, 0.65, "pocket pivot", True)

def vcp(bars, ctx=None):
    """Minervini: תבנית טרנד + התכווצויות תנודתיות יורדות + פריצה מעל פיבוט אחרון (חצי גוף, נפח)"""
    n = len(bars)
    if n < 230: return None
    c, last, a = _cl(bars), bars[-1], atr(bars)
    s150, s200, s200_old = sma(c, 150), sma(c, 200), sum(c[-220:-20]) / 200
    hi52, lo52 = max(b["h"] for b in bars[-252:]), min(b["l"] for b in bars[-252:])
    if not a or not (c[-1] > s150 and c[-1] > s200 > s200_old) or c[-1] < 0.75 * hi52 or c[-1] < 1.3 * lo52: return None
    piv = pivots(bars[-120:], 3, 3)
    pairs = []
    for i in range(len(piv) - 1):
        if piv[i][2] == "H" and piv[i + 1][2] == "L": pairs.append((piv[i][1], piv[i + 1][1], piv[i][0]))
    pairs = pairs[-3:]
    if len(pairs) < 2: return None
    depths = [(h - l) / h * 100 for h, l, _ in pairs]
    if not all(depths[i] > depths[i + 1] for i in range(len(depths) - 1)) or depths[-1] > 10 or depths[0] < 5: return None
    res = max(h for h, _, _ in pairs[-2:])
    if not (res < last["c"] <= res * 1.04) or body_beyond(last, res) < BODY_MIN or last["v"] < 1.3 * _vavg(bars): return None
    dry = avg(b["v"] for b in bars[-8:-1]) < 0.9 * _vavg(bars, 50)
    low = pairs[-1][1]
    return Signal("vcp", "long", "swing", last["c"], low - 0.25 * a, last["c"] + 3 * (last["c"] - low), 0.75 + (0.05 if dry else 0),
                  f"contractions {' > '.join(f'{d:.0f}%' for d in depths)}", True)

def cup_handle(bars, ctx=None):
    n = len(bars)
    if n < 130: return None
    last, a = bars[-1], atr(bars)
    win = bars[-130:-3]; off = n - 130
    i1 = max(range(len(win) - 25), key=lambda k: win[k]["h"])               # שפת שמאל
    H1 = win[i1]["h"]
    rest = win[i1 + 8:]
    if len(rest) < 25: return None
    i2 = i1 + 8 + min(range(len(rest)), key=lambda k: rest[k]["l"])         # תחתית הכוס
    L = win[i2]["l"]
    depth = (H1 - L) / H1 * 100
    if not (12 <= depth <= 35) or i2 - i1 < 15: return None
    after = win[i2 + 6:]
    if len(after) < 8: return None
    H3 = max(b["h"] for b in after)                                         # שפה ימנית
    if H3 < 0.9 * H1 or H3 > 1.05 * H1: return None
    i3 = i2 + 6 + max(range(len(after)), key=lambda k: after[k]["h"])
    handle = win[i3:] + bars[-3:-1]
    hl = min(b["l"] for b in handle)
    if not (2 <= len(handle) <= 20) or (H3 - hl) > 0.5 * (H1 - L): return None
    hh = max(b["h"] for b in handle)
    if not (hh < last["c"] <= hh * 1.04) or body_beyond(last, hh) < BODY_MIN or last["v"] < 1.2 * _vavg(bars) or not a: return None
    return Signal("cup_handle", "long", "swing", last["c"], hl - 0.25 * a, hh + (H1 - L), 0.75, f"cup {depth:.0f}% deep", True)

def ttm_squeeze(bars, ctx=None):
    """בולינגר בתוך קלטנר >= 6 ימים, ואז שחרור כלפי מעלה עם מומנטום"""
    if len(bars) < 80: return None
    c, last, a = _cl(bars), bars[-1], atr(bars)
    def squeezed(k):
        sub = bars[:len(bars) - k]
        bb, kc = bollinger(_cl(sub), 20), keltner(sub)
        return bool(bb and kc and bb[1] < kc[1] and bb[2] > kc[2])
    if squeezed(0) or not a or not all(squeezed(k) for k in range(1, 7)): return None
    bb = bollinger(c, 20)
    if last["c"] <= bb[0] or c[-1] <= c[-6] or last["c"] <= last["o"]: return None
    return Signal("ttm_squeeze", "long", "swing", last["c"], bb[0] - 0.5 * a, last["c"] + 3 * a, 0.65, "squeeze fired up", True)

# =============== נרות היפוך בשלושה ===============
def reversal_candles(bars, ctx=None):
    """morning star / piercing / three white soldiers / tweezer bottom - רק ליד תמיכה או שפל 20 יום ו-RSI נמוך"""
    if len(bars) < 60: return None
    a, last, c = atr(bars), bars[-1], _cl(bars)
    r = rsi(c)
    low20 = min(b["l"] for b in bars[-21:-1])
    at_support = min(b["l"] for b in bars[-4:]) <= low20 * 1.03 or any(abs(min(b["l"] for b in bars[-4:]) - lv["price"]) / lv["price"] < 0.015 for lv in key_levels(bars[:-4], min_touches=3))
    if not a or r is None or r > 48 or not at_support: return None
    b1, b2, b3 = bars[-3], bars[-2], bars[-1]
    body = lambda b: abs(b["c"] - b["o"]); rng = lambda b: max(b["h"] - b["l"], 1e-9)
    name = None
    if b1["c"] < b1["o"] and body(b1) > 0.5 * rng(b1) and body(b2) < 0.35 * body(b1) and b3["c"] > b3["o"] and b3["c"] > (b1["o"] + b1["c"]) / 2:
        name = "morning_star"
    elif b2["c"] < b2["o"] and body(b2) > 0.5 * rng(b2) and b3["c"] > b3["o"] and b3["o"] < b2["l"] and (b2["o"] + b2["c"]) / 2 < b3["c"] < b2["o"]:
        name = "piercing_line"
    elif all(x["c"] > x["o"] and body(x) > 0.6 * rng(x) for x in (b1, b2, b3)) and b1["c"] < b2["c"] < b3["c"] and b2["o"] > b1["o"] and b3["o"] > b2["o"] and c[-4] < sma(c, 20):
        name = "three_white_soldiers"
    elif b2["c"] < b2["o"] and b3["c"] > b3["o"] and abs(b2["l"] - b3["l"]) / b3["l"] < 0.002 and body(b3) > 0.5 * rng(b3):
        name = "tweezer_bottom"
    if not name: return None
    stop = min(b["l"] for b in (b1, b2, b3)) - 0.25 * a
    return Signal(name, "long", "swing", last["c"], stop, last["c"] + 2.5 * a, 0.6, f"RSI {r:.0f} at support", last["v"] > _vavg(bars))

# =============== מגמה / רמות / טריז ===============
def ema21_bounce(bars, ctx=None):
    """מגמה חזקה (EMA9>21>50, ADX>20): נסיגה ל-EMA21 וסגירה מעליו בנר ירוק"""
    if len(bars) < 80: return None
    c, last, a = _cl(bars), bars[-1], atr(bars)
    e9, e21, e50, ad = ema(c, 9), ema(c, 21), ema(c, 50), adx(bars)
    if not (a and ad and e9 > e21 > e50) or ad < 20: return None
    if not (last["l"] <= e21 * 1.005 and last["c"] > e21 and last["c"] > last["o"] and ibs(last) > 0.55): return None
    return Signal("ema21_bounce", "long", "swing", last["c"], min(last["l"], e21) - 0.5 * a, last["c"] + 3 * a, 0.6 + (0.05 if ad > 30 else 0), f"ADX {ad:.0f}", False)

def level_bounce(bars, ctx=None):
    """קפיצה מרמת תמיכה עם 3+ נגיעות, נר היפוך ו-RSI לא גבוה"""
    if len(bars) < 80: return None
    last, a, c = bars[-1], atr(bars), _cl(bars)
    cand = bull_candle(bars); r = rsi(c)
    if not (a and cand and r is not None and r < 55): return None
    for lv in sorted(key_levels(bars[:-3], min_touches=3), key=lambda x: -x["touches"]):
        L = lv["price"]
        if bars[-1]["l"] <= L * 1.01 and last["c"] > L and min(b["l"] for b in bars[-3:]) >= L * 0.985 and last["c"] > c[-2]:
            return Signal("level_bounce", "long", "swing", last["c"], L - 0.75 * a, last["c"] + 3 * a, 0.6 + (0.05 if lv["touches"] >= 4 else 0), f"support {L:.2f} x{lv['touches']} {cand}", False)
    return None

def falling_wedge(bars, ctx=None):
    """טריז יורד מתכנס: שיאים ושפלים יורדים, השיאים יורדים מהר יותר; פריצה מעל הקו העליון (חצי גוף)"""
    if len(bars) < 70: return None
    seg = bars[-70:]; piv = pivots(seg, 2, 2)
    hs, ls = [p for p in piv if p[2] == "H"][-3:], [p for p in piv if p[2] == "L"][-3:]
    if len(hs) < 3 or len(ls) < 3: return None
    if not (hs[0][1] > hs[1][1] > hs[2][1] and ls[0][1] > ls[1][1] > ls[2][1]): return None
    sh = (hs[2][1] - hs[0][1]) / (hs[2][0] - hs[0][0]); sl = (ls[2][1] - ls[0][1]) / (ls[2][0] - ls[0][0])
    if sh >= sl or sh >= 0: return None                              # שני הקווים יורדים והעליון תלול יותר (מתכנסים)
    line = hs[2][1] + sh * (len(seg) - 1 - hs[2][0])
    last, a = seg[-1], atr(bars)
    if not (a and line < last["c"] <= line * 1.04) or body_beyond(last, line) < BODY_MIN or last["v"] < 1.1 * _vavg(bars): return None
    return Signal("falling_wedge", "long", "swing", last["c"], ls[2][1] - 0.25 * a, hs[0][1], 0.65, "falling wedge breakout", True)

def pead_pullback(bars, ctx=None):
    """Post-Earnings Drift: גאפ חזק בנפח (דוח) שהחזיק, נסיגה, וממשיכים מעלה"""
    n = len(bars)
    if n < 80: return None
    c, last, a = _cl(bars), bars[-1], atr(bars)
    for g in range(n - 22, n - 4):
        gap = (bars[g]["o"] / bars[g - 1]["c"] - 1) * 100
        base_v = avg(b["v"] for b in bars[max(0, g - 20):g])
        if gap >= 5 and bars[g]["v"] >= 2.5 * base_v and bars[g]["c"] > bars[g]["o"]:
            since = bars[g:]
            if min(b["c"] for b in since) < bars[g]["l"]: return None   # הגאפ נסגר - הוא לא החזיק
            s20 = sma(c, 20)
            near = last["l"] <= max(bars[g]["c"], s20) * 1.02
            if not (a and near and last["c"] > last["o"] and last["c"] > bars[-2]["h"] * 0.995): return None
            lo = min(b["l"] for b in since)
            return Signal("pead_pullback", "long", "swing", last["c"], lo - 0.25 * a, max(b["h"] for b in since) + 3 * a, 0.75, f"post-earnings gap {gap:.0f}% held", True)
    return None

# =============== יום ===============
def red_to_green(b5, ctx=None):
    pc = (ctx or {}).get("prev_close")
    if not pc or len(b5) < 8: return None
    last, vw = b5[-1], vwap(b5)
    if not (b5[0]["o"] <= pc * 0.99) or any(b["c"] > pc for b in b5[:-1]) or not (pc < last["c"] <= pc * 1.015) or body_beyond(last, pc) < BODY_MIN: return None
    if vw and last["c"] < vw or last["v"] < 1.3 * avg(b["v"] for b in b5[:-1]): return None
    lo = min(b["l"] for b in b5)
    return Signal("red_to_green", "long", "day", last["c"], lo - 0.02, last["c"] + 2 * (last["c"] - lo), 0.65, f"reclaimed prev close {pc:.2f}", True)

def hod_break(b5, ctx=None):
    """פריצת שיא היום אחרי התכנסות צמודה של ~6 נרות מתחתיו, בנפח, מעל VWAP (חצי גוף)"""
    if len(b5) < 20: return None
    last = b5[-1]; hod = max(b["h"] for b in b5[:-1])
    cons = b5[-7:-1]
    chi, clo = max(b["h"] for b in cons), min(b["l"] for b in cons)
    if (chi - clo) / last["c"] * 100 > 0.9 or chi < hod * 0.994: return None        # צמוד לשיא ומתכנס
    vw = vwap(b5)
    if not (hod < last["c"] <= hod * 1.01) or body_beyond(last, hod) < BODY_MIN or (vw and last["c"] < vw) or last["v"] < 1.4 * avg(b["v"] for b in b5[:-1]): return None
    h = hod - clo
    return Signal("hod_break", "long", "day", last["c"], clo - 0.02, last["c"] + 2 * max(h, last["c"] * 0.003), 0.65, f"HOD {hod:.2f} after tight base", True)

def vwap_bounce(b5, ctx=None):
    """יום מגמה: רוב היום מעל VWAP, נסיגה ל-VWAP ונר ירוק שחוזר מעליו"""
    if len(b5) < 18: return None
    vws = [vwap(b5[:i + 1]) for i in range(len(b5))]
    vw, last = vws[-1], b5[-1]
    if not vw: return None
    body = list(range(len(b5) - 3))
    above = sum(1 for i in body if vws[i] and b5[i]["c"] > vws[i]) / len(body)
    if above < 0.8 or not (last["l"] <= vw * 1.0015 and last["c"] > vw and last["c"] > last["o"] and ibs(last) > 0.6): return None
    hod = max(b["h"] for b in b5)
    return Signal("vwap_bounce", "long", "day", last["c"], min(last["l"], vw) - 0.03, max(hod, last["c"] * 1.006), 0.6, "trend-day VWAP bounce", True)

def intraday_flag(b5, ctx=None):
    s = P.flag_long(b5, min_pole_pct=1.5, max_pole=8, min_flag=3, max_flag=8, min_bars=20)
    if not s: return None
    s.name, s.kind = "intraday_flag", "day"
    return s

SWING = {"rsi2_reversion": rsi2_reversion, "ibs_reversion": ibs_reversion, "donchian55": donchian55, "donchian20": donchian20,
         "nr7_breakout": nr7_breakout, "pocket_pivot": pocket_pivot, "vcp": vcp, "cup_handle": cup_handle, "ttm_squeeze": ttm_squeeze,
         "reversal_candles": reversal_candles, "ema21_bounce": ema21_bounce, "level_bounce": level_bounce, "falling_wedge": falling_wedge,
         "pead_pullback": pead_pullback}
DAY = {"red_to_green": red_to_green, "hod_break": hod_break, "vwap_bounce": vwap_bounce, "intraday_flag": intraday_flag}

for _k, _f in SWING.items(): P.LONG_DETECTORS[_k] = (lambda f: (lambda b, c: f(b, c)))(_f)
P.DAY_DETECTORS.update(DAY)
