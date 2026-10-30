import backtest as BT
import patterns as P
from tests.test_patterns import ramp, B, make_flag, flat

ONLY_FLAG = {k: k == "flag" for k in P.LONG_DETECTORS}

def series(after):
    bars = flat(140, 40) + make_flag()
    return bars + after

def test_flag_trade_hits_target():
    flag = make_flag(); fh = flag[-1]["c"]
    after = [B(fh + 0.1, fh + 20, fh, fh + 15, 3000)] + flat(5, fh + 15)
    t = BT.simulate(series(after), ONLY_FLAG, shorts=False, warmup=120)
    flags = [x for x in t if x["pattern"] == "flag"]
    assert flags and flags[0]["reason"] == "target" and flags[0]["R"] > 0

def test_stop_wins_when_both_hit_same_bar():
    flag = make_flag(); fh = flag[-1]["c"]
    after = [B(fh, fh + 30, fh - 30, fh, 3000)] + flat(5, fh)       # נר ענק שנוגע גם בסטופ וגם ביעד
    t = [x for x in BT.simulate(series(after), ONLY_FLAG, shorts=False, warmup=120) if x["pattern"] == "flag"]
    assert t and t[0]["reason"] == "stop" and t[0]["R"] < 0

def test_stats_and_disable():
    tr = [{"pattern": "x", "side": "long", "R": -1.0, "pnl_pct": -2, "held": 3, "reason": "stop", "i": k} for k in range(40)]
    tr += [{"pattern": "y", "side": "long", "R": 1.0, "pnl_pct": 2, "held": 3, "reason": "target", "i": k} for k in range(40)]
    st = BT.stats(tr)
    assert st["x"]["win_rate"] == 0 and st["y"]["avg_R"] == 1.0 and st["ALL"]["n"] == 80
    assert BT.disabled_from(st) == ["x"]
    assert "| x |" in BT.to_markdown(st, ["A"], 3, ["x"])

def test_per_direction_disable_and_short_guard(tmp_path):
    import backtest, bot, json
    from patterns import Signal
    mk = lambda p, side, R: {"pattern": p, "side": side, "R": R, "pnl_pct": R, "held": 5}
    tr = [mk("x", "long", 1.0) for _ in range(20)] + [mk("x", "short", -1.0) for _ in range(20)]
    st = backtest.stats(tr)
    assert backtest.disabled_sides_from(st) == ["x:short"] and "x" not in backtest.disabled_from(st)
