"""Lab run 51 (2026-11-20): information-discreteness ("frog in the pan", Da/Gurun/Warachka 2014) of the pre-signal decline as conditioner of the vol60>=1.75% LIVE setup.
ID = sign(R_n) * (share of down days - share of up days) over last n days; for a dip R<0 so ID = %up - %down: high = discrete (few big down days), low = continuous slide.
Also: share of the n-day drop caused by its single largest down day. Sources (search hits only, unverified): https://www3.nd.edu/~zda/Frog.pdf . Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def idisc(c, i, n):
    r = [c[j]/c[j-1]-1 for j in range(i-n+1, i+1)]
    tot = c[i]/c[i-n]-1
    up = sum(1 for x in r if x > 0)/n; dn = sum(1 for x in r if x < 0)/n
    sgn = -1 if tot < 0 else 1
    big = min(r); drops = sum(x for x in r if x < 0)
    return sgn*(dn-up), (big/drops if drops < 0 else 0)

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
                d = {}
                for n in (10, 20):
                    d["id%d" % n], d["mx%d" % n] = idisc(c, i, n)
                live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0), **d))
    row("LIVE ref", live, kw, cut)
    for k in ("id10", "id20", "mx10", "mx20"):
        q = sorted(t[k] for t in live); print(k, "quartiles", [round(q[int(len(q)*p)], 3) for p in (.25, .5, .75)])
    V = []
    for k in ("id10", "id20"):
        q = sorted(t[k] for t in live); med = q[len(q)//2]
        V += [(k+" > median (continuous slide: more down days)", lambda t, k=k, m=med: t[k] > m), (k+" <= median (discrete: few big drops)", lambda t, k=k, m=med: t[k] <= m)]
    for k in ("mx10", "mx20"):
        q = sorted(t[k] for t in live); med = q[len(q)//2]
        V += [(k+" >= median (one day dominates)", lambda t, k=k, m=med: t[k] >= m), (k+" < median (spread over days)", lambda t, k=k, m=med: t[k] < m)]
    for nm, f in V:
        sub = [t for t in live if f(t)]
        if len(sub) > 15: row(nm, sub, kw, cut)
        else: print(nm, "n=", len(sub))
    print("variants tried:", len(V))
