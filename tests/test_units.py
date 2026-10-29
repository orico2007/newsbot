from helpers import *
import indicators as ind, chart, fundamentals as fu, brain
from risk import evaluate_entry

ACC = {"equity": 100000, "last_equity": 100000, "buying_power": 200000}
def ev(strategy="day", side="long", price=50, prev=49, adv=2e6, acc=ACC, pos=(), state=None, open_=True, atr=1.5, shortable=True):
    return evaluate_entry(R, strategy, side, "AAA", price, prev, adv, acc, list(pos), state if state is not None else {}, open_, atr=atr, shortable=shortable)

# ----- indicators
def test_rsi_extremes():
    assert ind.rsi([float(i) for i in range(30)]) == 100.0
    assert ind.rsi([float(30 - i) for i in range(30)]) < 1
def test_atr_constant_range():
    bars = [bar(10, spread=0.5) for _ in range(30)]
    assert abs(ind.atr(bars) - 1.0) < 1e-9
def test_vwap_weighted():
    assert abs(ind.vwap([bar(10, 1), bar(20, 3)]) - 17.5) < 1e-9

# ----- chart
CFG = R["day"]["chart"]
def test_intraday_long_ok():
    ok, why, snap = chart.intraday_check(intraday_up(), "long", CFG); assert ok, (why, snap)
def test_intraday_long_blocked_in_downtrend():
    ok, why, _ = chart.intraday_check(intraday_down(), "long", CFG); assert not ok and "VWAP" in why
def test_intraday_short_ok():
    ok, why, snap = chart.intraday_check(intraday_down(), "short", CFG); assert ok, (why, snap)
def test_intraday_low_volume_blocked():
    ok, why, _ = chart.intraday_check(intraday_up(spike=1000), "long", CFG); assert not ok and "volume" in why
def test_intraday_too_few_bars():
    assert not chart.intraday_check(intraday_up(2), "long", CFG)[0]
def test_swing_scan_ok_and_downtrend_rejected():
    ok, why, s = chart.swing_scan_ok(daily_pullback(), R["swing"]["scan"]); assert ok, (why, s)
    assert not chart.swing_scan_ok(daily_downtrend(), R["swing"]["scan"])[0]
def test_trend_ok_sides():
    assert chart.trend_ok(daily_pullback(), "long")[0] and not chart.trend_ok(daily_pullback(), "short")[0]
    assert chart.trend_ok(daily_downtrend(), "short")[0]

# ----- fundamentals (פורמט XBRL של SEC)
def q(end, start, val, form="10-Q", filed="2026-01-01"): return {"start": start, "end": end, "val": val, "form": form, "filed": filed}
FACTS = {"facts": {"us-gaap": {
    "Revenues": {"units": {"USD": [q("2025-06-30", "2025-04-01", 100), q("2026-06-30", "2026-04-01", 125),
                                  q("2026-06-30", "2026-01-01", 240, "10-Q")]}},   # חצי שנה - מתעלמים
    "EarningsPerShareDiluted": {"units": {"USD/shares": [q("2025-06-30", "2025-04-01", 1.0), q("2026-06-30", "2026-04-01", 1.3)]}}}}}
def test_fundamentals_parse():
    f = fu.parse_facts(FACTS)
    assert f["rev_yoy"] == 25.0 and f["eps_yoy"] == 30.0 and f["eps_positive"] is True and f["as_of"] == "2026-06-30"
def test_fundamentals_missing_is_safe():
    assert fu.parse_facts({"facts": {}})["rev_yoy"] is None
def test_fundamentals_ok_rules():
    cfg = R["swing"]["scan"]
    assert chart.fundamentals_ok({"rev_yoy": 25, "eps_positive": True}, cfg)
    assert not chart.fundamentals_ok({"rev_yoy": 5, "eps_positive": True}, cfg)
    assert not chart.fundamentals_ok({"rev_yoy": 25, "eps_positive": False}, cfg)
    assert not chart.fundamentals_ok(None, cfg)
