from datetime import date, timedelta
import copy, pytest, bot
from earnings import Earnings, parse
from helpers import *
from broker import MockBroker
from test_engine import clock
from test_v3_engine import swing_flag_daily, NOW

def cal(mapping):
    return lambda d: {"data": {"rows": [{"symbol": s} for s in mapping.get(d, [])]}}

def test_parse_and_days_until():
    t = date(2026, 10, 28)   # Wednesday
    e = Earnings(4, cal({t + timedelta(days=1): ["aaa"], t + timedelta(days=2): ["BBB"]}))
    assert e.days_until("AAA", t) == 1 and e.days_until("BBB", t) == 2 and e.days_until("CCC", t) is None
    assert parse({"data": None}) == set()

def test_unknown_calendar_fails_open():
    def boom(d): raise RuntimeError("blocked")
    e = Earnings(4, boom)
    assert e.days_until("AAA", date(2026, 10, 28)) is None

@pytest.fixture
def eng(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path); bot.STATE_FILE = tmp_path / "s.json"; bot.JOURNAL = tmp_path / "j.csv"
    def make(report_day_offset):
        b = MockBroker(); b._news = []; b._clock = clock(10)
        r = copy.deepcopy(R); r["swing"]["watchlist"] = ["AAA"]
        today = date.today()
        e = Earnings(4, cal({today + timedelta(days=report_day_offset): ["AAA"]}))
        return b, bot.Engine(b, FakeBrain(1, "neutral"), r, bot.roll({}), None, e)
    return make

def test_swing_entry_blocked_before_earnings(eng):
    b, e = eng(1)
    d = swing_flag_daily(); last = d[-1]["c"]
    b.bar_data[("AAA", "1Day")] = d; b.snap["AAA"] = (last, d[-2]["c"], 2e8)
    e.swing_pass(NOW, 10)
    assert not b.orders and (bot.JOURNAL).read_text(encoding="utf-8-sig").count("earnings in") >= 1

def test_swing_entry_allowed_when_no_report_soon(eng):
    b, e = eng(30)      # מחוץ לטווח הבדיקה
    d = swing_flag_daily(); last = d[-1]["c"]
    b.bar_data[("AAA", "1Day")] = d; b.snap["AAA"] = (last, d[-2]["c"], 2e8)
    e.swing_pass(NOW, 10)
    assert b.orders

def test_open_swing_flattened_day_before_report(eng):
    b, e = eng(1)
    b._pos.append({"symbol": "AAA", "market_value": "1000", "qty": "10"})
    e.state["meta"]["AAA"] = {"strategy": "swing", "side": "long", "entry_date": str(date.today()), "ts": 0}
    e.swing_pass(NOW, 10)
    assert "AAA" in b.closed
