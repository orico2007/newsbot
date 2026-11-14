"""Lab run 50 (2026-11-14): sector-level washout (share of same-sector peers with RSI2<10 on signal day) as conditioner of the LIVE setup.
Web seed: SentimenTrader sector capitulation posts (https://sentimentrader.com/blog/massive-capitulation-in-the-utilities-sector); rules are my own. Backtest only."""
import datetime
import lab, sweep, challenger, market
import portfolio_test as PT
from lab_52wh import row
import lab_breadth

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); raw = lab.load_bars(); last = raw["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    B = lab_breadth.breadth_series(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    sec = {}
    for s in AS: sec.setdefault(market.SECTOR_OF.get(s), []).append(s)
    def share(t):
        s = t["sym"]; d = t["t"][:10]; n = k = 0
        for p in sec.get(market.SECTOR_OF.get(s), []):
            if p == s: continue
            j = IX[p].get(d)
            if j is None or AS[p]["r2"][j] is None: continue
            n += 1; k += AS[p]["r2"][j] < 10
        return k / n if n >= 3 else None
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    live = [t for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    for t in live: t["_s"] = share(t)
    live = [t for t in live if t["_s"] is not None]
    v = sorted(t["_s"] for t in live); print("n", len(live), "median", v[len(v)//2], "terciles", v[len(v)//3], v[2*len(v)//3])
    row("LIVE ref", live, kw, cut)
    V = [("sector washout share >= 20%", lambda t: t["_s"] >= .2), ("sector washout share < 20%", lambda t: t["_s"] < .2),
         ("sector washout share >= 35%", lambda t: t["_s"] >= .35), ("sector washout share < 10%", lambda t: t["_s"] < .1),
         ("sector washout share >= 50%", lambda t: t["_s"] >= .5)]
    print("variants tried:", len(V) + 1)
    for n, f in V: row(n, [t for t in live if f(t)], kw, cut)
    row("rank by highest sector washout", [dict(t, score=t["_s"]) for t in live], kw, cut)
