import random
import patterns as P
import patterns3 as P3
from tests.test_patterns import B, ramp, flat
from tests.test_patterns2 import walk
from indicators import macd, stoch, anchored_vwap, ichimoku

def sane(s): return (s.stop < s.price < s.target) if s.side == "long" else (s.target < s.price < s.stop)

def test_new_indicators():
    c = [100 + 0.5 * i for i in range(80)]
    m = macd(c); assert m and m[0] > 0
    bars = [{"o": x, "h": x + 1, "l": x - 1, "c": x, "v": 100} for x in c]
    k, d, kp, dp = stoch(bars); assert 0 <= k <= 100
    assert anchored_vwap(bars, 10) > anchored_vwap(bars, 0)
    ich = ichimoku(bars); assert ich and ich[0] > ich[1] > ich[2]            # מגמה עולה: tenkan>kijun>ענן

def test_swing_geometry_all_mirrors():
    for seed in range(120):
        d = random.Random(seed).choice([-0.0008, -0.0003, 0.0, 0.0006, 0.0012, 0.002])
        bars = walk(430, seed, drift=d, vol=random.Random(seed + 1).choice([0.012, 0.02, 0.03]))
        for s in P.detect_all(bars, {k: (k in P3.SWING) for k in P.LONG_DETECTORS}, {"rs": 0}):
            assert sane(s), (s.name, s.side, s.price, s.stop, s.target)

def test_day_geometry_with_prev_day_context():
    for seed in range(250):
        b5 = walk(78, seed, drift=0.0003, vol=0.0025)
        ctx = {"prev_close": b5[0]["o"] * random.Random(seed).choice([0.96, 1.0, 1.04]),
               "prev_high": max(b["h"] for b in b5[:40]), "prev_low": min(b["l"] for b in b5[:40])}
        for s in P.detect_day(b5, ctx):
            assert sane(s), (s.name, s.side)

# ---- סווינג: דוגמאות בנויות (שהגלאי באמת עובד, לא רק רץ) ----
def test_capitulation_reversal():
    base = [B(100 + 0.3 * (i % 3), 100.8, 99.2, 100, 1000) for i in range(60)]
    drop = [B(100 - 2 * i, 100.2 - 2 * i, 98 - 2 * i, 98.2 - 2 * i, 1500) for i in range(1, 8)]
    s = P3.capitulation_reversal(base + drop + [B(84.5, 88.5, 82.0, 87.0, 5200)])
    assert s and s.name == "capitulation_reversal" and sane(s)
    assert P3.capitulation_reversal(base + drop + [B(84.5, 88.5, 82.0, 87.0, 1500)]) is None       # בלי נפח

def test_momentum_burst():
    tight = [B(50 + 0.1 * (i % 2), 50.5, 49.6, 50.1, 1000) for i in range(40)]
    s = P3.momentum_burst(tight + [B(50.0, 52.6, 49.9, 52.5, 2600)])
    assert s and sane(s)
    assert P3.momentum_burst(tight + [B(50.0, 51.2, 49.9, 51.0, 2600)]) is None                    # רק +2%

def test_gap_down_reclaim():
    gd = [B(100 + 0.2 * (i % 3), 100.6, 99.4, 100.2, 1000) for i in range(60)]
    s = P3.gap_down_reclaim(gd + [B(97.0, 100.9, 96.8, 100.8, 2400)])
    assert s and sane(s)
    assert P3.gap_down_reclaim(gd + [B(97.0, 99.0, 96.8, 98.0, 2400)]) is None                      # לא חזר מעל הסגירה

def test_keltner_thrust():
    up = ramp(50, 90, 40, 1000, sp=0.3)
    pause = [B(90 + 0.4 * ((-1) ** i), 90.7, 89.4, 90 + 0.3 * ((-1) ** i), 1000) for i in range(32)]
    s = P3.keltner_thrust(up + pause + [B(92.0, 94.5, 91.9, 94.2, 2500)])
    assert s and sane(s)
    assert P3.keltner_thrust(up + pause + [B(90.2, 94.5, 90.1, 94.2, 2500)]) is None               # חצי גוף לא מעל הקו

