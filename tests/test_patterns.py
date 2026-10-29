import patterns as P
from structure import pivots, trend_structure, key_levels, fib_levels
from tests.helpers import bar

def B(o, h, l, c, v=1000): return {"t": "x", "o": o, "h": h, "l": l, "c": c, "v": v}

def flat(n, price=50, v=1000, sp=0.2):
    return [B(price, price + sp, price - sp, price, v) for _ in range(n)]

def ramp(a, b, n, v=1000, sp=0.2):
    out = []
    for i in range(n):
        c = a + (b - a) * (i + 1) / n
        out.append(B(c, c + sp, c - sp, c, v))
    return out

# ---- structure ----
def test_pivots_and_trend_up():
    bars = []
    for lo, hi in [(10, 14), (12, 18), (15, 22), (19, 26)]:
        bars += ramp(lo, hi, 6) + ramp(hi, lo + 2, 6)
    bars += ramp(bars[-1]["c"], bars[-1]["c"] + 3, 4)
    assert trend_structure(bars)["trend"] == "up"

def test_trend_down():
    bars = []
    for lo, hi in [(19, 26), (15, 22), (12, 18), (9, 14)]:
        bars += ramp(hi, lo, 6) + ramp(lo, hi - 3, 6)
    bars += ramp(bars[-1]["c"], bars[-1]["c"] - 3, 4)
    assert trend_structure(bars)["trend"] == "down"

def test_key_levels_cluster():
    bars = []
    for _ in range(4):
        bars += ramp(50, 60, 5) + ramp(60, 50, 5)
    lv = key_levels(bars)
    assert any(abs(l["price"] - 60.2) < 0.6 and l["touches"] >= 3 for l in lv)

def test_fib():
    f = fib_levels(100, 200)
    assert abs(f["50"] - 150) < 1e-9 and abs(f["61.8"] - 138.2) < 1e-9

# ---- mirror ----
def test_mirror_roundtrip():
    bars = ramp(50, 60, 30)
    mb, k2 = P.mirror(bars)
    assert all(m["h"] >= m["l"] for m in mb)
    s = P.Signal("x", "long", "swing", mb[-1]["c"], mb[-1]["c"] * 0.95, mb[-1]["c"] * 1.1)
    P.unmirror(s, k2)
    assert s.side == "short" and abs(s.price - 60) < 1e-6 and s.stop > s.price > s.target

# ---- candles ----
def test_hammer():
    bars = flat(5) + [B(50, 50.1, 48, 50.05)]
    assert P.bull_candle(bars) == "hammer"

def test_engulfing():
    bars = flat(5) + [B(50.5, 50.6, 49.9, 50.0), B(49.9, 51.2, 49.8, 51.0)]
    assert P.bull_candle(bars) == "bullish_engulfing"

def test_no_candle_on_flat():
    assert P.bull_candle(flat(10)) is None

# ---- flag ----
def make_flag(breakout=True):
    bars = flat(30, 50) + ramp(50, 62, 6, v=3000)
    bars += [B(61.5, 62.0, 60.8, 61.2, 800), B(61.2, 61.8, 60.6, 61.0, 700), B(61.0, 61.6, 60.5, 60.9, 600), B(60.9, 61.5, 60.4, 61.0, 600)]
    bars += [B(61.3, 62.6, 61.2, 62.4, 1500)] if breakout else [B(61.0, 61.5, 60.6, 61.0, 600)]
    return bars

def test_flag_detects():
    s = P.flag_long(make_flag())
    assert s and s.name == "flag" and s.target > s.price > s.stop

def test_flag_needs_breakout():
    assert P.flag_long(make_flag(False)) is None

# ---- base breakout ----
def test_base_breakout():
    bars = ramp(40, 50, 30) + [B(50 + (0.5 if i % 2 else -0.5), 51 + (0 if i % 2 else 0), 49, 50, 1000) for i in range(25)]
    bars += [B(50.5, 52.2, 50.4, 52.0, 2500)]
    s = P.base_breakout_long(bars)
    assert s and s.name == "base_breakout" and s.volume_ok

def test_base_breakout_low_volume_rejected():
    bars = ramp(40, 50, 30) + [B(50, 51, 49, 50, 1000) for _ in range(25)] + [B(50.5, 52.2, 50.4, 52.0, 1000)]
    assert P.base_breakout_long(bars) is None