class FakeHttp:
    def __init__(self): self.urls = []
    def get(self, url, **kw):
        self.urls.append(url)
        class Rsp:
            def raise_for_status(s): pass
            def json(s): return {"0": {"cik_str": 1, "ticker": "AAA"}} if "company_tickers" in url else FACTS
        return Rsp()
def test_fundamentals_client_caches():
    h = FakeHttp(); f = fu.Fundamentals(h)
    assert f.get("AAA")["rev_yoy"] == 25.0 and f.get("AAA") and len(h.urls) == 2
    assert f.get("ZZZ") is None

# ----- brain
def test_parse_garbage_and_clamp():
    assert brain.parse_verdict("lol").score == 1
    v = brain.parse_verdict('{"score": 99, "direction":"bullish","event":"earnings","horizon":"swing"}')
    assert (v.score, v.event, v.horizon) == (10, "earnings", "swing")
    assert brain.parse_verdict('{"score": 9, "direction":"neutral"}').score == 5
    assert brain.parse_verdict('{"score": 9, "direction":"bullish","event":"x","horizon":"y"}').horizon == "intraday"
def test_prompt_contains_body_and_fundamentals_without_html():
    p = brain.build_prompt("AAA", "Q2 results", "", "<p>Revenue <b>up</b> 25%</p>", {"rev_yoy": 25})
    assert "Revenue up 25%" in p and "<b>" not in p and "rev_yoy" in p

# ----- risk gate
def test_day_long_sizing():
    d = ev(); assert d.ok and d.qty == 100 and d.side == "buy" and d.stop_price == 48.5 and d.take_profit_price == 53.0 and d.tif == "day"
def test_day_short_levels_and_smaller_size():
    d = ev(side="short", prev=51); assert d.ok and d.qty == 60 and d.side == "sell" and d.stop_price == 51.5 and d.take_profit_price == 47.0
def test_short_blocked_if_not_shortable():   assert not ev(side="short", shortable=False).ok
def test_short_chasing_blocked():            assert not ev(side="short", price=45, prev=50).ok
def test_long_chasing_blocked():             assert not ev(price=53, prev=49).ok
def test_market_closed_penny_illiquid():
    assert not ev(open_=False).ok and not ev(price=3).ok and not ev(adv=1e5).ok
def test_duplicate_and_max_positions():
    assert not ev(pos=[{"symbol": "AAA"}]).ok
    assert not ev(pos=[{"symbol": s} for s in "BCDEFGHI"]).ok
def test_strategy_slot_limit():
    st = {"meta": {s: {"strategy": "day"} for s in "BCD"}}
    assert not ev(pos=[{"symbol": s} for s in "BCD"], state=st).ok
def test_gross_exposure_cap():
    pos = [{"symbol": "B", "market_value": "58000"}]
    assert ev(pos=pos).qty == 40            # נשארו 2000$ עד תקרת 60%
    assert not ev(pos=[{"symbol": "B", "market_value": "59990"}]).ok
def test_daily_loss_halts():
    st = {}; d = ev(acc={"equity": 97500, "last_equity": 100000, "buying_power": 1e5}, state=st)
    assert not d.ok and st["halted"] and not ev(state=st).ok
def test_swing_uses_atr_and_gtc():
    d = ev("swing", atr=1.0); assert d.ok and d.tif == "gtc" and d.stop_price == 48.0 and d.take_profit_price == 54.0 and d.qty == 80
def test_swing_stop_capped_by_max_pct():
    d = ev("swing", atr=10.0); assert d.stop_price == 46.0       # 8% מ-50
def test_swing_needs_atr():                  assert not ev("swing", atr=None).ok
def test_disabled_strategy():
    import copy; r = copy.deepcopy(R); r["day"]["enabled"] = False
    assert not evaluate_entry(r, "day", "long", "A", 50, 49, 2e6, ACC, [], {}, True).ok
