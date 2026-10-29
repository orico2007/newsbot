import sys, pathlib, os
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from datetime import datetime, timezone, timedelta
import pytest
from rules_loader import load_rules
from models import Verdict, NewsItem
from risk import evaluate
from broker import MockBroker
from brain import parse_verdict
import bot

R = load_rules(str(pathlib.Path(__file__).parent.parent / "rules.yaml"))
ACC = {"equity": 100000, "last_equity": 100000, "buying_power": 200000}
def ev(score=9, direction="bullish", price=50, prev=49, adv=1e7, acc=ACC, pos=(), state=None, open_=True, sym="AAA"):
    return evaluate(R, Verdict(score, direction, ""), price, prev, adv, acc, list(pos), sym, state if state is not None else {}, open_)

def test_buy_sizing_and_levels():
    d = ev()
    assert d.ok and d.qty == 100 and d.stop_price == 48.5 and d.take_profit_price == 53.0   # 5% של 100k = 5000 / 50
def test_score_8_rejected():           assert not ev(score=8).ok
def test_score_9_accepted():           assert ev(score=9).ok
def test_bearish_rejected():           assert not ev(direction="bearish", score=10).ok
def test_market_closed():              assert not ev(open_=False).ok
def test_penny():                      assert not ev(price=3).ok
def test_illiquid():                   assert not ev(adv=1e5).ok
def test_chasing():                    assert not ev(price=53, prev=49).ok
def test_duplicate_position():         assert not ev(pos=[{"symbol": "AAA"}]).ok
def test_max_positions():              assert not ev(pos=[{"symbol": s} for s in "BCDEF"]).ok
def test_daily_loss_halts():
    st = {}
    d = ev(acc={"equity": 97500, "last_equity": 100000, "buying_power": 1e5}, state=st)
    assert not d.ok and st["halted"] and not ev(state=st).ok
def test_buying_power_cap():           assert ev(acc={"equity": 100000, "last_equity": 100000, "buying_power": 2000}).qty == 40
def test_parse_garbage():              assert parse_verdict("lol").score == 1
def test_parse_clamps():               assert parse_verdict('{"score": 99, "direction":"bullish"}').score == 10

class FakeBrain:
    def __init__(self, score, direction="bullish"): self.v = Verdict(score, direction, "t")
    def rate(self, *a): return self.v

def mkbroker(age_min=1, symbols=("AAA",)):
    b = MockBroker(); b.snap["AAA"] = (50, 49, 1e7)
    b._news = [NewsItem("1", "Big contract", "", list(symbols), datetime.now(timezone.utc) - timedelta(minutes=age_min))]
    return b

def run(b, brain, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path); bot.STATE_FILE = tmp_path / "s.json"; bot.JOURNAL = tmp_path / "j.csv"
    bot.run_once(b, brain, R, {"seen": [], "trades_today": 0, "halted": False})

def test_e2e_buy(tmp_path, monkeypatch):
    b = mkbroker(); run(b, FakeBrain(10), tmp_path, monkeypatch)
    assert b.orders == [("AAA", 100, 48.5, 53.0)]
def test_e2e_low_score_no_buy(tmp_path, monkeypatch):
    b = mkbroker(); run(b, FakeBrain(7), tmp_path, monkeypatch); assert not b.orders
def test_e2e_stale_news(tmp_path, monkeypatch):
    b = mkbroker(age_min=40); run(b, FakeBrain(10), tmp_path, monkeypatch); assert not b.orders
def test_e2e_multi_symbol_news_ignored(tmp_path, monkeypatch):
    b = mkbroker(symbols=("AAA", "BBB")); run(b, FakeBrain(10), tmp_path, monkeypatch); assert not b.orders
def test_news_not_processed_twice(tmp_path, monkeypatch):
    b = mkbroker(); monkeypatch.chdir(tmp_path); bot.STATE_FILE = tmp_path / "s.json"; bot.JOURNAL = tmp_path / "j.csv"
    st = {"seen": [], "trades_today": 0, "halted": False}
    bot.run_once(b, FakeBrain(10), R, st); b._pos.clear(); bot.run_once(b, FakeBrain(10), R, st)
    assert len(b.orders) == 1

def test_market_closed_skips_scoring(tmp_path, monkeypatch):
    b = mkbroker(); b.is_open = False
    class Boom:
        def rate(self, *a): raise AssertionError("should not score while closed")
    run(b, Boom(), tmp_path, monkeypatch); assert not b.orders

def test_ts_nanoseconds():
    assert bot._ts("2026-10-29T10:00:00.337868559-04:00").year == 2026

def test_session_exits_when_market_far(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path); bot.STATE_FILE = tmp_path / "s.json"; bot.JOURNAL = tmp_path / "j.csv"
    b = mkbroker(); b._clock = {"is_open": False, "timestamp": "2026-10-29T05:00:00-04:00", "next_open": "2026-10-29T09:30:00-04:00"}
    class Boom:
        def rate(self, *a): raise AssertionError
    bot.session(b, Boom(), R, sleep=lambda s: None); assert not b.orders

def test_session_trades_then_ends_at_close(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path); bot.STATE_FILE = tmp_path / "s.json"; bot.JOURNAL = tmp_path / "j.csv"
    b = mkbroker(); calls = {"n": 0}
    open_c = {"is_open": True}; closed_c = {"is_open": False, "timestamp": "2026-10-29T16:01:00-04:00", "next_open": "2026-10-30T09:30:00-04:00"}
    def fake_sleep(s):
        calls["n"] += 1; b._clock = closed_c if calls["n"] >= 2 else open_c
    b._clock = open_c
    bot.session(b, FakeBrain(10), R, sleep=fake_sleep)
    assert len(b.orders) == 1 and calls["n"] == 2
