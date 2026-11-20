"""Lab run 44 (2026-11-20): nominal share-price level and distance-above-252d-low as conditioners of the vol60>=1.75% LIVE setup (own idea, no web source;
price-level/low-price effects are a classic anomaly theme but no earlier run tested price tiers). Backtest only."""
import datetime
import lab, sweep, challenger
import lab_breadth, lab_sector
from lab_52wh import row
import portfolio_test as PT

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    T0 = PT.gen(AS, ctx, challenger.ruleset()); B = lab_breadth.breadth_series(AS); F = lab_sector.feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    def px(t): return AS[t["sym"]]["c"][IX[t["sym"]][t["t"][:10]]]
    def lowd(t):
        i = IX[t["sym"]][t["t"][:10]]; c = AS[t["sym"]]["c"]
        if i < 252: return None
        return (c[i] / min(c[i-252:i+1]) - 1) * 100
    ps = sorted(px(t) for t in live); print("price quartiles", [round(ps[int(len(ps)*q)],1) for q in (.25,.5,.75)])
    V = [("price >= 20", lambda t: px(t) >= 20), ("price >= 50", lambda t: px(t) >= 50), ("price >= 100", lambda t: px(t) >= 100),
         ("price < 150", lambda t: px(t) < 150), ("price < 300", lambda t: px(t) < 300),
         ("52w-low dist >= 50%", lambda t: (lowd(t) or 0) >= 50), ("52w-low dist >= 100%", lambda t: (lowd(t) or 0) >= 100),
         ("52w-low dist < 100%", lambda t: lowd(t) is not None and lowd(t) < 100)]
    print("variants tried:", len(V))
    row("LIVE ref", live, kw, cut)
    for n, f in V: row(n, [t for t in live if f(t)], kw, cut)