# ---- double bottom ----
def test_double_bottom():
    bars = flat(40, 60) + ramp(60, 50, 8) + ramp(50, 56, 7) + ramp(56, 50.3, 7) + ramp(50.3, 56, 7)
    bars += [B(56.2, 57.5, 56.1, 57.2, 2000)]
    bars = [dict(b, v=1000) if b["v"] != 2000 else b for b in bars]
    s = P.double_bottom_long(bars)
    assert s and s.name == "double_bottom" and s.target > s.price > s.stop

# ---- gaps ----
def test_breakaway_gap():
    bars = [B(50 + (0.3 if i % 2 else -0.3), 50.8, 49.2, 50.0, 1000) for i in range(30)]
    bars += [B(52.0, 53.0, 51.9, 52.8, 4000)]
    s = P.gap_breakaway_long(bars)
    assert s and s.name == "breakaway_gap"

def test_gap_down_not_long():
    bars = flat(30) + [B(48, 48.5, 47.5, 48.2, 4000)]
    assert P.gap_breakaway_long(bars) is None

# ---- high52 ----
def test_high52():
    bars = ramp(40, 50, 200) + flat(30, 50.0) + [B(50.3, 52, 50.2, 51.8, 3000)]
    s = P.high52_breakout_long(bars)
    assert s and s.name == "high52_breakout" and s.stop < s.price < s.target

# ---- detect_all with shorts ----
def test_detect_all_shorts_from_mirror():
    # mirrored flag-like breakdown must produce a short
    up = make_flag()
    mb, k2 = P.mirror(up)
    # mirror of mirror-of-bearish: feed the mirrored series; its mirror is the original long flag -> long
    sigs = P.detect_all(up, shorts=False)
    assert any(s.name == "flag" and s.side == "long" for s in sigs)
    sigs2 = P.detect_all(mb, shorts=True)
    shorts = [s for s in sigs2 if s.side == "short" and s.name == "flag"]
    assert shorts and shorts[0].stop > shorts[0].price > shorts[0].target

def test_detect_all_safe_on_garbage():
    assert P.detect_all(flat(5)) == []
    assert isinstance(P.detect_all(flat(300)), list)

# ---- day detectors ----
def intraday_orb(breakout=True, vol=3000):
    bars = [B(50, 50.4, 49.8, 50.2, 2000), B(50.2, 50.5, 50.0, 50.3, 1500), B(50.3, 50.5, 50.1, 50.4, 1500)]
    bars += [B(50.3 + 0.02 * (i % 3), 50.45, 50.2, 50.35, 1000) for i in range(8)]
    bars += [B(50.4, 51.0, 50.4, 50.9, vol)] if breakout else [B(50.3, 50.4, 50.2, 50.3, 1000)]
    return bars

def test_orb_long():
    s = P.orb_long(intraday_orb())
    assert s and s.kind == "day" and s.stop < s.price < s.target

def test_orb_needs_volume_and_breakout():
    assert P.orb_long(intraday_orb(vol=1000)) is None
    assert P.orb_long(intraday_orb(False)) is None

def test_gap_and_go_named():
    s = P.orb_long(intraday_orb(), {"prev_close": 48.5})
    assert s and s.name == "gap_and_go"

def test_orb_short_via_mirror():
    up = intraday_orb()
    mb, k2 = P.mirror(up)
    sigs = P.detect_day(mb)
    assert any(s.name == "orb" and s.side == "short" and s.target < s.price < s.stop for s in sigs)

def test_vwap_reclaim():
    bars = [B(50, 50.3, 49.9, 50.1, 1000) for _ in range(4)]
    bars += [B(50.1 - 0.1 * i, 50.15 - 0.1 * i, 49.7 - 0.1 * i, 49.9 - 0.12 * i, 1000) for i in range(1, 9)]
    bars += [B(49.0, 50.9, 48.95, 50.8, 5000)]
    s = P.vwap_reclaim_long(bars)
    assert s and s.name == "vwap_reclaim" and s.stop < s.price < s.target
    assert P.vwap_reclaim_long(bars[:-1] + [B(49.0, 49.3, 48.9, 49.1, 5000)]) is None
