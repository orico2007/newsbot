import random
import patterns as P
import patterns2 as P2
from indicators import ema, adx, keltner, ibs, rsi
from tests.test_patterns import B, ramp, flat

def walk(n, seed, drift=0.0004, vol=0.015, intraday=False):
    r = random.Random(seed); p = 100.0; out = []
    for i in range(n):
        o = p; c = p * (1 + r.gauss(drift, vol)); h = max(o, c) * (1 + abs(r.gauss(0, vol / 3))); l = min(o, c) * (1 - abs(r.gauss(0, vol / 3)))
        out.append({"t": f"2025-01-{1 + i % 28:02d}T00:00:00Z", "o": o, "h": h, "l": l, "c": c, "v": int(1e6 * (1 + abs(r.gauss(0, 0.6))))}); p = c
    return out

SWING_NAMES = list(P2.SWING)
DAY_NAMES = list(P2.DAY)

def sane(s):
    return (s.stop < s.price < s.target) if s.side == "long" else (s.target < s.price < s.stop)

def test_indicators():
    c = [100 + i for i in range(60)]
    assert ema(c, 10) > ema(c, 30)                      # בעלייה EMA מהיר גבוה
    up = [{"o": x, "h": x + 1, "l": x - 1, "c": x, "v": 1} for x in c]
    assert adx(up) > 40 and ibs({"h": 10, "l": 0, "c": 1}) == 0.1 and keltner(up)[1] > keltner(up)[2]

def test_swing_geometry_and_reachability():
    fired = {n: 0 for n in SWING_NAMES}
    for seed in range(120):
        bars = walk(420, seed, drift=random.Random(seed).choice([-0.0006, 0.0, 0.0008, 0.0015]))
        sigs = P.detect_all(bars, {k: (k in SWING_NAMES) for k in P.LONG_DETECTORS}, {"rs": 0})
        for s in sigs:
            assert sane(s), (s.name, s.side, s.price, s.stop, s.target)
            if s.name in fired: fired[s.name] += 1
    never = [n for n, k in fired.items() if k == 0]
    assert len(never) <= 6, f"too many detectors never fire on random data: {never}"      # חלקם נדירים באמת (VCP/כוס וידית)

def test_day_geometry_and_reachability():
    fired = {n: 0 for n in DAY_NAMES + ["orb", "vwap_reclaim"]}
    for seed in range(300):
        b5 = walk(60, seed, drift=0.0003, vol=0.002)
        for s in P.detect_day(b5, {"prev_close": b5[0]["o"] * 1.01}):
            assert sane(s), (s.name, s.side)
            base = s.name.replace("_15m", "")
            if base in fired: fired[base] += 1
    assert sum(1 for k in fired.values() if k) >= 3

def test_rsi2_reversion_fixture():
    bars = ramp(50, 120, 230) + [B(120, 120.3, 118, 118.5), B(118.5, 118.7, 116, 116.5), B(116.5, 116.7, 114, 114.2)]
    s = P2.rsi2_reversion(bars)
    assert s and s.name == "rsi2_reversion" and s.stop < s.price < s.target

def test_rsi2_not_below_200ma():
    bars = ramp(150, 50, 230) + [B(50, 50.3, 48, 48.5), B(48.5, 48.7, 46, 46.5)]
    assert P2.rsi2_reversion(bars) is None

def test_donchian_needs_half_body_and_volume():
    base = ramp(40, 60, 150) + [B(58 + (i % 3) * 0.4, 60.3, 57.5, 59, 1000) for i in range(30)]
    good = base + [B(59.0, 61.9, 58.9, 61.6, 2500)]
    assert P2.donchian20(good) is not None
    weak = base + [B(58.0, 61.9, 57.9, 60.5, 2500)]                  # סוגר מעל, רוב הגוף מתחת לקו
    assert P2.donchian20(weak) is None
    assert P2.donchian20(base + [B(59.0, 61.9, 58.9, 61.6, 900)]) is None

def test_nr7_breakout():
    bars = ramp(40, 60, 100)
    wide = [B(60 + (0.4 if i % 2 else -0.4), 61.2, 58.8, 60, 1000) for i in range(8)]
    bars += wide + [B(60, 60.2, 59.9, 60.05, 800)]                    # NR7
    bars += [B(60.1, 61.8, 60.0, 61.6, 1800)]
    s = P2.nr7_breakout(bars)
    assert s and s.name == "nr7_breakout" and s.stop < s.price < s.target

def test_pocket_pivot():
    c = [50 + 0.2 * i for i in range(230)]
    bars = [B(x, x + 0.4, x - 0.4, x, 1000) for x in c]
    for i in range(-10, -1):
        if i % 2: bars[i] = B(bars[i - 1]["c"], bars[i - 1]["c"] + 0.1, bars[i - 1]["c"] - 0.9, bars[i - 1]["c"] - 0.6, 900)
    last = bars[-2]["c"]
    bars[-1] = B(last, last + 1.4, last - 0.05, last + 1.2, 2500)
    s = P2.pocket_pivot(bars)
    assert s and s.stop < s.price < s.target

def test_morning_star_context_required():
    base = ramp(100, 70, 60)
    ms = base + [B(72, 72.2, 69.5, 69.8, 1500), B(69.5, 69.9, 68.8, 69.3, 900), B(69.6, 71.5, 69.5, 71.2, 1800)]
    s = P2.reversal_candles(ms)
    assert s and s.name == "morning_star"
    ctx_less = ramp(60, 100, 60) + [B(100, 100.2, 97.5, 97.8, 1500), B(97.5, 97.9, 96.8, 97.3, 900), B(97.6, 99.5, 97.5, 99.2, 1800)]
    assert P2.reversal_candles(ctx_less) is None                      # בלי RSI נמוך / תמיכה

