"""Lab run 53: robustness / walk-forward sensitivity of the run-52b contraction-breakout sleeve (threshold, breakout length, volume multiple, hold). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
import lab_breadth, lab_sector
from lab_52wh import row
from lab_vcb import signals, trades

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; lastd = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(lastd) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = challenger.DEF_PORT
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    B = lab_breadth.breadth_series(AS); F = lab_sector.feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    print("data through", lastd); row("LIVE vol175", live, kw, cut)
    V = [("base c0.8 v1.5 n20 h10", dict(contr=0.8, volx=1.5), 10),
         ("c0.6 v1.5 n20 h10", dict(contr=0.6, volx=1.5), 10),
         ("c0.7 v1.5 n20 h10", dict(contr=0.7, volx=1.5), 10),
         ("c0.9 v1.5 n20 h10", dict(contr=0.9, volx=1.5), 10),
         ("c0.8 v1.25 n20 h10", dict(contr=0.8, volx=1.25), 10),
         ("c0.8 v2.0 n20 h10", dict(contr=0.8, volx=2.0), 10),
         ("c0.8 v1.5 n55 h10", dict(contr=0.8, volx=1.5, n=55), 10),
         ("c0.8 v1.5 n10 h10", dict(contr=0.8, volx=1.5, n=10), 10),
         ("c0.8 v1.5 n20 h5", dict(contr=0.8, volx=1.5), 5),
         ("c0.8 v1.5 n20 h15", dict(contr=0.8, volx=1.5), 15)]
    print("variants tried:", len(V))
    for nme, k, hold in V:
        T = trades(AS, signals(AS, ctx, **k), hold)
        row(nme, T, kw, cut); row("   + live combined", live + T, kw, cut)
