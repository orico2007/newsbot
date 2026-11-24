"""Lab run 81 (2026-11-24): rank same-day entries by regression-z depth (deepest first / shallowest first) on live vol60+zreg setup. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_zscore import zreg

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(spy) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2; B = breadth_series(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(t["t"][:10]); v = challenger.vol60(AS[t["sym"]], i)
            if v is not None and v >= 1.75 and i is not None and i >= 65:
                z = zreg(AS[t["sym"]], i, 20)
                if z < -1.5: u = dict(t); u["z"] = z; live.append(u)
    row("LIVE ref", live, kw, cut)
    for n, f in [("deepest z first", 1), ("shallowest z first", -1)]:
        T = []
        for t in live: u = dict(t); u["score"] = f * t["z"] * -1 * -1; T.append(u)
        row(n, T, kw, cut)
    print("variants tried: 2")
