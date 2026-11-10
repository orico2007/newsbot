"""Lab run 20 (2026-11-10): SPY-dip sizing re-tested on the NEW live setup (breadth>=10%, weakest-peer rank, vol60>=1.75%).
Follow-up of run 19, which was only run on the previous champion. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
import lab_breadth, lab_sector
from lab_52wh import row
from lab_dipsize import scaled
from lab_fear import spy_feats

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
    S = spy_feats()
    row("LIVE (vol175)", live, kw, cut)
    V = [("1.5x if SPY3d<-1% else 1x", lambda f: 1.5 if f[1] < -1 else 1.0),
         ("1.5x if dip else 0.5x", lambda f: 1.5 if f[1] < -1 else 0.5),
         ("1.25x if dip else 0.75x", lambda f: 1.25 if f[1] < -1 else 0.75),
         ("0.5x if SPY3d>0 else 1x (control: shrink calm days)", lambda f: 0.5 if f[1] > 0 else 1.0)]
    print("variants tried:", len(V))
    for n, fn in V: row(n, scaled(live, S, fn), kw, cut)
