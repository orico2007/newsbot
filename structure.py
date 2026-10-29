"""מבנה שוק: פיבוטים, מגמה (HH/HL), רמות מפתח, פיבונאצ'י"""

def pivots(bars, left=3, right=3):
    """[(index, price, 'H'|'L')] - פיבוטים מאושרים בלבד (right ברים אחרי)"""
    out = []
    for i in range(left, len(bars) - right):
        hi, lo = bars[i]["h"], bars[i]["l"]
        if all(hi > bars[j]["h"] for j in range(i - left, i)) and all(hi >= bars[j]["h"] for j in range(i + 1, i + right + 1)):
            out.append((i, hi, "H"))
        if all(lo < bars[j]["l"] for j in range(i - left, i)) and all(lo <= bars[j]["l"] for j in range(i + 1, i + right + 1)):
            out.append((i, lo, "L"))
    return out

def trend_structure(bars, left=3, right=3):
    """מגמת עלייה = שיא גבוה יותר + שפל גבוה יותר (כמו במחברת); ירידה = הפוך"""
    piv = pivots(bars, left, right)
    highs = [p for p in piv if p[2] == "H"][-2:]
    lows = [p for p in piv if p[2] == "L"][-2:]
    res = {"trend": "range", "last_low": lows[-1][1] if lows else None, "last_high": highs[-1][1] if highs else None,
           "last_low_idx": lows[-1][0] if lows else None, "last_high_idx": highs[-1][0] if highs else None}
    if len(highs) == 2 and len(lows) == 2:
        if highs[1][1] > highs[0][1] and lows[1][1] > lows[0][1]: res["trend"] = "up"
        elif highs[1][1] < highs[0][1] and lows[1][1] < lows[0][1]: res["trend"] = "down"
    return res

def key_levels(bars, tol=0.006, min_touches=3, lookback=160, left=2, right=2):
    """רמות תמיכה/התנגדות: אשכולות פיבוטים (>=3 נגיעות)"""
    seg = bars[-lookback:]
    prices = sorted(p[1] for p in pivots(seg, left, right))
    groups, cur = [], []
    for p in prices:
        if cur and p <= (sum(cur) / len(cur)) * (1 + tol): cur.append(p)
        else:
            if cur: groups.append(cur)
            cur = [p]
    if cur: groups.append(cur)
    return [{"price": sum(g) / len(g), "touches": len(g)} for g in groups if len(g) >= min_touches]

def fib_levels(low, high):
    """רמות נסיגה 38.2/50/61.8 בעלייה מ-low ל-high"""
    d = high - low
    return {"38.2": high - 0.382 * d, "50": high - 0.5 * d, "61.8": high - 0.618 * d}
