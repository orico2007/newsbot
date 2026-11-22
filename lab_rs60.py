"""Lab run 68 (2026-11-22): stock relative strength vs SPY (20d/60d/120d return minus SPY's) and 60d up-day share as conditioners of the vol60>=1.75% live setup. Own idea. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); S = lab.load_bars()["SPY"]
    cut = (datetime.date.fromisoformat(S[-1]["t"][:10]) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2; B = breadth_series(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    SI = {b["t"][:10]: i for i, b in enumerate(S)}; sc = [b["c"] for b in S]
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        d = t["t"][:10]
        if B.get(d, (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(d); v = challenger.vol60(AS[t["sym"]], i) if i else None
            j = SI.get(d)
            if v is not None and v >= 1.75 and i >= 130 and j and j >= 130:
                c = AS[t["sym"]]["c"]; r = {}
                for n in (20, 60, 120):
                    r[n] = (c[i] / c[i-n] - 1) - (sc[j] / sc[j-n] - 1)
                up = sum(1 for k in range(i-59, i+1) if c[k] > c[k-1]) / 60
                live.append(dict(t, rs20=r[20], rs60=r[60], rs120=r[120], up=up))
    row("LIVE ref", live, kw, cut); n = 1
    import statistics
    for k in ("rs20", "rs60", "rs120", "up"):
        vals = sorted(t[k] for t in live); med = statistics.median(vals); q1 = vals[len(vals)//3]; q2 = vals[2*len(vals)//3]
        print(k, "tercile cuts", round(q1, 3), round(q2, 3))
        n += 4
        row(f"{k} top third", [t for t in live if t[k] > q2], kw, cut)
        row(f"{k} mid third", [t for t in live if q1 < t[k] <= q2], kw, cut)
        row(f"{k} bottom third", [t for t in live if t[k] <= q1], kw, cut)
        row(f"{k} >= median", [t for t in live if t[k] >= med], kw, cut)
    for th in (0, -0.05):
        n += 2
        row(f"rs60 > {th}", [t for t in live if t["rs60"] > th], kw, cut)
        row(f"rs60 <= {th}", [t for t in live if t["rs60"] <= th], kw, cut)
    print("variants tried:", n)
