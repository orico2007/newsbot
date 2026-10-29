"""אסטרטגיות נוספות (v5). אותו מבנה: (bars, ctx) -> Signal|None, ללונג; שורט במראה."""
import patterns as P
from patterns import Signal, body_beyond, BODY_MIN, bull_candle, _vavg
from indicators import sma, ema, rsi, atr, avg, adx, keltner, ibs, vwap, macd, stoch, anchored_vwap, ichimoku
from structure import pivots, trend_structure

def _cl(bars): return [b["c"] for b in bars]

# ---------------- סווינג ----------------
def spring_reversal(bars, ctx=None):
    """Turtle Soup / Wyckoff spring: שבירת שפל 20 יום ו"בריחה" - חוזרים וסוגרים מעליו בנר ירוק חזק"""
    if len(bars) < 60: return None
    last, a = bars[-1], atr(bars)
    ref = min(b["l"] for b in bars[-24:-3]); lo3 = min(b["l"] for b in bars[-3:])
    if not a or lo3 >= ref or last["c"] <= ref or last["c"] <= last["o"] or ibs(last) < 0.6: return None
    rng_hi = max(b["h"] for b in bars[-24:-3])
    return Signal("spring_reversal", "long", "swing", last["c"], lo3 - 0.25 * a, max((rng_hi + ref) / 2, last["c"] + 2 * a), 0.65, f"failed break of {ref:.2f}", last["v"] > _vavg(bars))

def higher_low_breakout(bars, ctx=None):
    """שבירת מבנה בעלייה: HH/HL ואז סגירה מעל השיא הקודם (חצי גוף, נפח)"""
    if len(bars) < 60: return None
    st = trend_structure(bars[:-1])
    last, a = bars[-1], atr(bars)
    if st["trend"] != "up" or not a or st["last_high"] is None: return None
    hi, lo = st["last_high"], st["last_low"]
    if not (hi < last["c"] <= hi * 1.04) or body_beyond(last, hi) < BODY_MIN or last["v"] < 1.1 * _vavg(bars): return None
    return Signal("higher_low_breakout", "long", "swing", last["c"], lo - 0.25 * a, last["c"] + (hi - lo), 0.65, f"breaks {hi:.2f}, HL {lo:.2f}", True)

def down_trendline_break(bars, ctx=None):
    """פריצת קו מגמה יורד (אלכסוני) שנבנה משני שיאים יורדים, חצי גוף מעל הקו"""
    if len(bars) < 70: return None
    seg = bars[-90:]; piv = pivots(seg, 3, 3)
    hs = [p for p in piv if p[2] == "H"][-2:]
    if len(hs) < 2 or hs[0][1] <= hs[1][1] or hs[1][0] - hs[0][0] < 8: return None
    slope = (hs[1][1] - hs[0][1]) / (hs[1][0] - hs[0][0])
    line = hs[1][1] + slope * (len(seg) - 1 - hs[1][0])
    last, a = seg[-1], atr(bars)
    if not a or any(b["c"] > hs[1][1] + slope * (i - hs[1][0]) for i, b in enumerate(seg[hs[1][0] + 1:-1], start=hs[1][0] + 1)): return None
    if not (line < last["c"] <= line * 1.04) or body_beyond(last, line) < BODY_MIN or last["v"] < 1.1 * _vavg(bars): return None
    lows = [p for p in piv if p[2] == "L" and p[0] > hs[0][0]]
    stop = (lows[-1][1] if lows else min(b["l"] for b in seg[-10:])) - 0.25 * a
    return Signal("down_trendline_break", "long", "swing", last["c"], stop, last["c"] + (hs[0][1] - stop), 0.65, f"trendline {line:.2f}", True)

def channel_bounce(bars, ctx=None):
    """קפיצה מהקו התחתון של ערוץ עולה (3 שפלים עולים) עם נר היפוך"""
    if len(bars) < 80: return None
    seg = bars[-100:]; piv = pivots(seg, 3, 3)
    ls = [p for p in piv if p[2] == "L"][-3:]
    if len(ls) < 3 or not (ls[0][1] < ls[1][1] < ls[2][1]) or ls[2][0] - ls[0][0] < 15: return None
    slope = (ls[2][1] - ls[0][1]) / (ls[2][0] - ls[0][0])
    line = ls[2][1] + slope * (len(seg) - 1 - ls[2][0])
    last, a = seg[-1], atr(bars)
    cand = bull_candle(seg)
    if not (a and cand and abs(last["l"] - line) / line < 0.012 and last["c"] > line): return None
    hs = [p for p in piv if p[2] == "H"][-2:]
    top = max(h[1] for h in hs) if hs else last["c"] + 3 * a
    return Signal("channel_bounce", "long", "swing", last["c"], line - 0.75 * a, max(top, last["c"] + 2 * a), 0.6, f"rising channel {cand}", False)

