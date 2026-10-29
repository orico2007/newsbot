import bot, scorecard, alerts
from helpers import *
from broker import MockBroker
from test_engine import clock
from test_v3_engine import NOW

def eng(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path); bot.STATE_FILE = tmp_path / "s.json"; bot.JOURNAL = tmp_path / "j.csv"; monkeypatch.setattr(bot, "DATA", tmp_path)
    sent = []; monkeypatch.setattr(alerts, "send", lambda text, title="": sent.append(text))
    b = MockBroker(); b._news = []; b._clock = clock(240)
    return b, bot.Engine(b, FakeBrain(1, "neutral"), R, bot.roll({}), None), sent

def test_slippage_and_trade_record(tmp_path, monkeypatch):
    b, e, sent = eng(tmp_path, monkeypatch)
    e.state["meta"]["AAA"] = {"strategy": "swing", "side": "long", "entry": 100.0, "stop": 96, "stop0": 96, "ext": 100, "atr": 2, "ts": 0,
                              "entry_date": "2026-10-20", "pattern": "flag"}
    pos = [{"symbol": "AAA", "current_price": "104", "avg_entry_price": "100.2", "qty": "10", "side": "long"}]
    e.track_positions(NOW, pos)
    assert abs(e.state["meta"]["AAA"]["slip"] - 0.2) < 1e-9
    b.fills["AAA"] = 105.0
    e.reconcile([])                                           # הפוזיציה נסגרה
    t = scorecard.read_trades(tmp_path / "trades.csv")
    assert len(t) == 1 and t[0]["pattern"] == "flag" and abs(t[0]["pnl_pct"] - 4.790) < 0.01 and t[0]["R"] > 1 and t[0]["entry_slip_pct"] == 0.2

def test_exit_falls_back_to_last_price(tmp_path, monkeypatch):
    b, e, _ = eng(tmp_path, monkeypatch)
    e.state["meta"]["BBB"] = {"strategy": "day", "side": "short", "entry": 50.0, "stop0": 51.5, "ts": 0, "pattern": "orb", "last": 48.0, "fill": 50.0, "entry_date": "2026-10-29"}
    e.reconcile([])
    t = scorecard.read_trades(tmp_path / "trades.csv")
    assert t and t[0]["pnl_pct"] > 0 and t[0]["side"] == "short"

def test_scorecard_disables_losers():
    rows = [{"closed": "x", "symbol": "A", "strategy": "swing", "pattern": "flag", "side": "long", "pnl_pct": -2.0, "R": -1.0, "entry_slip_pct": 0.1}] * 16
    rows += [{"closed": "x", "symbol": "A", "strategy": "swing", "pattern": "orb", "side": "long", "pnl_pct": 2.0, "R": 1.0, "entry_slip_pct": None}] * 16
    st = scorecard.compute(rows)
    assert scorecard.losers(st) == ["flag"] and st["ALL"]["n"] == 32 and "flag" in scorecard.markdown(st, ["flag"])
    assert "No closed trades" in scorecard.markdown({}, [])

def test_alert_on_entry(tmp_path, monkeypatch):
    b, e, sent = eng(tmp_path, monkeypatch)
    e._j(NOW, "AAA", "x", None, "day", "long", "ENTER", "buy qty=1")
    e._j(NOW, "AAA", "x", None, "day", "long", "blocked", "nope")
    assert len(sent) == 1 and "ENTER AAA" in sent[0]

def test_disabled_merges_scorecard(tmp_path, monkeypatch):
    import json
    b, e, _ = eng(tmp_path, monkeypatch)
    (tmp_path / "scorecard.json").write_text(json.dumps({"disabled": ["orb"]}), encoding="utf-8")
    (tmp_path / "backtest.json").write_text(json.dumps({"disabled": ["flag"]}), encoding="utf-8")
    assert e._disabled_patterns() == {"orb", "flag"}

def test_alert_on_closed_trade_with_pnl(tmp_path, monkeypatch):
    b, e, sent = eng(tmp_path, monkeypatch)
    e.state["meta"]["AAA"] = {"strategy": "swing", "side": "long", "entry": 100.0, "fill": 100.0, "qty": 10, "stop0": 96, "ts": 0, "entry_date": "2026-10-20", "pattern": "flag", "last": 104}
    b.fills["AAA"] = 105.0
    e.reconcile([])
    assert any("WIN AAA" in t and "+5.00%" in t and "+50.00 USD" in t for t in sent)

def test_alert_on_loss_short(tmp_path, monkeypatch):
    b, e, sent = eng(tmp_path, monkeypatch)
    e.state["meta"]["BBB"] = {"strategy": "day", "side": "short", "entry": 50.0, "fill": 50.0, "qty": 20, "stop0": 51.5, "ts": 0, "pattern": "orb", "last": 51.0, "entry_date": "2026-10-29"}
    e.reconcile([])
    assert any("LOSS BBB" in t and "-2.00" in t or "LOSS BBB" in t and "-20.00 USD" in t for t in sent)

def test_alerts_never_hit_the_network_under_pytest(monkeypatch):
    import requests
    calls = []
    monkeypatch.setattr(requests, "post", lambda *a, **k: calls.append(a))
    monkeypatch.setenv("NTFY_TOPIC", "should-not-be-used")
    alerts.send("hello")                       # PYTEST_CURRENT_TEST פעיל: לא יוצא החוצה
    assert calls == []
