"""Lab run 62 (2026-11-22): SPY drawdown from its N-day closing high on the signal day as filter / size tilt of the vol60>=1.75% live setup. Own idea. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_wftilt import pf, scaled

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); S = lab.load_bars()["SPY"]
    cut = (datetime.date.fromisoformat(S[-1]["t"][:10]) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2; B = breadth_series(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    sc = [b["c"] for b in S]; sd = [b["t"][:10] for b in S]
    dd = {}
    for N in (20, 60, 120):
        for i in range(N, len(sc)): dd[(N, sd[i])] = sc[i] / max(sc[i-N:i+1]) - 1
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        d = t["t"][:10]
        if B.get(d, (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(d); v = challenger.vol60(AS[t["sym"]], i) if i else None
            if v is not None and v >= 1.75 and i >= 70: live.append(dict(t, d=d))
    row("LIVE ref", live, kw, cut); n = 1
    for N in (20, 60, 120):
        for th in (-.02, -.04, -.06):
            n += 2
            row(f"SPY dd{N} <= {th}", [t for t in live if dd.get((N, t['d']), 0) <= th], kw, cut)
            row(f"SPY dd{N} >  {th}", [t for t in live if dd.get((N, t['d']), 0) > th], kw, cut)
    print("variants tried:", n)
    for N, th in ((20, -.02), (60, -.04)):
        ms = [1.25 if dd.get((N, t['d']), 0) <= th else .75 for t in live]
        row(f"size tilt dd{N}<={th} 1.25/.75", scaled(live, ms), kw, cut)
