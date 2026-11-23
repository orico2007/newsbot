"""Lab run 70 (2026-11-23): steady-uptrend size tilt (60d up-day share > 0.55, rs60 vs SPY > 0) as 4th flag on the run-59 clipped stack; follow-up of run 68. Own idea. Backtest only."""
import datetime, statistics, random
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); S = lab.load_bars()["SPY"]
    cut = (datetime.date.fromisoformat(S[-1]["t"][:10]) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2; B = breadth_series(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    SI = {b["t"][:10]: i for i, b in enumerate(S)}; sc = [b["c"] for b in S]
    rk = challenger.disp_rank(); ib = challenger.spy_ibs(); vr = challenger.spy_volratio()
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        d = t["t"][:10]
        if B.get(d, (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(d); v = challenger.vol60(AS[t["sym"]], i) if i else None; j = SI.get(d)
            if v is not None and v >= 1.75 and i >= 130 and j and j >= 130:
                c = AS[t["sym"]]["c"]
                up = sum(1 for k in range(i-59, i+1) if c[k] > c[k-1]) / 60
                rs = (c[i]/c[i-60]-1) - (sc[j]/sc[j-60]-1)
                a = rk.get(d); b = ib.get(d); e = vr.get(d)
                fl = (a is not None and a >= .5, b is not None and b < .3, e is not None and e >= 1.1, up > .55, rs > 0)
                live.append(dict(t, fl=fl))
    def mk(fn, L=None):
        L = L or live; ms = [fn(t) for t in L]; mean = statistics.mean(ms); out = []
        for t, m in zip(L, ms):
            u = dict(t); u["pnl_pct"] = t["pnl_pct"]*m/mean
            if "R" in u: u["R"] = t["R"]*m/mean
            out.append(u)
        return out
    f = lambda t, j: 1.25 if t["fl"][j] else .75
    clip = lambda idx: (lambda t: min(1.5, max(.5, __import__("math").prod(f(t, j) for j in idx))))
    V = [("ref run59 stack (3 flags)", clip((0,1,2))), ("up-share tilt alone", clip((3,))), ("rs60 tilt alone", clip((4,))),
         ("3 flags + up-share", clip((0,1,2,3))), ("3 flags + rs60", clip((0,1,2,4))), ("3 flags + up + rs60", clip((0,1,2,3,4)))]
    row("LIVE ref (before zreg)", live, kw, cut)
    for nm, fn in V:
        row(nm + " (norm mean 1)", mk(fn), kw, cut)
    for sp, g in (("<=2023", lambda t: t["t"][:4] <= "2023"), (">=2024", lambda t: t["t"][:4] >= "2024")):
        L = [t for t in live if g(t)]
        row("live "+sp, L, kw, cut)
        for nm, fn in (V[0], V[1], V[3]):
            row(nm[:22]+" "+sp, mk(fn, L), kw, cut)
    def pf(T):
        w = sum(t["pnl_pct"] for t in T if t["pnl_pct"] > 0); l = -sum(t["pnl_pct"] for t in T if t["pnl_pct"] < 0); return w/l if l else 9
    fn = V[1][1]; ms = [fn(t) for t in live]; mean = statistics.mean(ms)
    real = pf([dict(t, pnl_pct=t["pnl_pct"]*m/mean) for t, m in zip(live, ms)])
    random.seed(1); ks = []
    for _ in range(2000):
        sh = ms[:]; random.shuffle(sh); ks.append(pf([dict(t, pnl_pct=t["pnl_pct"]*m/mean) for t, m in zip(live, sh)]))
    ks.sort(); print("placebo up-share tilt PF: median %.2f p95 %.2f p99 %.2f ; real %.2f ; live %.2f" % (ks[1000], ks[1900], ks[1980], real, pf(live)))
    print("variants tried: 6 (+3x2 split) + placebo")
