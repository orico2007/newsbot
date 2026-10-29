import copy, time
from datetime import datetime, timedelta
import pytest, bot, alerts
from helpers import *
from broker import MockBroker
from test_engine import clock
from test_v3_engine import NOW
from tests.test_patterns import intraday_orb
import market as M

@pytest.fixture
def mk(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path); bot.STATE_FILE = tmp_path / "s.json"; bot.JOURNAL = tmp_path / "j.csv"; monkeypatch.setattr(bot, "DATA", tmp_path)
    monkeypatch.setattr(alerts, "send", lambda *a, **k: None)
    def make(brain=None, closed_in=None):
        b = MockBroker(); b._news = []; b._clock = clock(240)
        r = copy.deepcopy(R); r["swing"]["watchlist"] = ["AAA"]
        return b, bot.Engine(b, brain or FakeBrain(10), r, bot.roll({}), None)
    return make

# ---------- premarket ----------
def pre_clock(open_in):
    ts = datetime.fromisoformat("2026-10-29T08:30:00-04:00")
    return {"is_open": False, "timestamp": ts.isoformat(), "next_open": (ts + timedelta(minutes=open_in)).isoformat(),
            "next_close": (ts + timedelta(minutes=open_in + 390)).isoformat()}

def test_premarket_scores_and_queues_then_acts_at_open(mk):
    b, e = mk()
    b._news = [news("p1", age_min=300, headline="Beats earnings, raises guidance")]
    b._clock = pre_clock(60)
    e.step()
    assert len(e.state["queue"]) == 1 and not b.orders and e.brain.calls
    # פתיחה: יש נרות 5 דקות ומחיר
    b._clock = clock(240); b._news = []
    b.snap["AAA"] = (50, 49, 2e6); b.bar_data[("AAA", "5Min")] = intraday_up(); b.bar_data[("AAA", "1Day")] = daily_pullback()
    e.step()
    assert len(b.orders) == 1 and not e.state["queue"]

def test_premarket_ignored_when_far_from_open(mk):
    b, e = mk(); b._news = [news("p2", age_min=300)]; b._clock = pre_clock(400)
    e.step()
    assert not e.state["queue"] and not e.brain.calls

def test_queue_retries_until_enough_bars_then_expires(mk):
    b, e = mk()
    b.snap["AAA"] = (50, 49, 2e6); b.bar_data[("AAA", "5Min")] = intraday_up()[:2]; b.bar_data[("AAA", "1Day")] = daily_pullback()
    e.state["queue"] = [{"sym": "AAA", "headline": "h", "v": {"score": 10, "direction": "bullish", "reason": "r", "event": "other", "horizon": "intraday"},
                         "route": ["day", "long"], "expire": time.time() + 600}]
    e.process_queue(NOW, 240, True)
    assert len(e.state["queue"]) == 1 and not b.orders                 # עדיין אין נרות: נשאר בתור
    e.state["queue"][0]["expire"] = time.time() - 1
    e.process_queue(NOW, 240, True)
    assert e.state["queue"] == []

# ---------- kill switch ----------
def test_kill_switch_rules():
    m = M.Market(None, {"kill_switch": {"enabled": True, "spy_drop_pct": 2, "spy_rally_pct": 3, "vixy_spike_pct": 10, "extreme_move_pct": 5}}, None)
    assert m.kill("long") is None
    m.risk = {"spy": -2.5, "vix": 0}; assert "no new longs" in m.kill("long") and m.kill("short") is None
    m.risk = {"spy": 0.5, "vix": 12}; assert "volatility" in m.kill("long") and m.kill("short") is None
    m.risk = {"spy": 3.5, "vix": 0}; assert m.kill("long") is None and "no new shorts" in m.kill("short")
    m.risk = {"spy": -5.5, "vix": 0}; assert m.kill("long") and m.kill("short")

def test_kill_switch_blocks_news_entry(mk):
    b, e = mk()
    b.snap["AAA"] = (50, 49, 2e6); b.bar_data[("AAA", "5Min")] = intraday_up(); b.bar_data[("AAA", "1Day")] = daily_pullback()
    b.snap["SPY"] = (95, 100, 1e9); b.snap["VIXY"] = (10, 10, 1e7)
    b._news = [news()]
    e.step()
    assert not b.orders and "kill switch" in (bot.JOURNAL).read_text(encoding="utf-8-sig")

# ---------- actives / disabled patterns in day scan ----------
def test_day_scan_uses_actives_and_respects_disabled(mk, tmp_path):
    import json
    b, e = mk()
    b.act = ["ZZZ"]
    b.bar_data[("ZZZ", "5Min")] = intraday_orb(); b.snap["ZZZ"] = (50.9, 50.0, 2e6)
    (tmp_path / "scorecard.json").write_text(json.dumps({"disabled": ["orb"]}), encoding="utf-8")
    e.day_scan(NOW, 240, True)
    assert not b.orders
    (tmp_path / "scorecard.json").write_text(json.dumps({"disabled": []}), encoding="utf-8")
    e.state["day_scan_ts"] = 0
    e.day_scan(NOW, 240, True)
    assert b.orders and b.orders[0][0] == "ZZZ"
