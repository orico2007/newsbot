"""Lab run 87 (2026-11-24): Parkinson range-vol and range-vol/close-vol ratio as conditioners of live vol60+zreg setup. Backtest only."""
import math
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats
from lab_zscore import zreg

def feat(A, i, n=20):
    h, l, c = A["h"], A["l"], A["c"]
    pk = (sum(math.log(h[j]/l[j])**2 for j in range(i-n+1, i+1))/(4*math.log(2)*n))**.5
    r = [math.log(c[j]/c[j-1]) for j in range(i-n+1, i+1)]
    m = sum(r)/n; sd = (sum((x-m)**2 for x in r)/(n-1))**.5
    return pk*100, (pk/sd if sd else 1.0)

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(spy) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2; B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(t["t"][:10]); v = challenger.vol60(AS[t["sym"]], i)
            if v is not None and v >= 1.75 and i is not None and i >= 65 and zreg(AS[t["sym"]], i, 20) < -1.5:
                A = AS[t["sym"]]
                live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0), _f5=feat(A, i)[0], _f20=feat(A, i)[1]))
    row("LIVE (vol60+zreg)", live, kw, cut)
    n = 2
    for key, nm in (("_f5", "pk20"), ("_f20", "pkratio")):
        s = sorted(t[key] for t in live); q1, q2 = s[len(s)//3], s[2*len(s)//3]
        row(nm + " low third", [t for t in live if t[key] <= q1], kw, cut)
        row(nm + " mid third", [t for t in live if q1 < t[key] <= q2], kw, cut)
        row(nm + " high third", [t for t in live if t[key] > q2], kw, cut)
        row(nm + " skip low third", [t for t in live if t[key] > q1], kw, cut)
        row(nm + " skip high third", [t for t in live if t[key] <= q2], kw, cut)
        for en, f in (("early", lambda t: t["t"][:4] <= "2023"), ("late", lambda t: t["t"][:4] >= "2024")):
            row(f"  {en} ref", [t for t in live if f(t)], kw, cut)
            row(f"  {en} skip low", [t for t in live if f(t) and t[key] > q1], kw, cut)
            row(f"  {en} skip high", [t for t in live if f(t) and t[key] <= q2], kw, cut)
    print("variants tried: 10 + splits (run87)")
