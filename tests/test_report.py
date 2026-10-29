import json, bot, report
from helpers import *
from broker import MockBroker
from test_engine import clock
from test_v3_engine import NOW

def test_report_contents(tmp_path):
    day = "2026-10-29"
    j = tmp_path / "j.csv"
    j.write_text("time,symbol,headline,score,direction,event,horizon,strategy,side,action,detail,reason\n"
                 f"{day}T14:00:00+00:00,AAA,Big win,9,bullish,x,intraday,day,long,ENTER,buy qty=10,r\n"
                 f"{day}T15:00:00+00:00,AAA,,,,,,day,long,EXIT,end-of-day flatten,\n"
                 f"{day}T15:01:00+00:00,BBB,h,9,bullish,x,intraday,day,long,blocked,cooldown after recent exit,r\n"
                 "2026-10-28T10:00:00+00:00,OLD,h,9,bullish,x,intraday,day,long,ENTER,old,r\n", encoding="utf-8")
    md = report.write(day, {"equity": "101000", "last_equity": "100000"}, [{"symbol": "AAA", "side": "long", "qty": "5", "unrealized_pl": "12.5"}],
                      j, tmp_path / "none.csv", tmp_path / "none.json", tmp_path)
    assert "+1,000.00 (+1.00%)" in md and "Entries: 1" in md and "OLD" not in md and "cooldown" in md
    assert (tmp_path / "reports" / f"{day}.md").exists()

def test_engine_writes_report_near_close_once(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path); bot.STATE_FILE = tmp_path / "s.json"; bot.JOURNAL = tmp_path / "j.csv"
    b = MockBroker(); b._news = []; b._clock = clock(3)
    e = bot.Engine(b, FakeBrain(1, "neutral"), R, bot.roll({}), None)
    e.step(NOW)
    assert (tmp_path / "data" / "report.md").exists() or (bot.DATA / "report.md").exists()
    assert e.state["report_done"]

def test_backtest_disabled_detectors_are_skipped(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path); bot.STATE_FILE = tmp_path / "s.json"; bot.JOURNAL = tmp_path / "j.csv"
    monkeypatch.setattr(bot, "DATA", tmp_path)
    (tmp_path / "backtest.json").write_text(json.dumps({"disabled": ["flag"]}), encoding="utf-8")
    b = MockBroker(); e = bot.Engine(b, FakeBrain(1, "neutral"), R, bot.roll({}), None)
    assert e._disabled_patterns() == {"flag"}
