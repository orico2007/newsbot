"""Lab run 79 (2026-11-24): OBV / net volume-flow share (5d, 20d) as conditioner of live vol60+zreg setup. Web-seeded (OBV divergence search hits). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats
from lab_zscore import zreg

def flow(A, i, n):
    c, v = A["c"], A["v"]; num = den = 0.0
    for j in range(i-n+1, i+1):
        s = 1 if c[j] > c[j-1] else -1 if c[j] < c[j-1] else 0
        num += s*v[j]; den += v[j]
    return num/den if den else 0.0

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
                live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0), _f5=flow(A, i, 5), _f20=flow(A, i, 20)))
    row("LIVE (vol60+zreg)", live, kw, cut)
    n = 2
    for key, nm in (("_f5", "flow5"), ("_f20", "flow20")):
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
    print("variants tried: 10 + splits")
