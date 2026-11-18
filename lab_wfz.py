"""Lab run 45 (2026-11-18): walk-forward re-selection of the regression-residual z filter (window, threshold) on the vol60>=1.75% LIVE setup.
Expanding window: pick (W,th) on prior years only, apply to next year. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats
from lab_zscore import zreg
GRID = [(W, th) for W in (10, 20, 30, 60) for th in (-1.0, -1.25, -1.5, -1.75)]
if __name__ == "__main__":
    AS, ctx = sweep.load_all(); last = lab.load_bars()["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    PT.gate_ok = challenger.gate2
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            v = challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10]))
            if v is not None and v >= 1.75:
                u = dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0))
                i = IX[t["sym"]][t["t"][:10]]
                for W in (10, 20, 30, 60): u["z%d" % W] = zreg(AS[t["sym"]], i, W)
                live.append(u)
    yrs = sorted({t["t"][:4] for t in live}); print("years", yrs)
    row("LIVE ref", live, kw, cut)
    row("fixed zreg20<-1.5", [t for t in live if t["z20"] < -1.5], kw, cut)
    for obj in ("pf_pct", "ret_pct"):
        sel = []; chosen = {}
        for y in yrs:
            prior = [t for t in live if t["t"][:4] < y]
            cur = [t for t in live if t["t"][:4] == y]
            if y == yrs[0] or len(prior) < 60:
                chosen[y] = None; sel += cur; continue
            best = None
            for W, th in GRID:
                S = [t for t in prior if t["z%d" % W] < th]
                if len(S) < 40: continue
                v = lab.portfolio(S, **kw)[obj]
                if best is None or v > best[0]: best = (v, (W, th))
            chosen[y] = best[1]; W, th = best[1]
            sel += [t for t in cur if t["z%d" % W] < th]
        print("objective", obj, chosen)
        row("walk-forward " + obj, sel, kw, cut)
    # per-year: filter vs live
    for y in yrs:
        a = [t for t in live if t["t"][:4] == y]; b = [t for t in a if t["z20"] < -1.5]
        print(y, "live n", len(a), "z20 n", len(b))
