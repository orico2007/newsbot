"""Lab run 34 (2026-11-17): priority ranking of same-day signals by vol60 (high/low first) vs live weakest-peer rank, on the vol60>=1.75% LIVE setup. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
import lab_breadth, lab_sector
from lab_52wh import row

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = challenger.DEF_PORT
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    B = lab_breadth.breadth_series(AS); F = lab_sector.feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    v60 = lambda t: challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10]))
    base = []
    for t in T0:
        v = v60(t)
        if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and v is not None and v >= 1.75:
            u = dict(t); u["_v"] = v; u["score"] = -F[(t["sym"], t["t"])]["m3"] if (t["sym"], t["t"]) in F else 0; base.append(u)
    def rk(f): return [dict(t, score=f(t)) for t in base]
    row("LIVE (weakest-peer rank)", base, kw, cut)
    V = [("rank vol60 high first", rk(lambda t: t["_v"])), ("rank vol60 low first", rk(lambda t: -t["_v"]))]
    print("variants tried:", len(V))
    for n, S in V:
        row(n, S, kw, cut)
        for lb, f in (("early 2021-23", lambda t: t["t"][:4] <= "2023"), ("late 2024-26", lambda t: t["t"][:4] >= "2024")):
            row("  " + lb, [t for t in S if f(t)], kw, cut)
