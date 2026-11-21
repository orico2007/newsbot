"""Lab run 59 (2026-11-21): CAPPED stack (clip multiplier) of the three tilts; follow-up to run 58. Original: stack/vote of the three market-state size tilts (dispersion pct>=.5, SPY IBS<.3, SPY vol ratio>=1.1) on the live vol60>=1.75% setup.
Web seed: https://alphaarchitect.com/how-volatility-and-turnover-affect-return-reversals/ (search hit only, not fetched). Backtest only."""
import datetime, statistics
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); S = lab.load_bars()["SPY"]
    cut = (datetime.date.fromisoformat(S[-1]["t"][:10]) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2; B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    rk = challenger.disp_rank(); ib = challenger.spy_ibs(); vr = challenger.spy_volratio()
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        d = t["t"][:10]
        if B.get(d, (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(d); v = challenger.vol60(AS[t["sym"]], i) if i else None
            if v is not None and v >= 1.75 and i >= 70:
                a = rk.get(d); b = ib.get(d); c = vr.get(d)
                fl = (a is not None and a >= .5, b is not None and b < .3, c is not None and c >= 1.1)
                live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0), fl=fl, k=sum(fl)))
    import random
    def mk(fn, norm=False):
        ms = [fn(t) for t in live]; mean = statistics.mean(ms) if norm else 1.0
        out = []
        for t, m in zip(live, ms):
            m = m / mean; u = dict(t); u["pnl_pct"] = t["pnl_pct"]*m
            if "R" in u: u["R"] = t["R"]*m
            out.append(u)
        return out, statistics.mean(ms)
    f = lambda t, j: 1.25 if t["fl"][j] else .75
    st = lambda t: f(t,0)*f(t,1)*f(t,2)
    cl = lambda lo, hi: (lambda t: min(hi, max(lo, st(t))))
    V = [("stack clip 0.5-1.5", cl(.5,1.5)), ("stack clip 0.75-1.25", cl(.75,1.25)), ("stack clip 0.6-1.6", cl(.6,1.6)),
         ("rank-free 3-level 0.75/1/1.5 by k (0,1-2,3)", lambda t: .75 if t["k"]==0 else (1.5 if t["k"]==3 else 1.0))]
    row("LIVE ref (before zreg)", live, kw, cut)
    for nm, fn in V:
        T, mean = mk(fn); print(f"[{nm}] mean multiplier {mean:.2f}")
        row(nm, T, kw, cut); T, _ = mk(fn, True); row(nm + " (norm mean 1)", T, kw, cut)
    for sp, g in (("<=2023", lambda t: t["t"][:4] <= "2023"), (">=2024", lambda t: t["t"][:4] >= "2024")):
        L = [t for t in live if g(t)]; fn = V[0][1]; ms = [fn(t) for t in L]; mean = statistics.mean(ms); T = []
        for t, m in zip(L, ms):
            u = dict(t); u["pnl_pct"] = t["pnl_pct"]*m/mean
            if "R" in u: u["R"] = t["R"]*m/mean
            T.append(u)
        row("clip0.5-1.5 norm "+sp, T, kw, cut); row("live "+sp, L, kw, cut)
    # placebo: shuffle the k labels across trades, compute clip0.5-1.5 normalised total return & PF
    def pf(T):
        w = sum(t["pnl_pct"] for t in T if t["pnl_pct"] > 0); l = -sum(t["pnl_pct"] for t in T if t["pnl_pct"] < 0); return w/l if l else 9
    fn = V[0][1]; ms = [fn(t) for t in live]; mean = statistics.mean(ms)
    real = pf([dict(t, pnl_pct=t["pnl_pct"]*m/mean) for t, m in zip(live, ms)])
    random.seed(1); ks = []
    for _ in range(2000):
        sh = ms[:]; random.shuffle(sh); ks.append(pf([dict(t, pnl_pct=t["pnl_pct"]*m/mean) for t, m in zip(live, sh)]))
    ks.sort(); print("placebo PF (shuffled multipliers): median %.2f p95 %.2f p99 %.2f ; real %.2f ; live PF %.2f" % (ks[1000], ks[1900], ks[1980], real, pf(live)))
    print("variants tried: 4 (x2 normalisation) + placebo")
