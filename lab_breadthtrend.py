"""Lab run 32 (2026-11-12): breadth TREND (washout deepening vs easing) and SPY bounce-day conditioners of the LIVE vol60>=1.75% setup.
Web seed: breadth-thrust / capitulation write-ups (unverified; rules are my own). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    B = breadth_series(AS); F = feats(AS)
    ds = sorted(B); di = {d: i for i, d in enumerate(ds)}
    sp = {b["t"][:10]: b["c"] for b in spy}; sd = sorted(sp); si = {d: i for i, d in enumerate(sd)}
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    base = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10]
    live = [t for t in base if (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))]
    def f(t):
        d = t["t"][:10]; i = di.get(d); j = si.get(d)
        if not i or i < 3 or not j or j < 3: return None
        return dict(b0=B[d][0], d1=B[d][0]-B[ds[i-1]][0], d3=B[d][0]-B[ds[i-3]][0],
                    spy1=sp[d]/sp[sd[j-1]]-1, spy3=sp[d]/sp[sd[j-3]]-1)
    row("LIVE ref", live, kw, cut)
    V = [("breadth rising vs yday (easing)", lambda x: x["d1"] > 0), ("breadth falling vs yday (deepening)", lambda x: x["d1"] <= 0),
         ("breadth 3d change > 0", lambda x: x["d3"] > 0), ("breadth 3d change <= 0", lambda x: x["d3"] <= 0),
         ("breadth >= 20%", lambda x: x["b0"] >= .20), ("breadth 10-20%", lambda x: x["b0"] < .20),
         ("SPY up on signal day", lambda x: x["spy1"] > 0), ("SPY down on signal day", lambda x: x["spy1"] <= 0),
         ("SPY 3d < -1%", lambda x: x["spy3"] < -.01), ("SPY 3d >= -1%", lambda x: x["spy3"] >= -.01)]
    print("variants tried:", len(V)+1)
    for n, fn in V:
        S = [t for t in live if (lambda x: x is not None and fn(x))(f(t))]
        row(n, S, kw, cut)
