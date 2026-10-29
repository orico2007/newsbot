"""ניתוח גרף כחוקים קשיחים בקוד (לא תמונות): אישור כניסה ליום ולסווינג."""
from indicators import sma, rsi, atr, vwap, vol_spike

def intraday_check(bars5, side, cfg):
    """אישור גרף לכניסת Day: מחיר מול VWAP, זינוק בנפח, RSI לא קיצוני."""
    if len(bars5) < 3:
        return False, "not enough intraday bars", {}
    last = bars5[-1]["c"]
    vw = vwap(bars5)
    closes = [b["c"] for b in bars5]
    r = rsi(closes) if len(closes) >= 15 else None
    spike = vol_spike(bars5)
    snap = {"price": round(last, 2), "vwap": round(vw, 2) if vw else None,
            "rsi": round(r, 1) if r is not None else None, "vol_spike": round(spike, 2) if spike else None}
    if cfg.get("require_vwap_side", True) and vw:
        if side == "long" and last <= vw:
            return False, "price below VWAP", snap
        if side == "short" and last >= vw:
            return False, "price above VWAP", snap
    if r is not None:
        if side == "long" and r > cfg["max_rsi_long"]:
            return False, f"RSI {r:.0f} overbought", snap
        if side == "short" and r < cfg["min_rsi_short"]:
            return False, f"RSI {r:.0f} oversold", snap
    if spike is not None and spike < cfg["min_rel_volume"]:
        return False, f"volume spike {spike:.1f}x too low", snap
    return True, "ok", snap

def daily_snapshot(daily):
    closes = [b["c"] for b in daily]
    return {"close": closes[-1], "sma20": sma(closes, 20), "sma50": sma(closes, 50),
            "rsi": rsi(closes), "atr": atr(daily), "high20": max(b["h"] for b in daily[-20:])}

def trend_ok(daily, side):
    """מגמה יומית לסווינג על חדשות: מעל/מתחת SMA50 ו-SMA20 מול SMA50"""
    if len(daily) < 55:
        return False, "not enough daily bars", {}
    s = daily_snapshot(daily)
    if s["atr"] is None:
        return False, "no ATR", s
    if side == "long" and not (s["close"] > s["sma50"] and s["sma20"] > s["sma50"]):
        return False, "no uptrend", s
    if side == "short" and not (s["close"] < s["sma50"] and s["sma20"] < s["sma50"]):
        return False, "no downtrend", s
    return True, "ok", s

def swing_scan_ok(daily, cfg):
    """סריקת סווינג ללונג: מגמת עלייה + נסיגה מבוקרת + RSI בטווח"""
    if len(daily) < 55:
        return False, "not enough daily bars", {}
    s = daily_snapshot(daily)
    if s["atr"] is None or s["rsi"] is None:
        return False, "no indicators", s
    if not (s["close"] > s["sma50"] and s["sma20"] > s["sma50"]):
        return False, "no uptrend", s
    if not (cfg["rsi_min"] <= s["rsi"] <= cfg["rsi_max"]):
        return False, f"RSI {s['rsi']:.0f} out of range", s
    pull = (s["high20"] - s["close"]) / s["high20"] * 100
    s["pullback_pct"] = round(pull, 1)
    if not (cfg["min_pullback_pct"] <= pull <= cfg["max_pullback_pct"]):
        return False, f"pullback {pull:.1f}% out of range", s
    return True, "ok", s

def fundamentals_ok(f, cfg):
    if not f or f.get("rev_yoy") is None:
        return False
    if f["rev_yoy"] < cfg["min_revenue_yoy_pct"]:
        return False
    return f.get("eps_positive") is not False
