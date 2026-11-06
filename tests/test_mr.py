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
    b, e = mk3(); _setup(b, e); e.mkt.regime = "bear"; e.mkt.spy_above200 = False
    assert e._mr_scan(NOW) == 0 and not b.orders
    e.mkt.regime = "neutral"; e.mkt.spy_above200 = True
    assert e._mr_scan(NOW) == 1 and b.orders[0][2] == "buy"
    assert e.state["meta"]["AAA"]["pattern"] == "mr_A"

def test_engine_exits_above_prior_high(mk3):
    b, e = mk3(); _setup(b, e); e.mkt.regime = "bull"; e.mkt.spy_above200 = True; e._mr_scan(NOW)
    b._pos = [{"symbol": "AAA", "qty": "10", "current_price": "1", "avg_entry_price": "1", "market_value": "10"}]
    d = b.bar_data[("AAA", "1Day")]; d[-1] = dict(d[-1], c=d[-2]["h"] * 1.01, h=d[-2]["h"] * 1.02)
    e.state["swing_done"] = None; e.swing_pass(NOW, 10)
    assert "AAA" in b.closed

def test_rule_f_fires_without_ibs_condition():
    d = uptrend_pullback(); d[-1]["l"] = d[-1]["c"] * 0.9; d[-1]["h"] = d[-1]["c"] * 1.01     # close near the high: A (IBS) fails
    s = mr.detect(d)
    assert s and s.name in ("mr_F", "mr_E")

def test_mr_position_size_is_10_pct(mk3):
    b, e = mk3(); _setup(b, e); e.mkt.regime = "bull"; e.mkt.spy_above200 = True; e._mr_scan(NOW)
    qty, px = b.orders[0][1], b.snap["AAA"][0]
    assert abs(qty * px / 100000 - 0.10) < 0.02

from helpers import FakeBrain, news as _news

def test_bearish_news_vetoes_dip(mk3):
    b, e = mk3(); _setup(b, e); e.mkt.regime = "bull"; e.mkt.spy_above200 = True
    e.brain = FakeBrain(8, "bearish", "swing"); b._news = [_news("1", ("AAA",), 600, "Company slashes guidance")]
    assert e._mr_scan(NOW) == 0 and not b.orders

def test_neutral_or_no_news_allows_dip(mk3):
    b, e = mk3(); _setup(b, e); e.mkt.regime = "bull"; e.mkt.spy_above200 = True
    b._news = [_news("1", ("AAA",), 600, "Company holds conference")]
    assert e._mr_scan(NOW) == 1

def test_shrinking_revenue_vetoes_dip(mk3):
    class F:
        def get(self, s): return {"rev_yoy": -5, "eps_positive": True}
    b, e = mk3(); _setup(b, e); e.mkt.regime = "bull"; e.mkt.spy_above200 = True; e.funds = F()
    assert e._mr_scan(NOW) == 0

def test_pattern_scan_blocked_by_bearish_news(mk3):
    from test_v3_engine import _flag_setup
    b, e = mk3(); _flag_setup(b)
    e.brain = FakeBrain(8, "bearish", "swing"); b._news = [_news("1", ("AAA",), 600, "Company slashes guidance")]
    e.swing_pass(NOW, 10)
    assert not b.orders

def test_new_entry_logs_previous_trade_in_same_symbol(mk3):
    import csv, bot as _bot
    b, e = mk3(); _setup(b, e); e.mkt.regime = "bull"; e.mkt.spy_above200 = True
    e.state["meta"]["AAA"] = {"strategy": "swing", "side": "long", "entry_date": "2026-11-03", "ts": 1.0, "entry": 100.0, "fill": 100.0, "qty": 5, "qty0": 5,
                              "stop0": 95.0, "pattern": "old", "last": 103.0}
    b.fills = {"AAA": 104.0}
    e._mr_scan(NOW)
    rows = list(csv.DictReader(open(_bot.DATA / "trades.csv")))
    assert rows and rows[-1]["symbol"] == "AAA" and rows[-1]["pattern"] == "old" and float(rows[-1]["pnl_pct"]) > 0
    assert e.state["meta"]["AAA"]["pattern"] == "mr_A"

