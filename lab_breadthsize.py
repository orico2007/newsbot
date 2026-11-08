"""Lab run 29 (2026-11-08): breadth-washout size tier on the LIVE setup (follow-up of runs 13/26). Post-hoc scaling of taken live trades; backtest only."""
import lab, sweep, challenger
import portfolio_test as PT
from lab_breadth import breadth_series
from lab_sector import feats
from lab_fearsize import curve

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); B = breadth_series(AS); F = feats(AS)
    m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            u = dict(t); u["score"] = -m3(t); live.append(u)
    taken = lab.portfolio(live, **kw)["trades"]
    for t in taken: t["b"] = B.get(t["t"][:10], (0, 0))[0]
    import numpy as np
    print("taken", len(taken), "breadth quantiles", np.percentile([t["b"] for t in taken], [10,25,50,75,90]).round(3))
    V = [("flat", lambda t: 1), ("1.5x if breadth>=20%", lambda t: 1.5 if t["b"] >= .20 else 1),
         ("1.5x if breadth>=30%", lambda t: 1.5 if t["b"] >= .30 else 1),
         ("1.5x >=20%, 0.75x <15%", lambda t: 1.5 if t["b"] >= .20 else (.75 if t["b"] < .15 else 1)),
         ("0.5x if breadth 10-15%", lambda t: .5 if t["b"] < .15 else 1)]
    print("variants tried:", len(V))
    for n, m in V: print(f"{n:26}", curve(taken, m))
    for lo, hi in [("2021","2023"),("2024","2026")]:
        s = [t for t in taken if lo <= t["t"][:4] <= hi]
        print(lo, hi, "n", len(s), {n: curve(s, m)[:3] for n, m in V})
    for y in ("2021","2022","2023","2024","2025","2026"):
        s = [t for t in taken if t["t"][:4] == y]
        print(y, len(s), "hi-breadth n", sum(t["b"]>=.2 for t in s), {n: curve(s, m)[:3] for n, m in V[:2]})
