"""מאפיינים מספריים של הגרף בזמן האיתות - משמשים גם ב-research (למידה מהיסטוריה) וגם בבוט (סינון חי)."""
from indicators import sma, rsi, atr, adx, avg, pct_return, ibs

NAMES = ["dist20", "dist50", "adx", "rsi", "rvol", "atr_pct", "ret5", "ret20", "ret60", "gap", "body_atr", "ibs", "pos20"]

def compute(bars):
    """dict של מאפיינים לנר האחרון. ערך חסר = None"""
    if len(bars) < 65: return {}
    c = [b["c"] for b in bars]; last = bars[-1]
    a, s20, s50 = atr(bars), sma(c, 20), sma(c, 50)
    hi20, lo20 = max(b["h"] for b in bars[-20:]), min(b["l"] for b in bars[-20:])
    v20 = avg(b["v"] for b in bars[-21:-1])
    f = {
        "dist20": (c[-1] - s20) / a if a and s20 else None,
        "dist50": (c[-1] / s50 - 1) * 100 if s50 else None,
        "adx": adx(bars), "rsi": rsi(c),
        "rvol": last["v"] / v20 if v20 else None,
        "atr_pct": a / c[-1] * 100 if a else None,
        "ret5": pct_return(c, 5), "ret20": pct_return(c, 20), "ret60": pct_return(c, 60),
        "gap": (last["o"] / bars[-2]["c"] - 1) * 100,
        "body_atr": abs(last["c"] - last["o"]) / a if a else None,
        "ibs": ibs(last),
        "pos20": (c[-1] - lo20) / (hi20 - lo20) if hi20 > lo20 else 0.5,
    }
    return {k: (round(v, 4) if isinstance(v, (int, float)) else None) for k, v in f.items()}

def passes(feat, rules):
    """rules: [{'f': name, 'op': '>='|'<=', 'v': number}]; מאפיין חסר = לא חוסמים"""
    for r in rules or []:
        x = feat.get(r["f"])
        if x is None: continue
        if (r["op"] == ">=" and x < r["v"]) or (r["op"] == "<=" and x > r["v"]): return False
    return True
