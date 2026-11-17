"""Lab run 38 (2026-11-17): Quantitativo-style own-history oversold percentile (QPI-like) and SPY realized-vol regime (VIX-SMA proxy) as conditioners of the LIVE vol60>=1.75% setup. Web-seeded; backtest only."""
import datetime, statistics
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth

def pct_rank(c, i, k=3, win=252):
    """percentile (0-100) of the k-day return at i among the stock's own k-day returns over the prior win days."""
    if i < win + k: return None
    cur = c[i] / c[i-k] - 1
    h = [c[j] / c[j-k] - 1 for j in range(i - win, i)]
    return 100.0 * sum(1 for x in h if x < cur) / len(h)

def spy_vol_regime(spy_c, dates, n=10, sm=15, mult=1.15):
    """bear flag per date: SPY n-day realized vol > mult * its sm-day SMA (proxy for the VIX > 1.15*SMA15 rule)."""
    rets = [0.0] + [spy_c[i]/spy_c[i-1]-1 for i in range(1, len(spy_c))]
    rv = [None]*len(spy_c)
    for i in range(n, len(spy_c)): rv[i] = statistics.pstdev(rets[i-n+1:i+1])
    out = {}
    for i in range(n+sm, len(spy_c)):
        out[dates[i]] = rv[i] > mult * (sum(rv[i-sm+1:i+1]) / sm)
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); bars = lab.load_bars(); last = bars["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    BR = lab_breadth.breadth_series(AS)
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [t for t in T0 if BR.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    row("LIVE ref", live, kw, cut)
    sp = bars["SPY"]; reg = spy_vol_regime([b["c"] for b in sp], [b["t"][:10] for b in sp])
    def pr(t, k):
        s = t["sym"]; i = IX[s].get(t["t"][:10])
        return None if i is None else pct_rank(AS[s]["c"], i, k)
    V = []
    for k in (3, 5):
        for th in (5, 10, 15):
            V.append((f"own-history {k}d-return pct <= {th}", lambda t, k=k, th=th: (lambda p: p is not None and p <= th)(pr(t, k))))
    V.append(("SPY 10d rvol NOT > 1.15x its SMA15", lambda t: not reg.get(t["t"][:10], False)))
    V.append(("SPY 10d rvol > 1.15x its SMA15 only", lambda t: reg.get(t["t"][:10], False)))
    print("variants tried:", len(V))
    for n, g in V: row(n, [t for t in live if g(t)], kw, cut)
    # follow-up size tilt (one extra variant family; total variants this run = 8 + 2)
    def tilt(g, hi=1.25, lo=0.75):
        out = []
        for t in live:
            m = hi if g(t) else lo; u = dict(t); u["pnl_pct"] = t["pnl_pct"] * m
            if "R" in u: u["R"] = t["R"] * m
            out.append(u)
        return out
    print("-- size tilts (PF size-weighted)")
    row("tilt 1.25/0.75 if own 5d pct<=10", tilt(lambda t: (lambda p: p is not None and p <= 10)(pr(t, 5))), kw, cut)
    row("tilt 1.25/0.75 if own 3d pct<=10", tilt(lambda t: (lambda p: p is not None and p <= 10)(pr(t, 3))), kw, cut)
