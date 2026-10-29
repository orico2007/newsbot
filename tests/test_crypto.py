import pathlib
from datetime import datetime, timezone, timedelta
import crypto
from broker import MockBroker
from models import Verdict, NewsItem
from tests.helpers import R, FakeBrain
from tests.test_patterns import ramp, B

NOW = datetime.now(timezone.utc)

def base_break_bars(top=200.0):
    bars = ramp(top * 0.5, top, 120, v=1000) + [B(top + (0.6 if i % 2 else -0.6), top + 1, top - 1, top, 1000) for i in range(25)]
    bars += [B(top + 0.5, top * 1.04, top + 0.4, top * 1.035, 2600)]
    return bars

def eng(tmp_path, monkeypatch, brain=None):
    monkeypatch.setattr(crypto, "JOURNAL", tmp_path / "j.csv"); monkeypatch.setattr(crypto, "STATE_FILE", tmp_path / "s.json")
    b = MockBroker()
    b.prices["ETH/USD"] = 207.0; b.prices["BTC/USD"] = 60000.0
    b.bar_data[("BTC/USD", "1Day")] = ramp(30000, 60000, 200)
    b.bar_data[("ETH/USD", "1Day")] = base_break_bars()
    state = {"meta": {}, "seen": [], "last_scan": 0}
    return b, crypto.CryptoEngine(b, brain or FakeBrain(5), R, state)

def test_scan_enters_pattern_long_only(tmp_path, monkeypatch):
    b, e = eng(tmp_path, monkeypatch)
    e.step(NOW)
    assert any(o[0] == "ETH/USD" and o[2] == "buy" for o in b.simple)
    m = e.state["meta"]["ETHUSD"]
    assert m["stop"] < m["entry"] < m["target"]
    assert all(o[2] == "buy" for o in b.simple)          # אין שורט בקריפטו

def test_btc_downtrend_blocks_alts(tmp_path, monkeypatch):
    b, e = eng(tmp_path, monkeypatch)
    b.bar_data[("BTC/USD", "1Day")] = ramp(60000, 30000, 200)
    e.step(NOW)
    assert not [o for o in b.simple if o[0] != "BTC/USD"]

def test_stop_exit(tmp_path, monkeypatch):
    b, e = eng(tmp_path, monkeypatch)
    e.step(NOW)
    stop = e.state["meta"]["ETHUSD"]["stop"]
    b.prices["ETH/USD"] = stop - 0.5
    e.step(NOW + timedelta(minutes=1))
    assert "ETHUSD" in b.closed

def test_trailing_moves_stop_up_never_down(tmp_path, monkeypatch):
    b, e = eng(tmp_path, monkeypatch)
    e.step(NOW)
    m = e.state["meta"]["ETHUSD"]; s0 = m["stop"]
    b.prices["ETH/USD"] = m["entry"] + 6 * m["atr"] * 0.5 + m["atr"]
    e.manage(NOW); s1 = m["stop"]
    assert s1 > s0
    b.prices["ETH/USD"] = m["entry"] + m["atr"]       # נסיגה קלה, לא מורידים סטופ
    e.manage(NOW)
    assert m["stop"] >= s1

def test_size_cap_exposure(tmp_path, monkeypatch):
    b, e = eng(tmp_path, monkeypatch)
    e.step(NOW)
    spent = sum(float(p["market_value"]) for p in b.positions())
    assert 0 < spent <= 100000 * R["crypto"]["max_gross_pct"] / 100 + 1

def test_bearish_news_exits(tmp_path, monkeypatch):
    brain = FakeBrain(9, "bearish")
    b, e = eng(tmp_path, monkeypatch, brain)
    e.step(NOW)
    b._news = [NewsItem("n1", "Exchange hacked", "", ["ETH/USD"], NOW, "")]
    e.step(NOW + timedelta(minutes=1))
    assert "ETHUSD" in b.closed

def test_bullish_news_enters_when_trend_ok(tmp_path, monkeypatch):
    brain = FakeBrain(9, "bullish")
    b, e = eng(tmp_path, monkeypatch, brain)
    b.bar_data[("ETH/USD", "1Day")] = ramp(100, 200, 120)     # ללא תבנית, אבל מעל SMA20
    e.state["last_scan"] = 10**12                              # מדלגים על הסריקה
    b._news = [NewsItem("n2", "ETF approved", "", ["ETH/USD"], NOW, "")]
    e.step(NOW)
    assert any(o[0] == "ETH/USD" for o in b.simple)
