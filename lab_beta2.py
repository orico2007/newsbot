"""Lab run 8b (2026-11-09): follow-up of lab_beta.py - absolute volatility thresholds, vol as priority rank, high-vol + others as filler. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_beta as LB
import math

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); bars = lab.load_bars(); spy = bars["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    from lab_breadth import breadth_series
    from lab_sector import feats
    champ = PT.gen(AS, ctx, challenger.ruleset()); B = breadth_series(AS); F = feats(AS)
    m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    def vol60(t):
        A = AS[t["sym"]]; i = IX[t["sym"]].get(t["t"][:10])
        if i is None or i < 61: return None
        r = [A["c"][j]/A["c"][j-1]-1 for j in range(i-59, i+1)]; m = sum(r)/60
        return math.sqrt(sum((x-m)**2 for x in r)/59)*100
    live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            u = dict(t); u["score"] = -m3(t); u["v"] = vol60(t); live.append(u)
    live = [t for t in live if t["v"] is not None]
    row("LIVE ref", live, kw, cut)
    V = []
    for th in (1.5, 1.75, 2.0, 2.5, 3.0):
        V.append((f"vol60 >= {th}", [t for t in live if t["v"] >= th]))
    V.append(("rank by vol60 (all signals)", [dict(t, score=t["v"]) for t in live]))
    V.append(("vol>=2.0 first, others as filler", [dict(t, score=t["score"] + (1000 if t["v"] >= 2.0 else 0)) for t in live]))
    V.append(("vol>=2.0 filter, rank by vol", [dict(t, score=t["v"]) for t in live if t["v"] >= 2.0]))
    print("variants tried:", len(V) + 9, "(incl. 9 in lab_beta.py)")
    for n, S in V:
        row(n, S, kw, cut)
