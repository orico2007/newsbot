"""Lab run 49 (2026-11-14): downside semi-deviation / up-vs-down vol asymmetry / worst-day crash history as selectors on the LIVE setup. Own idea. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth

def feats(A, i):
    """(downside semi-dev %, upside semi-dev %, worst 1d return %) over last 60 daily returns ending at i."""
    if i is None or i < 61: return None
    r = [A["c"][j] / A["c"][j - 1] - 1 for j in range(i - 59, i + 1)]
    dn = (sum(min(x, 0) ** 2 for x in r) / 60) ** 0.5 * 100
    up = (sum(max(x, 0) ** 2 for x in r) / 60) ** 0.5 * 100
    return dn, up, min(r) * 100

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); bars = lab.load_bars(); last = bars["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    BR = lab_breadth.breadth_series(AS)
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    F = lambda t: feats(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10]))
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    base = [t for t in T0 if BR.get(t["t"][:10], (0, 0))[0] >= 0.10]
    live = [t for t in base if hv(t)]
    row("LIVE ref", live, kw, cut)
    row("breadth-only (no vol filter)", base, kw, cut)
    def c(fn): return lambda t: (lambda f: f is not None and fn(f))(F(t))
    V = [("no vol filter; downside dev >=1.3", base, c(lambda f: f[0] >= 1.3)),
         ("no vol filter; downside dev >=1.5", base, c(lambda f: f[0] >= 1.5)),
         ("LIVE & down/up ratio < 1.0", live, c(lambda f: f[0] < f[1])),
         ("LIVE & down/up ratio >= 1.0", live, c(lambda f: f[0] >= f[1])),
         ("LIVE & worst day > -8%", live, c(lambda f: f[2] > -8)),
         ("LIVE & worst day <= -8%", live, c(lambda f: f[2] <= -8))]
    print("variants tried:", len(V))
    for n, src, g in V:
        row(n, [t for t in src if g(t)], kw, cut)
