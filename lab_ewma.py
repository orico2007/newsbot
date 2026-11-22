"""Lab run 65 (2026-11-22): EWMA (RiskMetrics) volatility forecast instead of / in addition to vol60>=1.75% as stock-volatility filter of the live setup.
Web-seeded by https://setup4alpha.substack.com/p/low-drawdown-nasdaq-mean-reversion (fetched; only says 'EWMA volatility forecast', no parameters; unverified). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series

def ewma(c, i, lam):
    v = None
    for j in range(max(1, i - 250), i + 1):
        r = c[j] / c[j-1] - 1
        v = r * r if v is None else lam * v + (1 - lam) * r * r
    return v ** .5 * 100

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); S = lab.load_bars()["SPY"]
    cut = (datetime.date.fromisoformat(S[-1]["t"][:10]) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2; B = breadth_series(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    base = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        d = t["t"][:10]
        if B.get(d, (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(d)
            if i and i >= 70:
                c = AS[t["sym"]]["c"]
                base.append(dict(t, v60=challenger.vol60(AS[t["sym"]], i), e94=ewma(c, i, .94), e97=ewma(c, i, .97)))
    live = [t for t in base if t["v60"] >= 1.75]
    row("LIVE ref (vol60>=1.75)", live, kw, cut); n = 1
    for lam in ("e94", "e97"):
        for th in (1.5, 1.75, 2.0, 2.25):
            n += 1; row(f"{lam}>={th}", [t for t in base if t[lam] >= th], kw, cut)
    for th in (1.5, 2.0):
        n += 1; row(f"vol60>=1.75 & e94>={th}", [t for t in live if t["e94"] >= th], kw, cut)
    n += 1; row("vol60>=1.75 & e94<vol60 (vol falling)", [t for t in live if t["e94"] < t["v60"]], kw, cut)
    n += 1; row("vol60>=1.75 & e94>=vol60 (vol rising)", [t for t in live if t["e94"] >= t["v60"]], kw, cut)
    print("variants tried:", n)
