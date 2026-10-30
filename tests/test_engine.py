import copy
from datetime import datetime, timedelta, date
import pytest
from helpers import *
import bot
from broker import MockBroker

def clock(mtc=240, is_open=True):
    ts = datetime.fromisoformat("2026-10-29T12:00:00-04:00")
    return {"is_open": is_open, "timestamp": ts.isoformat(), "next_close": (ts + timedelta(minutes=mtc)).isoformat(),
            "next_open": (ts + timedelta(minutes=600)).isoformat()}

class Funds:
    def __init__(self, f): self.f = f
    def get(self, sym): return self.f

@pytest.fixture
def mk(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path); bot.STATE_FILE = tmp_path / "s.json"; bot.JOURNAL = tmp_path / "j.csv"
    def make(brain=None, rules=None, funds=None, up=True, daily=None, prev=49, mtc=240, news_items=None):
        b = MockBroker(); b.snap["AAA"] = (50, prev, 2e6)
        b.bar_data[("AAA", "5Min")] = intraday_up() if up else intraday_down()
        b.bar_data[("AAA", "1Day")] = daily if daily is not None else daily_pullback()
        b._news = news_items if news_items is not None else [news()]
        b._clock = clock(mtc)
        eng = bot.Engine(b, brain or FakeBrain(10), rules or R, bot.roll({}), funds)
        return b, eng
    return make

def journal_text(tmp_path): return (tmp_path / "j.csv").read_text(encoding="utf-8-sig")

# ---------- day ----------
def test_day_long_buy(mk):
    b, e = mk(); e.step()
    assert b.orders == [("AAA", 100, "buy", 48.5, 53.0, "day")] and e.state["meta"]["AAA"]["strategy"] == "day"
def test_day_blocked_by_chart(mk, tmp_path):
    b, e = mk(up=False); e.step()
    assert not b.orders and "VWAP" in journal_text(tmp_path)
def test_day_short_sell(mk):
    b, e = mk(brain=FakeBrain(9, "bearish"), up=False, prev=51); e.step()
    assert b.orders == [("AAA", 60, "sell", 51.5, 47.0, "day")]
def test_short_blocked_when_not_shortable(mk):
    b, e = mk(brain=FakeBrain(9, "bearish"), up=False, prev=51); b.assets["AAA"] = {"shortable": True, "easy_to_borrow": False, "tradable": True}
    e.step(); assert not b.orders
def test_shorts_can_be_disabled(mk):
    r = copy.deepcopy(R); r["day"]["allow_short"] = False
    b, e = mk(brain=FakeBrain(10, "bearish"), up=False, prev=51, rules=r); e.step(); assert not b.orders
def test_low_score_stale_multi_symbol_and_dedupe(mk):
    b, e = mk(brain=FakeBrain(8)); e.step(); assert not b.orders
    b, e = mk(news_items=[news(age_min=40)]); e.step(); assert not b.orders
    b, e = mk(news_items=[news(symbols=("AAA", "BBB"))]); e.step(); assert not b.orders
    b, e = mk(); e.step(); b._pos.clear(); e.step(); assert len(b.orders) == 1
def test_no_new_day_entries_near_close(mk):
    b, e = mk(mtc=12); e.step(); assert not b.orders
def test_market_closed_does_not_call_claude(mk):
    brain = FakeBrain(10); b, e = mk(brain=brain); b._clock = clock(240, is_open=False); e.step()
    assert not b.orders and not brain.calls
def test_body_and_fundamentals_reach_claude(mk):
    brain = FakeBrain(5); f = {"rev_yoy": 30}
    b, e = mk(brain=brain, funds=Funds(f), news_items=[news(content="<p>Revenue up 30%</p>")]); e.step()
    sym, head, summ, content, fund = brain.calls[0]; assert "Revenue up 30%" in content and fund == f

def test_day_flatten_before_close(mk):
    b, e = mk(mtc=8, news_items=[]); b._pos = [{"symbol": "AAA", "market_value": "5000"}, {"symbol": "SW", "market_value": "4000"}]
    e.state["meta"] = {"AAA": {"strategy": "day", "side": "long", "entry_date": str(date.today()), "ts": 1e12},
                       "SW": {"strategy": "swing", "side": "long", "entry_date": str(date.today()), "ts": 1e12}}
    e.step(); assert b.closed == ["AAA"]          # רק Day נסגר, הסווינג נשאר

