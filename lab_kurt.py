"""Lab run 76 (2026-11-23): tail-proneness (60d excess kurtosis, worst day in 60d scaled by vol60) as conditioner on live vol60+zreg setup. Own idea. Backtest only."""
import datetime, math
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats
from lab_zscore import zreg

def tail(A, i, n=60):
    c = A["c"]; r = [c[j]/c[j-1]-1 for j in range(i-n+1, i+1)]
    m = sum(r)/n; s2 = sum((x-m)**2 for x in r)/n
    if s2 <= 0: return 0, 0
    k = sum((x-m)**4 for x in r)/n/s2**2 - 3
    return k, min(r)/math.sqrt(s2)

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
                k, w = tail(AS[t["sym"]], i)
                live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0), _k=k, _w=w))
    row("LIVE (vol60+zreg)", live, kw, cut)
    for key, nm in (("_k", "kurtosis"), ("_w", "worst-day z")):
        s = sorted(t[key] for t in live); q1, q2 = s[len(s)//3], s[2*len(s)//3]
        row(nm + " low third", [t for t in live if t[key] <= q1], kw, cut)
        row(nm + " mid third", [t for t in live if q1 < t[key] <= q2], kw, cut)
        row(nm + " high third", [t for t in live if t[key] > q2], kw, cut)
        row(nm + " skip high third", [t for t in live if t[key] <= q2], kw, cut)
        row(nm + " skip low third", [t for t in live if t[key] > q1], kw, cut)
        for en, f in (("early", lambda t: t["t"][:4] <= "2023"), ("late", lambda t: t["t"][:4] >= "2024")):
            row(f"  {en} ref", [t for t in live if f(t)], kw, cut)
            row(f"  {en} skip high", [t for t in live if f(t) and t[key] <= q2], kw, cut)
    print("variants tried: 10 + splits")
