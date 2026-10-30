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

# ---------- scale-out: מימוש חלקי + סטופ לנמוך הבא ----------
def _pos(px, qty, side="long", entry=100):
    return [{"symbol": "AAA", "current_price": str(px), "avg_entry_price": str(entry), "qty": str(qty), "side": side}]

def _meta(side="long"):
    return {"strategy": "swing", "side": side, "entry": 100, "qty": 90, "qty0": 90, "take": 115 if side == "long" else 85,
            "stop": 95 if side == "long" else 105, "stop0": 95 if side == "long" else 105, "ext": 100, "atr": 2, "ts": 0, "entry_date": "2026-10-20"}

def _bars_with_low(low_px):
    out = []
    for i in range(40):
        px = 98 + i * 0.2 if i != 30 else low_px
        out.append({"o": px, "h": px + 1, "l": px - (0.3 if i != 30 else 0), "c": px + 0.3, "v": 1e6})
    out[30]["l"] = low_px
    return out

def test_scale_out_long_takes_partial_and_squeezes_stop_to_swing_low(mk3):
    b, e = mk3()
    e.state["meta"]["AAA"] = _meta(); b._pos = _pos(105.5, 90)
    b.bar_data[("AAA", "1Day")] = _bars_with_low(102.0)
    e.scale_out(NOW, b._pos)                                          # 1R = +5 -> מוכרים 33%
    assert b.partials == [("AAA", 29)]
    sym, qty, side, stop, take = b.protected[-1]
    assert qty == 61 and side == "sell" and take == 115 and 100 <= stop < 105.5      # לפחות ברייק-אבן, לא מעל המחיר
    e.scale_out(NOW, _pos(105.9, 61))                                 # אותו יעד לא נמכר פעמיים
    assert len(b.partials) == 1

def test_scale_out_second_level_and_final_blended_record(mk3):
    b, e = mk3()
    e.state["meta"]["AAA"] = _meta(); b._pos = _pos(105.5, 90)
    e.scale_out(NOW, b._pos)
    e.scale_out(NOW, _pos(110.5, 61))                                 # 2R = +10
    assert len(b.partials) == 2 and b.protected[-1][1] == 32
    m = e.state["meta"]["AAA"]
    assert m["qty"] == 32 and m["tp_done"] == [0, 1] and m["stop"] >= 105              # הסטופ הוצמד מעל מחיר הכניסה

def test_scale_out_short_mirrors(mk3):
    b, e = mk3()
    e.state["meta"]["AAA"] = _meta("short"); b._pos = _pos(94.5, -90, "short")
    e.scale_out(NOW, b._pos)
    assert b.partials == [("AAA", 29)] and b.protected[-1][2] == "buy" and b.protected[-1][3] <= 100

def test_scale_out_skipped_when_target_too_close(mk3):
    b, e = mk3()
    m = _meta(); m["take"] = 104; e.state["meta"]["AAA"] = m; b._pos = _pos(106, 90)
    e.scale_out(NOW, b._pos)
    assert not getattr(b, "partials", [])

# ---------- research: whitelist / מסננים / יציאות ----------
def _write_research(validated=None, filters=None, exits=None):
    import json, bot
    if validated is not None: (bot.DATA / "validated.json").write_text(json.dumps({"patterns": validated}), encoding="utf-8")
    if filters is not None: (bot.DATA / "filters.json").write_text(json.dumps(filters), encoding="utf-8")
    if exits is not None: (bot.DATA / "exits.json").write_text(json.dumps(exits), encoding="utf-8")

def _enf():
    r = copy.deepcopy(R); r["research"] = {"enforce": True, "min_validated": 5}; return r

def _flag_setup(b):
    d = swing_flag_daily(); last = d[-1]["c"]
    b.bar_data[("AAA", "1Day")] = d; b.snap["AAA"] = (last, d[-2]["c"], 2e8)

OTHER5 = {f"p{i}:long": {"regimes": ["bull", "bear", "neutral"], "mult": 1.0} for i in range(5)}

def test_whitelist_blocks_unvalidated_pattern(mk3):
    b, e = mk3(_enf()); _flag_setup(b); _write_research(validated=OTHER5, filters={"long": [], "short": []})
    e.swing_pass(NOW, 10)
    assert not b.orders                                            # flag לא ברשימה המאומתת

def test_whitelist_allows_validated_and_scales_size(mk3):
    b, e = mk3(); _flag_setup(b)
    e.swing_pass(NOW, 10); base_qty = b.orders[0][1]               # בלי research: נכנס
    b2, e2 = mk3(_enf()); _flag_setup(b2)
    _write_research(validated=dict(OTHER5, **{"flag:long": {"regimes": ["bull", "bear", "neutral"], "mult": 0.75}}), filters={"long": [], "short": []})
    e2.swing_pass(NOW, 10)
    assert b2.orders and b2.orders[0][1] < base_qty                # מכפיל 0.75 מקטין את הפוזיציה

def test_whitelist_inactive_with_few_validated_patterns(mk3):
    b, e = mk3(_enf()); _flag_setup(b); _write_research(validated={"p0:long": {"regimes": ["bull"], "mult": 1.0}})
    e.swing_pass(NOW, 10)
    assert b.orders                                                # פחות מ-5 מאומתות: לא מחילים whitelist

def test_feature_filter_blocks_entry(mk3):
    b, e = mk3(_enf()); _flag_setup(b); _write_research(validated={}, filters={"long": [{"f": "rvol", "op": "<=", "v": 0.0001}], "short": []})
    e.swing_pass(NOW, 10)
    assert not b.orders

def test_research_exits_override_target_and_hold(mk3):
    b, e = mk3(_enf()); _flag_setup(b); _write_research(validated={}, filters={"long": [], "short": []}, exits={"stop_atr": None, "target_r": 2.0, "no_target": False, "hold": 7, "scale": []})
    e.swing_pass(NOW, 10)
    sym, qty, side, stop, tp, tif = b.orders[0]
    price = b.snap["AAA"][0]
    assert abs((tp - price) - 2.0 * (price - stop)) < 0.6 and e._hold_days() == 7

def test_research_not_enforced_by_default(mk3):
    b, e = mk3(); _flag_setup(b); _write_research(validated=OTHER5, filters={"long": [{"f": "rvol", "op": "<=", "v": 0.0001}], "short": []})
    e.swing_pass(NOW, 10)
    assert b.orders                                                # enforce=false: ה-research לא חוסם