# ---------- swing ----------
def test_swing_news_catalyst_entry(mk):
    b, e = mk(brain=FakeBrain(8, "bullish", "swing", "earnings")); e.step()
    assert len(b.orders) == 1 and b.orders[0][2] == "buy" and b.orders[0][5] == "gtc" and e.state["meta"]["AAA"]["strategy"] == "swing"
def test_swing_news_needs_uptrend(mk):
    b, e = mk(brain=FakeBrain(8, "bullish", "swing"), daily=daily_downtrend()); e.step(); assert not b.orders
def test_swing_news_blocked_by_bad_fundamentals(mk, tmp_path):
    b, e = mk(brain=FakeBrain(8, "bullish", "swing"), funds=Funds({"rev_yoy": -5})); e.step()
    assert not b.orders and "fundamentals disagree" in journal_text(tmp_path)
def test_swing_short_in_downtrend(mk):
    r = copy.deepcopy(R); r["swing"]["allow_short"] = True
    b, e = mk(brain=FakeBrain(8, "bearish", "swing"), daily=daily_downtrend(), prev=51, rules=r); e.step()
    assert len(b.orders) == 1 and b.orders[0][2] == "sell"
def test_swing_horizon_but_score_9_goes_day_if_swing_disabled(mk):
    r = copy.deepcopy(R); r["swing"]["enabled"] = False
    b, e = mk(brain=FakeBrain(9, "bullish", "swing"), rules=r); e.step()
    assert b.orders and b.orders[0][5] == "day"

def scan_rules():
    r = copy.deepcopy(R); r["swing"]["watchlist"] = ["AAA"]; return r
def test_daily_scan_buys_once_per_day(mk, tmp_path):
    b, e = mk(rules=scan_rules(), funds=Funds({"rev_yoy": 25, "eps_positive": True}), mtc=15, news_items=[]); e.step()
    assert len(b.orders) == 1 and b.orders[0][5] == "gtc" and e.state["swing_done"] == str(date.today())
    b._pos.clear(); e.step(); assert len(b.orders) == 1
def test_daily_scan_requires_growth(mk):
    b, e = mk(rules=scan_rules(), funds=Funds({"rev_yoy": 3, "eps_positive": True}), mtc=15, news_items=[]); e.step(); assert not b.orders
def test_daily_scan_not_before_window(mk):
    b, e = mk(rules=scan_rules(), funds=Funds({"rev_yoy": 25, "eps_positive": True}), mtc=120, news_items=[]); e.step(); assert not b.orders
def test_swing_time_stop(mk):
    r = scan_rules(); r["swing"]["scan"]["enabled"] = False
    b, e = mk(rules=r, mtc=15, news_items=[]); b._pos = [{"symbol": "AAA", "market_value": "4000"}]
    old = str(date.today() - timedelta(days=21))
    e.state["meta"] = {"AAA": {"strategy": "swing", "side": "long", "entry_date": old, "ts": 1e12}}
    e.step(); assert b.closed == ["AAA"]
def test_swing_not_closed_before_max_hold(mk):
    r = scan_rules(); r["swing"]["scan"]["enabled"] = False
    b, e = mk(rules=r, mtc=15, news_items=[]); b._pos = [{"symbol": "AAA", "market_value": "4000"}]
    e.state["meta"] = {"AAA": {"strategy": "swing", "side": "long", "entry_date": str(date.today() - timedelta(days=3)), "ts": 1e12}}
    e.step(); assert not b.closed

def test_reconcile_drops_stale_meta_only(mk):
    b, e = mk(news_items=[]); import time
    e.state["meta"] = {"OLD": {"strategy": "day", "ts": time.time() - 3600}, "NEW": {"strategy": "day", "ts": time.time()}}
    e.step(); assert "OLD" not in e.state["meta"] and "NEW" in e.state["meta"]

# ---------- session ----------
def test_session_exits_when_market_far(mk):
    brain = FakeBrain(10); b, e = mk(brain=brain); b._clock = clock(240, is_open=False)
    bot.session(e, sleep=lambda s: None); assert not b.orders and not brain.calls
def test_session_trades_then_ends_at_close(mk):
    b, e = mk(); calls = {"n": 0}
    def fake_sleep(s):
        calls["n"] += 1
        if calls["n"] >= 2: b._clock = clock(240, is_open=False)
    bot.session(e, sleep=fake_sleep); assert len(b.orders) == 1 and calls["n"] == 2
def test_ts_nanoseconds(): assert bot._ts("2026-10-29T10:00:00.337868559-04:00").year == 2026
def test_weekdays_between():
    assert bot.weekdays_between("2026-10-23", "2026-10-30") == 5      # ו' -> ה' הבאה
