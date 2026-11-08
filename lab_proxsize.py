"""Lab run 26 (2026-11-08): size-up tier for LIVE entries far below their 252d high (follow-up of lab_prox). Post-hoc scaling of taken live trades; backtest only."""
import lab, sweep, challenger
import portfolio_test as PT
from lab_breadth import breadth_series
from lab_sector import feats
from lab_prox import prox
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
    for t in taken: t["px"] = prox(AS, t)
    far = lambda t: t["px"] is not None and t["px"] < .90
    known = sum(t["px"] is not None for t in taken); print("taken", len(taken), "with prox", known, "far", sum(far(t) for t in taken))
    V = [("flat", lambda t: 1), ("1.5x if >10% below high", lambda t: 1.5 if far(t) else 1),
         ("1.5x far, 0.75x else", lambda t: 1.5 if far(t) else .75), ("1.3x far", lambda t: 1.3 if far(t) else 1)]
    for n, m in V: print(f"{n:28}", curve(taken, m))
    for lo, hi in [("2021","2023"),("2024","2026")]:
        s = [t for t in taken if lo <= t["t"][:4] <= hi]
        print(lo, hi, "n", len(s), "far", sum(far(t) for t in s), {n: curve(s, m)[:3] for n, m in V[:3]})
