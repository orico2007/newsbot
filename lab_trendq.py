"""Lab run 50 (2026-11-20): prior-trend quality (60d log-price R^2 and slope), MACD(12,26,9) histogram depth, as conditioners of the vol60>=1.75% LIVE setup. Web-seeded by search only (OU half-life / mean-reversion pages, e.g. https://medium.com/@constandinou.antonio/quant-post-3-1-a-guided-path-into-mean-reversion-8b33b3c279e4 , snippet only, unverified). Backtest only."""
import datetime, math
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def r2slope(c, i, n=60):
    y = [math.log(x) for x in c[i-n+1:i+1]]; xs = range(n); mx = (n-1)/2; my = sum(y)/n
    sxx = sum((x-mx)**2 for x in xs); sxy = sum((x-mx)*(v-my) for x, v in zip(xs, y)); syy = sum((v-my)**2 for v in y)
    if sxx == 0 or syy == 0: return 0, 0
    return sxy*sxy/(sxx*syy), sxy/sxx*n  # slope scaled to total log move over window

def ema(c, n):
    k = 2/(n+1); e = [c[0]]
    for v in c[1:]: e.append(e[-1]+k*(v-e[-1]))
    return e

def macdh(c):
    m = [a-b for a, b in zip(ema(c, 12), ema(c, 26))]; s = ema(m, 9)
    return [(a-b)/x for a, b, x in zip(m, s, c)]

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(spy) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2; B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    H = {}
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(t["t"][:10]); v = challenger.vol60(AS[t["sym"]], i) if i else None
            if v is not None and v >= 1.75 and i >= 80:
                A = AS[t["sym"]]
                if t["sym"] not in H: H[t["sym"]] = macdh(A["c"])
                # trend measured on the 60 days ending 5 days before signal (excludes the dip itself)
                r2, sl = r2slope(A["c"], i-5)
                live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0), _r2=r2, _sl=sl, _mh=H[t["sym"]][i]))
    row("LIVE ref", live, kw, cut)
    for k in ("_r2", "_sl", "_mh"):
        q = sorted(t[k] for t in live); print(k, "quartiles", [round(q[int(len(q)*p)], 3) for p in (.25, .5, .75)])
    V = [("prior60 R2 >= 0.5", lambda t: t["_r2"] >= .5), ("prior60 R2 < 0.5", lambda t: t["_r2"] < .5),
         ("prior60 R2>=.5 & slope>0", lambda t: t["_r2"] >= .5 and t["_sl"] > 0), ("prior60 slope > 0", lambda t: t["_sl"] > 0),
         ("prior60 slope > 0.10", lambda t: t["_sl"] > .10), ("prior60 slope <= 0", lambda t: t["_sl"] <= 0),
         ("MACD hist/price < -0.5%", lambda t: t["_mh"] < -.005), ("MACD hist/price < -1%", lambda t: t["_mh"] < -.01), ("MACD hist/price >= -0.5%", lambda t: t["_mh"] >= -.005)]
    for nm, f in V:
        sub = [t for t in live if f(t)]
        if len(sub) > 15: row(nm, sub, kw, cut)
        else: print(nm, "n=", len(sub))
    print("variants tried:", len(V))