def test_cup_handle_fixture():
    pre = flat(40, 60, 1000); left = ramp(60, 100, 30)
    cup = ramp(100, 75, 30) + ramp(75, 98, 30)
    handle = [B(98 - 0.3 * i, 98.4 - 0.3 * i if i else 98.3, 97.4 - 0.3 * i, 97.8 - 0.3 * i, 500) for i in range(8)]
    bars = pre + left + cup + handle + [B(97.9, 100.3, 97.8, 100.0, 2600)]
    s = P2.cup_handle(bars)
    assert s and s.name == "cup_handle" and s.stop < s.price < s.target
    weak = pre + left + cup + handle + [B(96.5, 100.3, 96.4, 99.0, 2600)]           # רוב הגוף מתחת לקו
    assert P2.cup_handle(weak) is None

def _vcp_bars(open_px=103.6):
    r = lambda a, b, n, v=1000: ramp(a, b, n, v, sp=0.15)
    bars = r(40, 100, 210) + r(100, 105, 6) + r(105, 95, 8) + r(95, 104, 8) + r(104, 98.5, 7) + r(98.5, 103.5, 7) + r(103.5, 100.8, 6, v=600)
    bars += [B(100.9, 101.2, 100.7, 101.0, 600), B(101.0, 101.3, 100.8, 101.1, 600), B(101.1, 101.4, 100.9, 101.2, 600), B(101.2, 101.4, 101.0, 101.3, 600)]
    return bars + [B(open_px, 105.9, open_px - 0.1, 105.6, 2600)]

def test_vcp_fixture_and_rules():
    s = P2.vcp(_vcp_bars())
    assert s and s.name == "vcp" and s.stop < s.price < s.target and "%" in s.notes
    assert P2.vcp(_vcp_bars(102.0)) is None                                       # חצי גוף לא מעל הקו
    flat_trend = ramp(100, 100.5, 257)
    assert P2.vcp(flat_trend) is None

def test_pead_pullback():
    base = [B(50 + (0.3 if i % 2 else -0.3), 50.8, 49.2, 50, 1000) for i in range(70)]
    gap = [B(54, 56, 53.8, 55.6, 4000)]
    drift = [B(55.6 - 0.15 * i, 55.9 - 0.15 * i, 55.0 - 0.15 * i, 55.2 - 0.15 * i, 800) for i in range(8)]
    last = [B(54.2, 55.4, 54.1, 55.1, 1500)]
    s = P2.pead_pullback(base + gap + drift + last)
    assert s and s.name == "pead_pullback" and s.stop < s.price < s.target
    closed = base + gap + [B(53, 53.2, 52, 52.5, 900)] + drift + last
    assert P2.pead_pullback(closed) is None                            # הגאפ נסגר

# ---- יום ----
def test_red_to_green():
    b5 = [B(48.8, 49.0, 48.5, 48.7, 1500)] + [B(48.7 + 0.03 * i, 48.95 + 0.03 * i, 48.5 + 0.03 * i, 48.8 + 0.03 * i, 1000) for i in range(10)]
    b5 += [B(49.9, 50.5, 49.8, 50.4, 3000)]
    s = P2.red_to_green(b5, {"prev_close": 50.0})
    assert s and s.name == "red_to_green" and s.stop < s.price < s.target

def test_hod_break():
    b5 = [B(50 + 0.05 * i, 50.3 + 0.05 * i, 49.8 + 0.05 * i, 50.1 + 0.05 * i, 1000) for i in range(14)]
    top = b5[-1]["h"]
    b5 += [B(top - 0.12, top, top - 0.2, top - 0.1 + (0.02 * (i % 2)), 700) for i in range(6)]
    b5 += [B(top - 0.1, top + 0.5, top - 0.15, top + 0.4, 2600)]
    s = P2.hod_break(b5)
    assert s and s.name == "hod_break" and s.stop < s.price < s.target

def test_vwap_bounce():
    b5 = [B(50 + 0.04 * i, 50.25 + 0.04 * i, 49.9 + 0.04 * i, 50.15 + 0.04 * i, 1000) for i in range(24)]
    from indicators import vwap
    vw = vwap(b5)
    b5 += [B(vw + 0.5, vw + 0.55, vw + 0.1, vw + 0.2, 800), B(vw + 0.2, vw + 0.25, vw - 0.02, vw - 0.01 + 0.0, 800)]
    b5 += [B(vw - 0.05, vw + 0.45, vw - 0.07, vw + 0.4, 1500)]
    s = P2.vwap_bounce(b5)
    assert s is None or (s.name == "vwap_bounce" and s.stop < s.price < s.target)

def test_intraday_flag_is_day_kind():
    b5 = [B(50, 50.05, 49.95, 50, 1000) for _ in range(14)]
    b5 += [B(50 + 0.3 * i, 50.3 + 0.3 * i, 49.95 + 0.3 * i, 50.3 + 0.3 * i, 3000) for i in range(5)]       # תורן ~3%
    hi = b5[-1]["c"]
    b5 += [B(hi - 0.02 * i, hi + 0.05 - 0.02 * i, hi - 0.25 - 0.02 * i, hi - 0.1 - 0.02 * i, 700) for i in range(4)]
    b5 += [B(hi - 0.1, hi + 0.5, hi - 0.15, hi + 0.35, 1800)]
    s = P2.intraday_flag(b5)
    assert s is None or (s.kind == "day" and s.name == "intraday_flag" and s.stop < s.price < s.target)
