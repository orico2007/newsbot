"""Lab run 40 (2026-11-18): Quantpedia 'Short-Term Correlated Stress Reversal' translated to cached ETFs (GLD/IEF/USO not in cache):
same-day concordant stress across risk assets / risk-off rotation as conditioner of the LIVE vol60>=1.75% setup. Web-seeded; backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); bars = lab.load_bars(); last = bars["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    BR = lab_breadth.breadth_series(AS); T0 = PT.gen(AS, ctx, challenger.ruleset())
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [t for t in T0 if BR.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    row("LIVE ref", live, kw, cut)
    R = {}
    for s in ("SPY", "QQQ", "IWM", "XLU", "XLP", "VIXY"):
        b = bars[s]; R[s] = {b[i]["t"][:10]: b[i]["c"] / b[i-1]["c"] - 1 for i in range(1, len(b))}
    g = lambda s, t: R[s].get(t["t"][:10])
    def f(fn): return lambda t: (lambda r: r is True)(fn(t))
    def both(a, b, ca, cb): return lambda t: g(a, t) is not None and g(b, t) is not None and ca(g(a, t)) and cb(g(b, t))
    dn = lambda x: x < 0; up = lambda x: x > 0
    V = [("SPY dn & XLU up (defensive rotation)", both("SPY", "XLU", dn, up)),
         ("SPY dn & XLP up", both("SPY", "XLP", dn, up)),
         ("SPY dn & VIXY up", both("SPY", "VIXY", dn, up)),
         ("SPY & QQQ & IWM all dn", lambda t: all(g(s, t) is not None and g(s, t) < 0 for s in ("SPY", "QQQ", "IWM"))),
         ("NOT (SPY dn & XLU up)", lambda t: not both("SPY", "XLU", dn, up)(t)),
         ("SPY dn & XLU dn (broad stress)", both("SPY", "XLU", dn, dn)),
         ("SPY dn & XLU dn & XLP dn", lambda t: all(g(s, t) is not None and g(s, t) < 0 for s in ("SPY", "XLU", "XLP"))),
         ("SPY up (control)", lambda t: g("SPY", t) is not None and g("SPY", t) > 0)]
    print("variants tried:", len(V))
    for n, fn in V: row(n, [t for t in live if fn(t)], kw, cut)