def capitulation_reversal(bars, ctx=None):
    """שיא בנפח וירידה חדה (10 ימים), RSI נמוך, והנר נסגר בחצי העליון: ניקוי מוכרים"""
    if len(bars) < 40: return None
    c, last, a, r = _cl(bars), bars[-1], atr(bars), rsi(_cl(bars))
    drop = (c[-1] / max(c[-11:-1]) - 1) * 100
    if not a or r is None or drop > -10 or r > 32 or last["v"] < 2.5 * _vavg(bars) or (last["h"] - last["l"]) < 1.8 * a or ibs(last) < 0.5: return None
    return Signal("capitulation_reversal", "long", "swing", last["c"], last["l"] - 0.25 * a, last["c"] + abs(last["c"] - max(c[-11:-1])) * 0.5, 0.6, f"drop {drop:.0f}% RSI {r:.0f} vol {last['v'] / _vavg(bars):.1f}x", True)

def golden_cross(bars, ctx=None):
    if len(bars) < 215: return None
    c, a, last = _cl(bars), atr(bars), bars[-1]
    x = [sma(c[:len(c) - k], 50) - sma(c[:len(c) - k], 200) for k in range(0, 4)]
    ad = adx(bars)
    if not (a and ad and x[0] > 0 and x[3] <= 0 and ad > 15 and last["c"] > last["o"] and last["c"] > sma(c, 200)): return None
    return Signal("golden_cross", "long", "swing", last["c"], last["c"] - 2.5 * a, last["c"] + 5 * a, 0.55, f"SMA50 over SMA200, ADX {ad:.0f}", False)

def macd_pullback(bars, ctx=None):
    """MACD מתהפך כלפי מעלה מתחת לאפס בזמן שהמגמה הראשית עולה (חזרה אחרי נסיגה)"""
    if len(bars) < 210: return None
    c, a = _cl(bars), atr(bars)
    m = macd(c)
    if not (a and m): return None
    line, sig, h, hp = m
    if not (sma(c, 50) > sma(c, 200) and c[-1] > sma(c, 50) and line < 0 and hp < 0 <= h and c[-1] > bars[-1]["o"]): return None
    return Signal("macd_pullback", "long", "swing", c[-1], min(b["l"] for b in bars[-5:]) - 0.25 * a, c[-1] + 3 * a, 0.55, "MACD cross up below zero in uptrend", False)

def stoch_oversold(bars, ctx=None):
    if len(bars) < 60: return None
    c, a, s = _cl(bars), atr(bars), stoch(bars)
    if not (a and s): return None
    k, d, kp, dp = s
    if not (c[-1] > sma(c, 50) and kp < 20 and kp <= dp and k > d and k < 40): return None
    return Signal("stoch_oversold", "long", "swing", c[-1], min(b["l"] for b in bars[-4:]) - 0.25 * a, c[-1] + 2.5 * a, 0.5, f"%K {k:.0f} crossed up from oversold", False)

def momentum_burst(bars, ctx=None):
    """Stockbee: +4% ביום בנפח גבוה מאתמול אחרי כמה ימים של צמצום"""
    if len(bars) < 40: return None
    last, prev, a = bars[-1], bars[-2], atr(bars)
    chg = (last["c"] / prev["c"] - 1) * 100
    prior = bars[-8:-1]
    tight = (max(b["h"] for b in prior) - min(b["l"] for b in prior)) / prev["c"] * 100
    hi5 = max(b["h"] for b in bars[-6:-1])
    if not a or chg < 4 or last["v"] <= prev["v"] or last["v"] < 1.5 * _vavg(bars) or tight > 9 or ibs(last) < 0.7 or body_beyond(last, hi5) < BODY_MIN: return None
    return Signal("momentum_burst", "long", "swing", last["c"], last["l"] - 0.1 * a, last["c"] + 4 * a, 0.6, f"+{chg:.1f}% burst after {tight:.0f}% range", True)

def rsi_divergence(bars, ctx=None):
    """סטייה חיובית: מחיר שופל נמוך יותר, RSI שפל גבוה יותר + נר היפוך"""
    if len(bars) < 80: return None
    seg = bars[-90:]; ls = [p for p in pivots(seg, 3, 3) if p[2] == "L"][-2:]
    if len(ls) < 2 or ls[1][0] - ls[0][0] < 8 or len(seg) - 1 - ls[1][0] > 8: return None
    c = _cl(bars); off = len(bars) - len(seg)
    r0, r1 = rsi(c[:off + ls[0][0] + 1]), rsi(c[:off + ls[1][0] + 1])
    last, a = seg[-1], atr(bars)
    if not (a and r0 is not None and r1 is not None) or not (ls[1][1] < ls[0][1] and r1 > r0 + 3 and r1 < 42): return None
    if not (bull_candle(seg) or last["c"] > max(b["h"] for b in seg[-4:-1])): return None
    top = max(b["h"] for b in seg[ls[0][0]:ls[1][0] + 1])
    return Signal("rsi_divergence", "long", "swing", last["c"], ls[1][1] - 0.25 * a, max(top, last["c"] + 2 * a), 0.65, f"RSI {r0:.0f}->{r1:.0f} on lower low", False)

