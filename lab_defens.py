"""Lab run 35 (2026-11-12): defensive-sector leadership (XLP/XLU vs SPY) as a cross-asset risk-off conditioner of the LIVE vol60>=1.75% setup. Own idea. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth

def idx(bars):
    return {b["t"][:10]: i for i, b in enumerate(bars)}, [b["c"] for b in bars]

def rel(B, d, k):
    """mean(XLP,XLU) k-day return minus SPY k-day return at date d (None if missing)."""
    out = []
    for s in ("XLP", "XLU", "SPY"):
        ix, c = B[s]; i = ix.get(d)
        if i is None or i < k: return None
        out.append(c[i] / c[i-k] - 1)
    return (out[0] + out[1]) / 2 - out[2]

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); bars = lab.load_bars(); last = bars["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    B = {s: idx(bars[s]) for s in ("XLP", "XLU", "SPY")}
    BR = lab_breadth.breadth_series(AS)
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [t for t in T0 if BR.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    row("LIVE ref", live, kw, cut)
    def f(k, op):
        def g(t):
            v = rel(B, t["t"][:10], k)
            return v is not None and (v > 0 if op == ">" else v <= 0)
        return g
    V = [("defensives lead SPY 5d", f(5, ">")), ("defensives lag SPY 5d", f(5, "<=")),
         ("defensives lead SPY 20d", f(20, ">")), ("defensives lag SPY 20d", f(20, "<="))]
    print("variants tried:", len(V))
    for n, g in V:
        S = [t for t in live if g(t)]
        row(n, S, kw, cut)
