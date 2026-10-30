"""ספירת 'כלים' בגרף: עסקה נכנסת רק עם לפחות 3 כלים (כלל המחברת).
תבנית גרף = 2, פריצה (חצי גוף מעבר לקו) = 1, נפח = 1, דגל = 1, נר מהפך = 1, מגמה לכיוון העסקה = 1,
רמת תמיכה/התנגדות = 1, מומנטום (RSI+MACD) = 1. הבוט מוסיף: טיימפריים שבועי מסכים = 1, שוק+סקטור מיושרים = 1."""
from indicators import sma, rsi, macd, vwap, avg
from structure import key_levels

CHART_PATTERNS = {"head_shoulders", "inverse_head_shoulders", "double_top", "double_bottom", "triple_bottom", "cup_handle", "vcp",
                  "ascending_triangle", "descending_triangle", "symmetrical_triangle", "rising_wedge", "falling_wedge", "base_breakout",
                  "channel_bounce", "island", "island_bottom", "dead_cat_bounce", "range_breakdown", "bollinger_squeeze", "ttm_squeeze"}
FLAGS = {"flag", "bear_flag", "pennant", "intraday_flag", "higher_low_breakout"}
CANDLES = {"evening_star", "morning_star", "bearish_engulfing_top", "bullish_engulfing_support", "shooting_star", "hammer_support", "three_black_crows",
           "three_white_soldiers", "three_inside_up", "bullish_harami_support", "piercing_line", "tweezer_bottom", "three_line_strike_bull",
           "outside_day_reversal", "upthrust", "spring_reversal", "inside_bar_breakout", "nr7_breakout"}
BREAKS = CHART_PATTERNS - {"channel_bounce", "dead_cat_bounce", "bollinger_squeeze", "ttm_squeeze"} | FLAGS

def _base(name): return name.replace("_15m", "").replace("_W", "")

def count(sig, bars, kind="swing"):
    """(מספר כלים, רשימת שמות). סופרים רק מה שהגרף עצמו מראה"""
    n, why = _base(sig.name), []
    long = sig.side == "long"
    pts = 0
    if n in CHART_PATTERNS: pts += 2; why.append("pattern(2)")
    elif n in FLAGS: pts += 1; why.append("flag")
    elif n in CANDLES: pts += 1; why.append("candle")
    else: pts += 1; why.append("signal")
    brk = n in BREAKS or "break" in n or n in ("orb", "gap_and_go", "pdh_break", "reclaim") or n.endswith("_thrust")
    if not brk and len(bars) > 22:
        last = bars[-1]
        if long and last["c"] > max(b["h"] for b in bars[-21:-1]) and last["c"] > last["o"] and (last["c"] - max(last["o"], max(b["h"] for b in bars[-21:-1]))) >= 0.5 * (last["c"] - last["o"]): brk = True
        if not long and last["c"] < min(b["l"] for b in bars[-21:-1]) and last["c"] < last["o"] and (min(last["o"], min(b["l"] for b in bars[-21:-1])) - last["c"]) >= 0.5 * (last["o"] - last["c"]): brk = True
    if brk: pts += 1; why.append("breakout")
    if sig.volume_ok: pts += 1; why.append("volume")
    c = [b["c"] for b in bars]
    try:
        if kind == "day":
            vw = vwap(bars)
            if vw and ((long and c[-1] > vw) or (not long and c[-1] < vw)): pts += 1; why.append("vwap")
        else:
            s50, sp = sma(c, 50), sma(c[:-5], 50) if len(c) > 56 else None
            if s50 and sp and ((long and c[-1] > s50 and s50 > sp) or (not long and c[-1] < s50 and s50 < sp)): pts += 1; why.append("trend")
            lv = key_levels(bars)
            if any(c[-1] * 0.985 <= L["price"] <= c[-1] * 1.005 for L in lv) if long else any(c[-1] * 0.995 <= L["price"] <= c[-1] * 1.015 for L in lv):
                pts += 1; why.append("level")
        r, m = rsi(c), macd(c)
        if r is not None and m and ((long and r > 50 and m[2] > 0) or (not long and r < 50 and m[2] < 0)): pts += 1; why.append("momentum")
    except Exception:
        pass
    return pts, why