def avwap_reclaim(bars, ctx=None):
    """VWAP מעוגן לשפל המשמעותי (120 נרות): סגירה מעליו מלמטה, חצי גוף, בנפח"""
    if len(bars) < 130: return None
    seg = bars[-120:]; i0 = len(bars) - 120 + min(range(120), key=lambda k: seg[k]["l"])
    if len(bars) - i0 < 15: return None
    av, last, prev, a = anchored_vwap(bars, i0), bars[-1], bars[-2], atr(bars)
    if not (av and a) or prev["c"] >= av or not (av < last["c"] <= av * 1.04) or body_beyond(last, av) < BODY_MIN or last["v"] < 1.2 * _vavg(bars): return None
    return Signal("avwap_reclaim", "long", "swing", last["c"], min(b["l"] for b in bars[-3:]) - 0.25 * a, last["c"] + 3 * a, 0.6, f"reclaims AVWAP {av:.2f}", True)

def pullback_reversal_day(bars, ctx=None):
    """מגמה עולה, 3 סגירות יורדות ברצף, ואז יום היפוך שסוגר מעל השיא של אתמול"""
    if len(bars) < 210: return None
    c, a, last = _cl(bars), atr(bars), bars[-1]
    if not (a and c[-1] > sma(c, 200) and sma(c, 50) > sma(c, 200)): return None
    if not (c[-2] < c[-3] < c[-4] < c[-5]) or (max(c[-12:-1]) / c[-2] - 1) * 100 < 3: return None
    if not (last["c"] > bars[-2]["h"] and last["c"] > last["o"]): return None
    return Signal("pullback_reversal_day", "long", "swing", last["c"], min(b["l"] for b in bars[-4:]) - 0.25 * a, last["c"] + 2.5 * a, 0.6, "3 down closes then reversal day", False)

def gap_down_reclaim(bars, ctx=None):
    """פתיחה בגאפ-דאון מתחת לשפל אתמול ואז סגירה מעל סגירת אתמול בנפח: מלכודת דובים"""
    if len(bars) < 40: return None
    last, prev, a = bars[-1], bars[-2], atr(bars)
    if not a or last["o"] > prev["l"] * 0.98 or last["c"] <= prev["c"] or last["v"] < 1.5 * _vavg(bars) or ibs(last) < 0.6: return None
    return Signal("gap_down_reclaim", "long", "swing", last["c"], last["l"] - 0.1 * a, max(prev["h"], last["c"] + 2 * a), 0.65, f"gap {(last['o'] / prev['c'] - 1) * 100:.1f}% reclaimed", True)

def keltner_thrust(bars, ctx=None):
    if len(bars) < 70: return None
    last, a, ad = bars[-1], atr(bars), adx(bars)
    kc, prev_kc = keltner(bars), keltner(bars[:-1])
    if not (a and ad and kc and prev_kc) or ad < 25 or bars[-2]["c"] > prev_kc[1] or not (kc[1] < last["c"] <= kc[1] * 1.04) or body_beyond(last, kc[1]) < BODY_MIN or last["v"] < 1.2 * _vavg(bars): return None
    return Signal("keltner_thrust", "long", "swing", last["c"], kc[0], last["c"] + 3 * a, 0.55, f"ADX {ad:.0f}", True)

def ichimoku_breakout(bars, ctx=None):
    if len(bars) < 90: return None
    ich, last, prev, a = ichimoku(bars), bars[-1], bars[-2], atr(bars)
    if not (ich and a): return None
    tenkan, kijun, top, bot = ich
    pich = ichimoku(bars[:-1])
    if not pich or prev["c"] > pich[2] or tenkan <= kijun or not (top < last["c"] <= top * 1.04) or body_beyond(last, top) < BODY_MIN: return None
    return Signal("ichimoku_breakout", "long", "swing", last["c"], max(bot, last["c"] - 3 * a), last["c"] + 4 * a, 0.6, f"above cloud {top:.2f}", last["v"] > _vavg(bars))

