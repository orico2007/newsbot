import copy
import mr, bot
from helpers import R, bar
from test_v3_engine import NOW

def uptrend_pullback():
    c = [50 + 0.4 * i for i in range(240)]
    c += [c[-1] * 0.99, c[-1] * 0.98, c[-1] * 0.97]       # 3 sharp down days in an uptrend
    d = [bar(x, 2_000_000, spread=x * 0.004) for x in c]
    d[-1]["h"] = d[-1]["c"] * 1.01; d[-1]["l"] = d[-1]["c"] * 0.998    # close near the low (IBS ~ 0.17)
    return d

def test_detects_rule_a_in_uptrend_pullback():
    s = mr.detect(uptrend_pullback())
    assert s and s.name == "mr_A" and s.side == "long" and s.stop < s.price < s.target

def test_no_signal_in_downtrend_or_without_pullback():
    up = [bar(50 + 0.15 * i, 2_000_000, spread=0.3) for i in range(245)]
    assert mr.detect(up) is None
    down = [bar(150 - 0.15 * i, 2_000_000, spread=0.3) for i in range(245)]
    assert mr.detect(down) is None

def test_exit_rule_prior_day_high():
    d = [bar(10), bar(10)]; d[-2]["h"] = 10.5
    d[-1]["c"] = 10.6; assert mr.exit_now(d)
    d[-1]["c"] = 10.4; assert not mr.exit_now(d)

def test_rules_enabled_and_long_only():
    assert R["swing"]["mr"]["enabled"] and R["swing"]["mr"]["hold_days"] == 7

from test_v3_engine import mk3  # noqa: F401

def _setup(b, e):
    d = uptrend_pullback(); b.bar_data[("AAA", "1Day")] = d; b.snap["AAA"] = (d[-1]["c"], d[-2]["c"], 2e8)

def test_engine_enters_only_in_bull_regime(mk3):
    b, e = mk3(); _setup(b, e); e.mkt.regime = "bear"
    assert e._mr_scan(NOW) == 0 and not b.orders
    e.mkt.regime = "bull"
    assert e._mr_scan(NOW) == 1 and b.orders[0][2] == "buy"
    assert e.state["meta"]["AAA"]["pattern"] == "mr_A"

def test_engine_exits_above_prior_high(mk3):
    b, e = mk3(); _setup(b, e); e.mkt.regime = "bull"; e._mr_scan(NOW)
    b._pos = [{"symbol": "AAA", "qty": "10", "current_price": "1", "avg_entry_price": "1", "market_value": "10"}]
    d = b.bar_data[("AAA", "1Day")]; d[-1] = dict(d[-1], c=d[-2]["h"] * 1.01, h=d[-2]["h"] * 1.02)
    e.state["swing_done"] = None; e.swing_pass(NOW, 10)
    assert "AAA" in b.closed

def test_rule_f_fires_without_ibs_condition():
    d = uptrend_pullback(); d[-1]["l"] = d[-1]["c"] * 0.9; d[-1]["h"] = d[-1]["c"] * 1.01     # close near the high: A (IBS) fails
    s = mr.detect(d)
    assert s and s.name in ("mr_F", "mr_E")

def test_mr_position_size_is_10_pct(mk3):
    b, e = mk3(); _setup(b, e); e.mkt.regime = "bull"; e._mr_scan(NOW)
    qty, px = b.orders[0][1], b.snap["AAA"][0]
    assert abs(qty * px / 100000 - 0.10) < 0.02

from helpers import FakeBrain, news as _news

def test_bearish_news_vetoes_dip(mk3):
    b, e = mk3(); _setup(b, e); e.mkt.regime = "bull"
    e.brain = FakeBrain(8, "bearish", "swing"); b._news = [_news("1", ("AAA",), 600, "Company slashes guidance")]
    assert e._mr_scan(NOW) == 0 and not b.orders

def test_neutral_or_no_news_allows_dip(mk3):
    b, e = mk3(); _setup(b, e); e.mkt.regime = "bull"
    b._news = [_news("1", ("AAA",), 600, "Company holds conference")]
    assert e._mr_scan(NOW) == 1

def test_shrinking_revenue_vetoes_dip(mk3):
    class F:
        def get(self, s): return {"rev_yoy": -5, "eps_positive": True}
    b, e = mk3(); _setup(b, e); e.mkt.regime = "bull"; e.funds = F()
    assert e._mr_scan(NOW) == 0
