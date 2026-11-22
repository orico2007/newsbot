"""Lab run 61 (2026-11-22): WALK-FORWARD audit of the run-58/59 three-tilt size stack. Thresholds are re-fitted each test year
using only trades from earlier years (expanding window), then applied (clip 0.5-1.5) to that year. Own idea. Backtest only."""
import datetime, statistics
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series

def pf(T):
    w = sum(t["pnl_pct"] for t in T if t["pnl_pct"] > 0); l = -sum(t["pnl_pct"] for t in T if t["pnl_pct"] < 0); return w/l if l else 9
def scaled(T, ms):
    return [dict(t, pnl_pct=t["pnl_pct"]*m, **({"R": t["R"]*m} if "R" in t else {})) for t, m in zip(T, ms)]

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); S = lab.load_bars()["SPY"]
    cut = (datetime.date.fromisoformat(S[-1]["t"][:10]) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2; B = breadth_series(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    rk = challenger.disp_rank(); ib = challenger.spy_ibs(); vr = challenger.spy_volratio()
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        d = t["t"][:10]
        if B.get(d, (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(d); v = challenger.vol60(AS[t["sym"]], i) if i else None
            if v is not None and v >= 1.75 and i >= 70:
                live.append(dict(t, x=(rk.get(d), ib.get(d), vr.get(d))))
    live.sort(key=lambda t: t["t"])
    yr = lambda t: int(t["t"][:4])
    GRID = [[.3, .4, .5, .6, .7], [.2, .3, .4, .5], [.9, 1.0, 1.1, 1.2, 1.3]]
    def flag(t, j, thr):
        x = t["x"][j]
        if x is None: return False
        return x < thr if j == 1 else x >= thr
    def mult(t, th):
        m = 1.0
        for j in range(3): m *= 1.25 if flag(t, j, th[j]) else .75
        return min(1.5, max(.5, m))
    def fit(train):
        th = []
        for j in range(3):
            best = max(GRID[j], key=lambda g: pf(scaled(train, [1.25 if flag(t, j, g) else .75 for t in train])))
            th.append(best)
        return th
    FIX = (.5, .3, 1.1)
    print("live trades", len(live), "per year", {y: sum(1 for t in live if yr(t) == y) for y in range(2021, 2027)})
    wf = []; chosen = {}
    for Y in range(2023, 2027):
        tr = [t for t in live if yr(t) < Y]; te = [t for t in live if yr(t) == Y]
        th = fit(tr); chosen[Y] = th
        wf += scaled(te, [mult(t, th) for t in te])
    print("chosen thresholds per test year (disp, ibs, vol):", chosen)
    base = [t for t in live if yr(t) >= 2023]
    fx = scaled(base, [mult(t, FIX) for t in base])
    print("--- test years 2023-2026 only (first 2 years used as the initial fit window)")
    row("LIVE flat 2023-26", base, kw, cut)
    row("walk-forward clip 0.5-1.5", wf, kw, cut)
    row("fixed in-sample thresholds clip 0.5-1.5", fx, kw, cut)
    for y in range(2023, 2027):
        a = [t for t in live if yr(t) == y]
        print(y, "n", len(a), "flat PF %.2f" % pf(a), "wf PF %.2f" % pf([t for t in wf if yr(t) == y]), "fixed PF %.2f" % pf([t for t in fx if yr(t) == y]))
    # also mean-1 normalised walk-forward (leverage check)
    ms = [mult(t, chosen[yr(t)]) for t in base]; mean = statistics.mean(ms)
    row("walk-forward normalised mean 1", scaled(base, [m/mean for m in ms]), kw, cut); print("mean mult", round(mean, 3))
    print("variants: 14 grid cells x 4 folds (fit), 1 reported walk-forward path")
