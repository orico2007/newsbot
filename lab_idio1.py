"""Lab run 47 (2026-11-20): 1-day idiosyncratic drop (stock return minus beta*SPY return on the signal day) and stock-down/SPY-up divergence
as conditioners of the vol60>=1.75% LIVE setup (own idea; run 30 tested 5d residual only, run 32 SPY direction only). Backtest only."""
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
    sc = {b["t"][:10]: b["c"] for b in spy}; sd = sorted(sc); si = {d: i for i, d in enumerate(sd)}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    def feat(t):
        A = AS[t["sym"]]; d = t["t"][:10]; i = IX[t["sym"]][d]
        if i < 62 or d not in si: return None
        rs, rm = [], []
        for k in range(i-59, i+1):
            dk = A["t"][k]; dp = A["t"][k-1]
            if dk in si and dp in si and si[dk] == si[dp] + 1:
                rs.append(A["c"][k]/A["c"][k-1]-1); rm.append(sc[dk]/sc[dp]-1)
        if len(rs) < 40: return None
        mm = sum(rm)/len(rm); ms = sum(rs)/len(rs)
        var = sum((x-mm)**2 for x in rm); beta = sum((a-ms)*(b-mm) for a, b in zip(rs, rm))/var if var else 1
        r1 = (A["c"][i]/A["c"][i-1]-1)*100; m1 = (sc[d]/sc[sd[si[d]-1]]-1)*100
        return dict(r1=r1, m1=m1, idio=r1-beta*m1)
    FT = {id(t): feat(t) for t in live}
    ok = [f["idio"] for f in FT.values() if f]; ok.sort(); print("idio1 quartiles", [round(ok[int(len(ok)*q)],2) for q in (.25,.5,.75)], "n feat", len(ok), "of", len(live))
    g = lambda t: FT[id(t)]
    V = [("idio1 < -2%", lambda t: g(t) and g(t)["idio"] < -2), ("idio1 < -4%", lambda t: g(t) and g(t)["idio"] < -4),
         ("idio1 >= -2% (market-driven)", lambda t: g(t) and g(t)["idio"] >= -2), ("idio1 >= -1%", lambda t: g(t) and g(t)["idio"] >= -1),
         ("stock<0 & SPY>0 (divergence)", lambda t: g(t) and g(t)["r1"] < 0 and g(t)["m1"] > 0),
         ("SPY 1d < -0.5% (market-led)", lambda t: g(t) and g(t)["m1"] < -0.5),
         ("stock 1d < -3%", lambda t: g(t) and g(t)["r1"] < -3), ("stock 1d >= -1%", lambda t: g(t) and g(t)["r1"] >= -1)]
    print("variants tried:", len(V))
    row("LIVE ref", live, kw, cut)
    for n, f in V: row(n, [t for t in live if f(t)], kw, cut)
