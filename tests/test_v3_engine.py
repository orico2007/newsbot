import copy
from datetime import datetime, timezone
import pytest
from helpers import *
import bot
from broker import MockBroker
from test_engine import clock, Funds
from tests.test_patterns import intraday_orb, ramp, B, make_flag
from tests.test_crypto import base_break_bars

NOW = datetime.now(timezone.utc)

@pytest.fixture
def mk3(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path); bot.STATE_FILE = tmp_path / "s.json"; bot.JOURNAL = tmp_path / "j.csv"
    def make(rules=None, mtc=240):
        b = MockBroker(); b._news = []; b._clock = clock(mtc)
        r = rules or copy.deepcopy(R); r["swing"]["watchlist"] = ["AAA"]
        return b, bot.Engine(b, FakeBrain(1, "neutral"), r, bot.roll({}), None)
    return make

# ---------- day signals ----------
def test_day_scan_enters_orb_long(mk3):
    b, e = mk3()
    b.bar_data[("AAA", "5Min")] = intraday_orb(); b.snap["AAA"] = (50.9, 50.0, 2e6)
    e.day_scan(NOW, 240, True)
    assert len(b.orders) == 1 and b.orders[0][0] == "AAA" and b.orders[0][2] == "buy"
    sym, qty, side, stop, tp, tif = b.orders[0]
    assert stop < 50.9 < tp and tif == "day" and e.state["meta"]["AAA"]["strategy"] == "day"

def test_day_scan_short_via_mirror(mk3):
    b, e = mk3()
    mb, _ = __import__("patterns").mirror(intraday_orb())
    b.bar_data[("AAA", "5Min")] = mb; last = mb[-1]["c"]; b.snap["AAA"] = (last, last * 1.01, 2e6)
    e.day_scan(NOW, 240, True)
    assert b.orders and b.orders[0][2] == "sell" and b.orders[0][3] > last > b.orders[0][4]

def test_day_scan_skips_near_close_and_only_once_per_symbol(mk3):
    b, e = mk3()
    b.bar_data[("AAA", "5Min")] = intraday_orb(); b.snap["AAA"] = (50.9, 50.0, 2e6)
    e.day_scan(NOW, 20, True); assert not b.orders                 # קרוב לסגירה
    e.day_scan(NOW, 240, True); n = len(b.orders)
    e.state["day_scan_ts"] = 0; e.state["meta"].clear(); b._pos.clear()
    e.day_scan(NOW, 240, True)
    assert len(b.orders) == n                                      # tried: לא חוזרים לאותה מניה באותו יום

# ---------- swing patterns ----------
def swing_flag_daily():
    bars = [B(40, 40.2, 39.8, 40, 2_000_000) for _ in range(90)] + [dict(b, v=b["v"] * 2000) for b in make_flag()]
    return bars

def test_swing_pattern_scan_enters_with_structure_levels(mk3):
    b, e = mk3()
    d = swing_flag_daily(); last = d[-1]["c"]
    b.bar_data[("AAA", "1Day")] = d; b.snap["AAA"] = (last, d[-2]["c"], 2e8)
    e.swing_pass(NOW, 10)
    assert b.orders, "flag should produce a swing entry"
    sym, qty, side, stop, tp, tif = b.orders[0]
    assert side == "buy" and tif == "gtc" and stop < last < tp

def test_swing_scan_blocked_by_weak_sector(mk3):
    b, e = mk3()
    r = copy.deepcopy(R); r["swing"]["watchlist"] = ["NEE"]; b2, e2 = mk3(r)
    d = swing_flag_daily(); last = d[-1]["c"]
    b2.bar_data[("NEE", "1Day")] = d; b2.snap["NEE"] = (last, d[-2]["c"], 2e8)
    b2.bar_data[("SPY", "1Day")] = ramp(100, 120, 220)
    for etf in ["XLK", "SMH", "XLF", "XLE", "XLV", "XBI", "XLY", "XLP", "XLI", "XLB", "XLRE", "XLC", "ITA"]:
        b2.bar_data[(etf, "1Day")] = ramp(100, 135, 220)
    b2.bar_data[("XLU", "1Day")] = ramp(100, 90, 220)
    e2.mkt.refresh(NOW, force=True)
    e2.swing_pass(NOW, 10)
    assert not b2.orders                                           # NEE (XLU) חלש = וטו ללונג

# ---------- trailing ----------
def test_breakeven_then_trail_moves_stop_up_only(mk3):
    b, e = mk3()
    e.state["meta"]["AAA"] = {"strategy": "swing", "side": "long", "entry": 100, "stop": 96, "ext": 100, "atr": 2, "ts": 0, "entry_date": "2026-10-20"}
    pos = lambda px: [{"symbol": "AAA", "current_price": str(px), "avg_entry_price": "100", "qty": "10", "side": "long"}]
    e.manage_positions(NOW, pos(102.5))                            # +1.25 ATR -> ברייק-אבן
    assert b.raised[-1] == ("AAA", 100) and e.state["meta"]["AAA"]["stop"] == 100
    e.manage_positions(NOW, pos(108))                              # +4 ATR -> טריילינג 108-5=103
    assert b.raised[-1][1] == 103
    n = len(b.raised); e.manage_positions(NOW, pos(105))           # נסיגה: לא מורידים
    assert len(b.raised) == n and e.state["meta"]["AAA"]["stop"] == 103

def test_trailing_short_moves_down(mk3):
    b, e = mk3()
    e.state["meta"]["AAA"] = {"strategy": "swing", "side": "short", "entry": 100, "stop": 104, "ext": 100, "atr": 2, "ts": 0, "entry_date": "2026-10-20"}
    e.manage_positions(NOW, [{"symbol": "AAA", "current_price": "92", "avg_entry_price": "100", "qty": "-10", "side": "short"}])
    assert b.raised and b.raised[-1][1] == 97          # 92 + 2.5*2

# ---------- cooldown / crypto isolation / sector cap ----------
def test_cooldown_after_position_disappears(mk3):
    b, e = mk3()
    e.state["meta"]["AAA"] = {"strategy": "day", "side": "long", "ts": 0}
    e.reconcile([])
    assert "AAA" in e.state["cool"]
    ok, why, _ = e._gate("AAA", "long")
    assert not ok and "cooldown" in why

def test_crypto_positions_ignored_by_stock_engine(mk3):
    b, e = mk3()
    b._pos.append({"symbol": "BTCUSD", "asset_class": "crypto", "market_value": "5000", "qty": "0.1"})
    assert e._pos() == []

def test_sector_cap(mk3):
    b, e = mk3()
    b._pos += [{"symbol": "NVDA", "market_value": "1000"}, {"symbol": "AMD", "market_value": "1000"}]
    ok, why, _ = e._gate("MU", "long")                              # כולם SMH
    assert not ok and "sector cap" in why
    assert e._gate("JPM", "long")[0]
