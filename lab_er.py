"""Lab run 48 (2026-11-18): Kaufman efficiency ratio (straight vs choppy decline) as conditioner of the vol60>=1.75% LIVE setup. Backtest only."""
import datetime, statistics
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def er(c, i, n):
    p = sum(abs(c[k]-c[k-1]) for k in range(i-n+1, i+1))
    return 0 if p == 0 else (c[i]-c[i-n])/p

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
                live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0), e5=er(c,i,5), e10=er(c,i,10), px=c[i]))
    live = [t for t in live if True]
    row("LIVE ref", live, kw, cut)
    for k in ("e5","e10"):
        v = sorted(t[k] for t in live); print(k, "terciles", round(v[len(v)//3],2), round(v[2*len(v)//3],2))
    q = lambda k, lo, hi: (lambda t: lo <= t[k] < hi)
    V = []
    for k in ("e5","e10"):
        v = sorted(t[k] for t in live); a1, a2 = v[len(v)//3], v[2*len(v)//3]
        V += [(k+" lowest third (most straight down)", q(k,-9,a1)), (k+" middle", q(k,a1,a2)), (k+" top third (choppy/up)", q(k,a2,9))]
    V += [("e5 < -0.6", q("e5",-9,-.6)), ("e5 >= -0.6", q("e5",-.6,9))]
    for n, f in V:
        sub = [t for t in live if f(t)]
        if len(sub) > 20: row(n, sub, kw, cut)
    print("variants tried: 8")
