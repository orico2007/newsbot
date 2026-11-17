"""Lab run 37 (2026-11-17): risk-appetite leadership (IWM small-cap and QQQ growth vs SPY) as a conditioner of the LIVE vol60>=1.75% setup. Own idea. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth

def idx(bars):
    return {b["t"][:10]: i for i, b in enumerate(bars)}, [b["c"] for b in bars]

SYM = "IWM"
def rel(B, d, k):
    """mean(XLP,XLU) k-day return minus SPY k-day return at date d (None if missing)."""
    out = []
    for s in (SYM, "SPY"):
        ix, c = B[s]; i = ix.get(d)
        if i is None or i < k: return None
        out.append(c[i] / c[i-k] - 1)
    return out[0] - out[1]

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); bars = lab.load_bars(); last = bars["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    B = {s: idx(bars[s]) for s in ("IWM", "QQQ", "SPY")}
    BR = lab_breadth.breadth_series(AS)
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [t for t in T0 if BR.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    row("LIVE ref", live, kw, cut)
    def f(sym, k, op):
        def g(t):
            global SYM
            SYM = sym
            v = rel(B, t["t"][:10], k)
            return v is not None and (v > 0 if op == ">" else v <= 0)
        return g
    V = [(f"{s} {w} SPY {k}d", f(s, k, o)) for s in ("IWM", "QQQ") for k in (5, 20) for o, w in ((">", "leads"), ("<=", "lags"))]
    print("variants tried:", len(V))
    for n, g in V:
        row(n, [t for t in live if g(t)], kw, cut)
