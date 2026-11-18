"""Lab run 46 (2026-11-18): 60d return skewness and share-price level as conditioners of the vol60>=1.75% LIVE setup. Backtest only."""
import datetime, statistics
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def skew(c, i, n=60):
    r = [c[k]/c[k-1]-1 for k in range(i-n+1, i+1)]
    m = sum(r)/n; sd = (sum((x-m)**2 for x in r)/n)**.5
    return 0 if sd == 0 else sum(((x-m)/sd)**3 for x in r)/n

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    champ = PT.gen(AS, ctx, challenger.ruleset()); live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(t["t"][:10]); v = challenger.vol60(AS[t["sym"]], i)
            if v is not None and v >= 1.75:
                c = AS[t["sym"]]["c"]
                live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0), sk=skew(c, i) if i and i > 60 else None, px=c[i]))
    live = [t for t in live if t["sk"] is not None]
    row("LIVE ref", live, kw, cut)
    sks = sorted(t["sk"] for t in live); med = sks[len(sks)//2]
    pxs = sorted(t["px"] for t in live); pmed = pxs[len(pxs)//2]
    print("median skew", round(med, 2), "median px", round(pmed, 1))
    V = [("skew60 < median", lambda t: t["sk"] < med), ("skew60 >= median", lambda t: t["sk"] >= med),
         ("skew60 < 0", lambda t: t["sk"] < 0), ("skew60 >= 0.5", lambda t: t["sk"] >= .5),
         ("px < median", lambda t: t["px"] < pmed), ("px >= median", lambda t: t["px"] >= pmed),
         ("px >= 50", lambda t: t["px"] >= 50), ("px < 50", lambda t: t["px"] < 50)]
    for n, f in V:
        sub = [t for t in live if f(t)]
        if len(sub) > 20: row(n, sub, kw, cut)
    print("variants tried: 8")
