"""Lab run 31: stacking the run30 (SPY IBS) and run52 (dispersion) size tilts on the vol60>=1.75% LIVE setup (own idea; follow-up of run 30). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
import lab_breadth, lab_sector
from lab_52wh import row

def scale(T, f):
    out = []
    for t in T:
        m = f(t); u = dict(t); u["pnl_pct"] = t["pnl_pct"] * m
        if "R" in u: u["R"] = t["R"] * m
        out.append(u)
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = challenger.DEF_PORT
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    B = lab_breadth.breadth_series(AS); F = lab_sector.feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    rk = challenger.disp_rank(); ib = challenger.spy_ibs()
    D = lambda t: (rk.get(t["t"][:10]) or 0) >= .5
    I = lambda t: (ib.get(t["t"][:10]) if ib.get(t["t"][:10]) is not None else 9) < .3
    print("data through", last, "| signals", len(live))
    row("LIVE vol175", live, kw, cut)
    row("disp tilt 1.25/.75", scale(live, lambda t: 1.25 if D(t) else .75), kw, cut)
    row("IBS tilt 1.25/.75", scale(live, lambda t: 1.25 if I(t) else .75), kw, cut)
    row("STACK mult (1.25/.75)^2", scale(live, lambda t: (1.25 if D(t) else .75) * (1.25 if I(t) else .75)), kw, cut)
    row("STACK additive 1+.25*(d+i)", scale(live, lambda t: 1 + .25 * ((1 if D(t) else -1) + (1 if I(t) else -1))), kw, cut)
    row("STACK mult 1.15/.85 each", scale(live, lambda t: (1.15 if D(t) else .85) * (1.15 if I(t) else .85)), kw, cut)
    print("--- 2x2 cells (unscaled)")
    for a in (True, False):
        for b in (True, False):
            row(f"disp>=.5={a} ibs<.3={b}", [t for t in live if D(t) == a and I(t) == b], kw, cut)
    print("overlap corr days:", sum(1 for t in live if D(t) and I(t)), "both of", len(live))
