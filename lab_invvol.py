"""Lab run 54 (2026-11-14): inverse-volatility (equal-risk) trade sizing on the LIVE setup (own idea; lab_invvol.py). Backtest only.
Size multiplier m = clip(target / vol60, lo, hi) where vol60 = 60d stdev of daily returns (%); PF is size-weighted."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
import lab_breadth, lab_sector
from lab_52wh import row

def sized(T, fn):
    out = []
    for t, v in T:
        m = fn(v); u = dict(t); u["pnl_pct"] = t["pnl_pct"] * m
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
    V60 = lambda t: challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10]))
    live = [(dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t, V60(t))
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and (V60(t) or 0) >= 1.75]
    vs = sorted(v for _, v in live); print("n", len(live), "vol60 median", vs[len(vs)//2], "p25", vs[len(vs)//4], "p75", vs[3*len(vs)//4])
    row("LIVE ref", [t for t, _ in live], kw, cut)
    V = [("inverse-vol target 2.5 clip .5-1.5", lambda v: min(1.5, max(.5, 2.5 / v))),
         ("inverse-vol target 2.5 clip .75-1.25", lambda v: min(1.25, max(.75, 2.5 / v))),
         ("inverse-vol target 3.0 clip .5-1.5", lambda v: min(1.5, max(.5, 3.0 / v))),
         ("DIRECT vol tilt (v/2.5) clip .5-1.5 (control)", lambda v: min(1.5, max(.5, v / 2.5))),
         ("DIRECT vol tilt (v/2.5) clip .75-1.25 (control)", lambda v: min(1.25, max(.75, v / 2.5)))]
    print("variants tried:", len(V))
    for n, fn in V: row(n, sized(live, fn), kw, cut)
