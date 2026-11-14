"""Lab run 53 (2026-11-14): average-correlation (correlated-stress) regime as filter / size tilt on the LIVE setup.
Web-seeded (unverified title only): https://quantpedia.com/short-term-correlated-stress-reversal-trading/ . Rules my own.
Corr proxy: for each day, mean over universe stocks of 20d correlation of daily returns with the equal-weight universe return;
percentile vs prior 250 days (no look-ahead). Backtest only; size tilt emulated by scaling pnl_pct."""
import datetime
import numpy as np
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    B = lab_breadth.breadth_series(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    raw = lab.load_bars()
    dates = sorted({b["t"][:10] for s in AS for b in raw[s]})
    di = {d: i for i, d in enumerate(dates)}
    syms = [s for s in AS if s in raw]
    M = np.full((len(dates), len(syms)), np.nan)
    for j, s in enumerate(syms):
        b = raw[s]
        for i in range(1, len(b)):
            M[di[b[i]["t"][:10]], j] = b[i]["c"] / b[i-1]["c"] - 1
    ew = np.nanmean(M, axis=1)
    C = {}
    for i in range(20, len(dates)):
        W = M[i-19:i+1]; e = ew[i-19:i+1]
        ok = ~np.isnan(W).any(axis=0)
        if ok.sum() < 30: continue
        X = W[:, ok]; Xc = X - X.mean(0); ec = e - e.mean()
        cors = (Xc * ec[:, None]).sum(0) / np.sqrt((Xc**2).sum(0) * (ec**2).sum() + 1e-18)
        C[dates[i]] = cors.mean()
    ds = sorted(C); rank = {}
    for k, d in enumerate(ds):
        w = [C[x] for x in ds[max(0, k-250):k]]
        rank[d] = sum(1 for x in w if x < C[d]) / len(w) if len(w) >= 60 else None
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    base = [t for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    for t in base: t["_r"] = rank.get(t["t"][:10])
    def tilt(hi, lo, th=.5):
        out = []
        for t in base:
            u = dict(t); r = t["_r"]; u["pnl_pct"] = t["pnl_pct"] * (hi if (r is not None and r >= th) else lo); out.append(u)
        return out
    print("variants tried: 7")
    print("rank coverage", sum(t["_r"] is not None for t in base), "/", len(base))
    row("LIVE ref", base, kw, cut)
    for th in (.5, .8):
        row(f"corr pct >= {th}", [t for t in base if t["_r"] is not None and t["_r"] >= th], kw, cut)
        row(f"corr pct < {th}", [t for t in base if t["_r"] is not None and t["_r"] < th], kw, cut)
    row("tilt 1.25x if corr>=.5 else 0.75x", tilt(1.25, .75), kw, cut)
    row("tilt 1.25x if corr<.5 else 0.75x (inverse)", tilt(.75, 1.25), kw, cut)
    # overlap with dispersion
