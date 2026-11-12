"""Lab run 38 (2026-11-12): same-symbol re-entry memory re-tested on the NEW live setup (vol60>=1.75%, breadth>=10%, peer rank). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth
from lab_reentry import filt

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    B = lab_breadth.breadth_series(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    live = [t for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    row("LIVE ref", live, kw, cut)
    V = [("skip if prev trade lost <=20d", "skip_loss", 20), ("skip if prev trade lost <=60d", "skip_loss", 60),
         ("skip any re-entry <=20d", "skip_any", 20)]
    print("variants tried:", len(V))
    for name, mode, N in V:
        T = filt(live, mode, N); print("  signals", len(T), "of", len(live)); row(name, T, kw, cut)