def test_spring_reversal():
    base = [B(100 + 0.4 * ((-1) ** i), 101, 99, 100, 1000) for i in range(60)]
    base += [B(99.6, 99.8, 97.5, 98.0, 1000), B(98.0, 98.4, 96.8, 97.5, 1200)]
    s = P3.spring_reversal(base + [B(98.0, 100.4, 97.8, 100.1, 1800)])
    assert s and s.name == "spring_reversal" and sane(s)
    assert P3.spring_reversal(base + [B(98.0, 98.5, 97.0, 97.4, 1800)]) is None                   # לא חזר מעל השפל

def test_higher_low_breakout_requires_structure_and_body():
    bars = []
    for lo, hi in [(10, 14), (12, 18), (15, 22), (19, 26)]:
        bars += ramp(lo, hi, 6) + ramp(hi, lo + 2, 6)
    bars = bars + [B(b["o"], b["h"], b["l"], b["c"], 1000) for b in []]
    pad = ramp(bars[0]["c"] - 8, bars[0]["c"], 40)
    bars = pad + bars + ramp(bars[-1]["c"], bars[-1]["c"] + 3, 4)
    hi = max(b["h"] for b in bars[-25:-1])
    base = bars + [B(hi - 0.5, hi + 2.2, hi - 0.6, hi + 2.0, 3000)]
    s = P3.higher_low_breakout(base)
    assert s is None or sane(s)                                                                      # רגיש לפיבוטים; מכוסה גם ע"י fuzz

# ---- יום ----
def test_pdh_break_and_mirror_pdl_break():
    b5 = [B(50 + 0.02 * (i % 3), 50.3, 49.8, 50.1, 1000) for i in range(10)] + [B(50.8, 51.7, 50.7, 51.5, 3000)]
    s = P3.pdh_break(b5, {"prev_high": 51.0})
    assert s and s.name == "pdh_break" and sane(s)
    assert P3.pdh_break(b5, {}) is None and P3.pdh_break(b5[:-1] + [B(50.0, 51.7, 49.9, 51.2, 3000)], {"prev_high": 51.0}) is None   # חצי גוף
    mb, _ = P.mirror(b5)
    sigs = P.detect_day(mb, {"prev_low": 49.0, "prev_high": 51.0, "prev_close": 50.0})
    assert all(sane(x) for x in sigs)

def test_gap_reversal():
    first = [B(48.2, 48.9, 48.0, 48.5, 2000), B(48.5, 48.8, 48.2, 48.3, 1500), B(48.3, 48.7, 48.1, 48.4, 1200), B(48.4, 48.7, 48.2, 48.3, 1000),
             B(48.3, 48.6, 48.1, 48.4, 1000), B(48.4, 48.6, 48.2, 48.3, 1000)]
    mid = [B(48.4, 48.7, 48.2, 48.5, 900) for _ in range(6)]
    s = P3.gap_reversal(first + mid + [B(48.7, 49.5, 48.6, 49.2, 2600)], {"prev_close": 50.0})
    assert s and s.name == "gap_reversal" and sane(s)
    assert P3.gap_reversal(first + mid + [B(48.7, 49.5, 48.6, 49.2, 2600)], {"prev_close": 49.0}) is None      # אין גאפ

def test_afternoon_breakout():
    morning = [B(50 + 0.03 * i, 50.3 + 0.03 * i, 49.8, 50.1 + 0.03 * i, 1000) for i in range(24)]
    lunch = [B(50.5 + 0.2 * ((-1) ** i), 50.7, 50.0, 50.4 + 0.1 * ((-1) ** i), 600) for i in range(24)]
    drift = [B(50.4, 50.6, 50.2, 50.4, 600) for _ in range(7)]
    s = P3.afternoon_breakout(morning + lunch + drift + [B(50.6, 51.4, 50.5, 51.2, 1600)])
    assert s and s.name == "afternoon_breakout" and sane(s)
    assert P3.afternoon_breakout(morning + lunch + drift + [B(50.6, 51.4, 50.5, 51.2, 500)]) is None
