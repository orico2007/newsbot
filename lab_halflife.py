"""Lab run 52 (2026-11-21): per-stock mean-reversion half-life (AR(1) on deviation of log price from its 20d SMA, trailing 252d) as selector of the vol60>=1.75% LIVE setup.
Source (search hits only, unverified): https://medium.com/@constandinou.antonio/quant-post-3-1-a-guided-path-into-mean-reversion-8b33b3c279e4 , https://arxiv.org/html/2412.12458v1 . Backtest only."""
import datetime, math
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def halflife(c, i, N=252, m=20):
    if i < N + m: return None
    x = [math.log(c[j]) - math.log(sum(c[j-m+1:j+1])/m) for j in range(i-N, i)]  # excludes signal day
    a = x[:-1]; b = [x[k+1]-x[k] for k in range(len(x)-1)]
    ma = sum(a)/len(a); mb = sum(b)/len(b)
    va = sum((u-ma)**2 for u in a)
    if va == 0: return None
    beta = sum((u-ma)*(v-mb) for u, v in zip(a, b))/va
    return -math.log(2)/beta if beta < 0 else 999.0

def vratio(c, i, N=252, q=5):
    r = [math.log(c[j]/c[j-1]) for j in range(i-N+1, i)]
    m = sum(r)/len(r); v1 = sum((x-m)**2 for x in r)/len(r)
    rq = [sum(r[k:k+q]) for k in range(len(r)-q+1)]; mq = sum(rq)/len(rq)
    vq = sum((x-mq)**2 for x in rq)/len(rq)
    return vq/(q*v1) if v1 > 0 else None

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(spy) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2; B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(t["t"][:10]); v = challenger.vol60(AS[t["sym"]], i) if i else None
            if v is not None and v >= 1.75 and i >= 30:
                c = AS[t["sym"]]["c"]
                live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0), hl=halflife(c, i), vr=vratio(c, i) if i > 260 else None))
    row("LIVE ref", live, kw, cut)
    ok = [t for t in live if t["hl"] is not None and t["vr"] is not None]
    print("with stats", len(ok), "of", len(live))
    for k in ("hl", "vr"):
        q = sorted(t[k] for t in ok); print(k, "terciles", [round(q[int(len(q)*p)], 3) for p in (.33, .67)])
    V = []
    for k in ("hl", "vr"):
        q = sorted(t[k] for t in ok); lo, hi = q[len(q)//3], q[2*len(q)//3]
        V += [(k+" low third", lambda t, k=k, lo=lo: t[k] <= lo), (k+" mid third", lambda t, k=k, lo=lo, hi=hi: lo < t[k] <= hi), (k+" high third", lambda t, k=k, hi=hi: t[k] > hi)]
    for nm, f in V:
        sub = [t for t in ok if f(t)]
        if len(sub) > 15: row(nm, sub, kw, cut)
        else: print(nm, "n=", len(sub))
    print("variants tried:", len(V))