# ---------------- יום ----------------
def pdh_break(b5, ctx=None):
    """פריצת שיא אתמול (חצי גוף, מעל VWAP, בנפח); בשורט: שבירת שפל אתמול"""
    ph = (ctx or {}).get("prev_high")
    if not ph or len(b5) < 8: return None
    last, vw = b5[-1], vwap(b5)
    if any(b["c"] > ph for b in b5[:-1]) or not (ph < last["c"] <= ph * 1.012) or body_beyond(last, ph) < BODY_MIN: return None
    if (vw and last["c"] < vw) or last["v"] < 1.3 * avg(b["v"] for b in b5[:-1]): return None
    lo = min(b["l"] for b in b5[-6:])
    return Signal("pdh_break", "long", "day", last["c"], min(lo, ph * 0.997) - 0.02, last["c"] + 2 * max(last["c"] - lo, last["c"] * 0.004), 0.65, f"prev-day high {ph:.2f}", True)

def ema9_pullback_5m(b5, ctx=None):
    if len(b5) < 30: return None
    c, last, vw = _cl(b5), b5[-1], vwap(b5)
    e9, e20 = ema(c, 9), ema(c, 20)
    if not (e9 and e20 and vw) or not (e9 > e20 and c[-1] > vw) or not (last["l"] <= e20 * 1.001 and last["c"] > e9 and last["c"] > last["o"]): return None
    hod = max(b["h"] for b in b5)
    return Signal("ema9_pullback_5m", "long", "day", last["c"], min(last["l"], e20) - 0.03, max(hod, last["c"] * 1.005), 0.6, "pullback to EMA20 in 5m uptrend", True)

def afternoon_breakout(b5, ctx=None):
    """פריצת טווח הצהריים (11:30-13:30 ET) אחרי 14:00, בנפח, מעל VWAP ובמגמת יום עולה"""
    if len(b5) < 55: return None
    lunch = b5[24:48]; last, vw = b5[-1], vwap(b5)
    lh, ll = max(b["h"] for b in lunch), min(b["l"] for b in lunch)
    if (lh - ll) / ll * 100 > 2.0 or any(b["c"] > lh for b in b5[48:-1]): return None
    if not (lh < last["c"] <= lh * 1.01) or body_beyond(last, lh) < BODY_MIN or (vw and last["c"] < vw) or last["c"] < b5[0]["o"] or last["v"] < 1.4 * avg(b["v"] for b in lunch): return None
    return Signal("afternoon_breakout", "long", "day", last["c"], ll - 0.02, last["c"] + 2 * (lh - ll), 0.6, f"lunch range {ll:.2f}-{lh:.2f}", True)

def gap_reversal(b5, ctx=None):
    """גאפ-דאון >=3% שמתהפך: חוצה את שיא 30 הדקות הראשונות מעל VWAP (בשורט: גאפ-אפ שנכשל)"""
    pc = (ctx or {}).get("prev_close")
    if not pc or len(b5) < 10 or b5[0]["o"] > pc * 0.97: return None
    first30 = b5[:6]; h30 = max(b["h"] for b in first30); last, vw = b5[-1], vwap(b5)
    if any(b["c"] > h30 for b in b5[6:-1]) or not (h30 < last["c"] <= h30 * 1.012) or body_beyond(last, h30) < BODY_MIN or (vw and last["c"] < vw) or last["v"] < 1.2 * avg(b["v"] for b in b5[:-1]): return None
    lo = min(b["l"] for b in b5)
    return Signal("gap_reversal", "long", "day", last["c"], lo - 0.02, min(pc, last["c"] + 2 * (last["c"] - lo)) if pc > last["c"] else last["c"] + 2 * (last["c"] - lo), 0.65, f"gap {((b5[0]['o'] / pc) - 1) * 100:.1f}% reversing", True)

SWING = {"spring_reversal": spring_reversal, "higher_low_breakout": higher_low_breakout, "down_trendline_break": down_trendline_break,
         "channel_bounce": channel_bounce, "capitulation_reversal": capitulation_reversal, "golden_cross": golden_cross, "macd_pullback": macd_pullback,
         "stoch_oversold": stoch_oversold, "momentum_burst": momentum_burst, "rsi_divergence": rsi_divergence, "avwap_reclaim": avwap_reclaim,
         "pullback_reversal_day": pullback_reversal_day, "gap_down_reclaim": gap_down_reclaim, "keltner_thrust": keltner_thrust,
         "ichimoku_breakout": ichimoku_breakout}
DAY = {"pdh_break": pdh_break, "ema9_pullback_5m": ema9_pullback_5m, "afternoon_breakout": afternoon_breakout, "gap_reversal": gap_reversal}
for _k, _f in SWING.items(): P.LONG_DETECTORS[_k] = (lambda f: (lambda b, c: f(b, c)))(_f)
P.DAY_DETECTORS.update(DAY)
