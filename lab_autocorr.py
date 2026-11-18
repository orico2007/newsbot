"""Lab run 43 (2026-11-18): stock-specific short-term autocorrelation / variance-ratio (mean-reverting character) as conditioner of the vol60>=1.75% LIVE setup. Web-seeded hypothesis; backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth

def ac1(c, i, n):
    if i < n + 1: return None
    r = [c[j]/c[j-1]-1 for j in range(i-n+1, i+1)]
    m = sum(r)/n; num = sum((r[k]-m)*(r[k-1]-m) for k in range(1, n)); den = sum((x-m)**2 for x in r)
    return num/den if den else None

def vr(c, i, n, q=5):
    if i < n + q: return None
    r1 = [c[j]/c[j-1]-1 for j in range(i-n+1, i+1)]
    rq = [c[j]/c[j-q]-1 for j in range(i-n+q, i+1)]
    v1 = sum(x*x for x in r1)/len(r1); vq = sum(x*x for x in rq)/len(rq)
    return vq/(q*v1) if v1 else None

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); bars = lab.load_bars(); last = bars["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    BR = lab_breadth.breadth_series(AS); T0 = PT.gen(AS, ctx, challenger.ruleset())
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [t for t in T0 if BR.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    row("LIVE ref", live, kw, cut)
    def f(t, fn, *a):
        s = t["sym"]; i = IX[s].get(t["t"][:10]); return None if i is None else fn(AS[s]["c"], i, *a)
    V = []
    for n in (60, 120, 250):
        V.append((f"ac1({n}d) < 0", lambda t, n=n: (lambda x: x is not None and x < 0)(f(t, ac1, n))))
        V.append((f"ac1({n}d) >= 0", lambda t, n=n: (lambda x: x is not None and x >= 0)(f(t, ac1, n))))
    for n in (120, 250):
        V.append((f"VR5({n}d) < 1", lambda t, n=n: (lambda x: x is not None and x < 1)(f(t, vr, n))))
        V.append((f"VR5({n}d) >= 1", lambda t, n=n: (lambda x: x is not None and x >= 1)(f(t, vr, n))))
    print("variants tried:", len(V))
    for n, g in V: row(n, [t for t in live if g(t)], kw, cut)
