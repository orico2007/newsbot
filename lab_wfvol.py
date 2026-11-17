"""Lab run 36 (2026-11-17): walk-forward re-selection of the vol60 threshold (expanding window; pick threshold on prior years only, apply to next year).
Own idea: an honest out-of-sample test of the vol60>=1.75% live filter, instead of one full-sample pick. Backtest only."""
import datetime
import lab, sweep, challenger, research
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

THR = [0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0]

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    base = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            u = dict(t); u["score"] = -m3(t)
            u["_v"] = challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])) or 0
            base.append(u)
    yrs = sorted({t["t"][:4] for t in base})
    print("years", yrs)
    for th in THR:
        row(f"fixed thr {th}", [t for t in base if t["_v"] >= th], kw, cut)
    for obj in ("pf_pct", "ret_pct"):
        sel = []; chosen = {}
        for y in yrs:
            prior = [t for t in base if t["t"][:4] < y]
            if y == yrs[0] or len(prior) < 60:
                chosen[y] = 0; sel += [t for t in base if t["t"][:4] == y]; continue
            best = None
            for th in THR:
                S = [t for t in prior if t["_v"] >= th]
                if len(S) < 40: continue
                v = lab.portfolio(S, **kw)[obj]
                if best is None or v > best[0]: best = (v, th)
            chosen[y] = best[1]
            sel += [t for t in base if t["t"][:4] == y and t["_v"] >= best[1]]
        print("walk-forward objective", obj, "chosen thresholds by year:", chosen)
        row(f"walk-forward ({obj})", sel, kw, cut)