def test_report_reads_journal_with_old_short_header(tmp_path):
    import report
    p = tmp_path / "journal.csv"
    p.write_text("time,symbol,headline,score,direction,reason,action,detail\n" + "2026-11-04T20:00:00+00:00,XOM,h,,,,,,,ENTER,buy,\n", encoding="utf-8")
    assert [r["action"] for r in report.read_journal(p, "2026-11-04")] == ["ENTER"]

def test_mr_scans_sector_constituents_beyond_watchlist(mk3):
    import market
    sym = next(x for x in market.SECTOR_OF if x.isalpha())
    b, e = mk3(); e.r["swing"]["watchlist"] = ["ZZZ"]
    d = uptrend_pullback(); b.bar_data[(sym, "1Day")] = d; b.snap[sym] = (d[-1]["c"], d[-2]["c"], 2e8)
    e.mkt.regime = "bull"; e.mkt.spy_above200 = True
    assert e._mr_scan(NOW) == 1 and b.orders[0][0] == sym

def test_pattern_trades_are_smaller_than_mr_trades(mk3):
    from test_v3_engine import _flag_setup
    b, e = mk3(); _flag_setup(b); e.swing_pass(NOW, 10)
    qty_pattern = b.orders[0][1] * b.snap["AAA"][0] / 100000
    assert qty_pattern < 0.05          # half of a ~4-6% pattern position

def _calm(n=240):
    return [bar(50 + 0.1 * i, 2_000_000, spread=0.3) for i in range(n)]

def test_breadth_filter_blocks_lone_dip(mk3):
    b, e = mk3(); e.r["swing"]["watchlist"] = ["AAA"] + [f"N{i}" for i in range(40)]
    _setup(b, e); e.mkt.regime = "bull"; e.mkt.spy_above200 = True
    for i in range(40): b.bar_data[(f"N{i}", "1Day")] = _calm()
    assert e._mr_scan(NOW) == 0 and not b.orders             # 1 of 41 stocks oversold = 2% < 10%

def test_breadth_filter_allows_market_wide_washout(mk3):
    b, e = mk3(); e.r["swing"]["watchlist"] = ["AAA"] + [f"N{i}" for i in range(9)]
    _setup(b, e); e.mkt.regime = "bull"; e.mkt.spy_above200 = True
    for i in range(9): b.bar_data[(f"N{i}", "1Day")] = _calm()
    # fewer than 30 stocks known -> filter cannot judge breadth, so it stays out of the way
    assert e._mr_scan(NOW) == 1

def test_weakest_sector_ranked_first(mk3, monkeypatch):
    import market
    secs = {}
    for sym, sec in market.SECTOR_OF.items():
        if sym.isalpha(): secs.setdefault(sec, []).append(sym)
    (s1, l1), (s2, l2) = [(k, v) for k, v in secs.items() if len(v) >= 3][:2]
    X, Y = l1[0], l2[0]
    b, e = mk3(); e.r["swing"]["watchlist"] = []; e.r["swing"]["mr"]["new_per_day"] = 1
    e.mkt.regime = "bull"; e.mkt.spy_above200 = True
    def bars_for(chg):                                  # last 3 days move by chg
        d = _calm(); last = d[-4]["c"]
        for k, f in zip((-3, -2, -1), (1, 1, 1)): d[k] = bar(last * (1 + chg * (4 + k)), 2_000_000, spread=0.3)
        return d
    sig_ids = {}
    for sym in l1 + l2:
        weak = sym in l1
        d = bars_for(-0.02 if weak else 0.02); b.bar_data[(sym, "1Day")] = d; b.snap[sym] = (d[-1]["c"], d[-2]["c"], 2e8)
    from patterns import Signal
    monkeypatch.setattr(bot.mr, "detect", lambda daily, stop=4.0: Signal("mr_A", "long", "swing", daily[-1]["c"], daily[-1]["c"] * 0.9, daily[-1]["c"] * 1.2) if daily[-1]["c"] and (daily is b.bar_data[(X, "1Day")] or daily is b.bar_data[(Y, "1Day")]) else None)
    assert e._mr_scan(NOW) == 1
    assert b.orders[0][0] == X                          # X's sector fell, Y's sector rose: weakest sector first
