from datetime import date, timedelta
import timeframes as T
from helpers import *
import bot, copy
from broker import MockBroker
from test_engine import clock
from test_v3_engine import swing_flag_daily, NOW

def dated(closes, start=date(2025, 1, 6), step_days=1):
    out, d = [], start
    for c in closes:
        while d.weekday() >= 5: d += timedelta(days=1)
        out.append({"t": d.isoformat() + "T00:00:00Z", "o": c, "h": c + 0.2, "l": c - 0.2, "c": c, "v": 1000}); d += timedelta(days=1)
    return out

def test_resample_weekly_ohlcv():
    d = dated([10, 11, 12, 13, 14, 15, 16])          # 5 ימים בשבוע הראשון + 2 בשני
    w = T.resample_weekly(d)
    assert len(w) == 2 and w[0]["o"] == 10 and w[0]["c"] == 14 and w[0]["h"] == 14.2 and w[0]["l"] == 9.8 and w[0]["v"] == 5000 and w[1]["c"] == 16

def test_resample_n_drops_partial_group():
    bars = [{"t": i, "o": i, "h": i + 1, "l": i - 1, "c": i, "v": 10} for i in range(7)]
    r = T.resample_n(bars, 3)
    assert len(r) == 2 and r[0]["o"] == 0 and r[0]["c"] == 2 and r[0]["h"] == 3 and r[0]["v"] == 30

def test_weekly_trend_and_points():
    up = dated([50 + 0.25 * i for i in range(300)])
    down = dated([120 - 0.25 * i for i in range(300)])
    assert T.weekly_trend(up) == "up" and T.weekly_trend(down) == "down" and T.weekly_trend(up[:20]) is None
    assert T.htf_points(up, "long") == 1.0 and T.htf_points(up, "short") == -1.0 and T.htf_points(down, "short") == 1.0

def test_near_level_blocks_day_long_under_resistance():
    bars = []
    for _ in range(4):
        bars += dated([50, 52, 55, 58, 60, 58, 55, 52])  # פיבוט שיא סביב 60.2 שוב ושוב
    lv = T.near_level(bars, 59.8, "long")
    assert lv and abs(lv - 60.2) < 0.6
    assert T.near_level(bars, 55, "long") is None

def test_swing_scan_only_in_last_15_minutes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path); bot.STATE_FILE = tmp_path / "s.json"; bot.JOURNAL = tmp_path / "j.csv"; monkeypatch.setattr(bot, "DATA", tmp_path)
    b = MockBroker(); b._news = []; b._clock = clock(240)
    r = copy.deepcopy(R); r["swing"]["watchlist"] = ["AAA"]
    e = bot.Engine(b, FakeBrain(1, "neutral"), r, bot.roll({}), None)
    d = swing_flag_daily(); last = d[-1]["c"]
    b.bar_data[("AAA", "1Day")] = d; b.snap["AAA"] = (last, d[-2]["c"], 2e8)
    e.swing_pass(NOW, 16); assert not b.orders and not e.state.get("swing_done")     # עדיין מוקדם
    e.swing_pass(NOW, 14); assert b.orders                                            # 15 דקות לפני הסגירה: פועל
