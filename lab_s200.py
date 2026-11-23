"""Lab run 78 (2026-11-23): long-term trend strength (distance above SMA200, SMA200 slope over 60d, trend age = days above SMA200 in last 252) as conditioners of the live vol60+zreg setup. Own idea. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats
from lab_zscore import zreg

def f200(A, i):
    s = A["s200"]; c = A["c"]
    dist = (c[i]/s[i]-1)*100
    slope = (s[i]/s[i-60]-1)*100 if s[i-60] else 0
    age = sum(1 for j in range(i-251, i+1) if A["s200"][j] and c[j] > A["s200"][j])
    return dist, slope, age

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(spy) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2; B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(t["t"][:10]); v = challenger.vol60(AS[t["sym"]], i)
            if v is not None and v >= 1.75 and i is not None and i >= 265 and zreg(AS[t["sym"]], i, 20) < -1.5:
                d, s, a = f200(AS[t["sym"]], i)
                live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0), _d=d, _s=s, _a=a))
    row("LIVE (vol60+zreg)", live, kw, cut)
    n = 0
    for key, nm in (("_d", "dist>SMA200"), ("_s", "SMA200 slope60"), ("_a", "trend age")):
        s = sorted(t[key] for t in live); q1, q2 = s[len(s)//3], s[2*len(s)//3]; print(nm, "cuts", round(q1,2), round(q2,2))
        for lab_, f in (("low third", lambda t: t[key] <= q1), ("mid third", lambda t: q1 < t[key] <= q2), ("high third", lambda t: t[key] > q2),
                        ("skip high", lambda t: t[key] <= q2), ("skip low", lambda t: t[key] > q1)):
            row(f"{nm} {lab_}", [t for t in live if f(t)], kw, cut); n += 1
        for en, g in (("early", lambda t: t["t"][:4] <= "2023"), ("late", lambda t: t["t"][:4] >= "2024")):
            row(f"  {en} ref", [t for t in live if g(t)], kw, cut)
            row(f"  {en} skip high", [t for t in live if g(t) and t[key] <= q2], kw, cut)
            row(f"  {en} skip low", [t for t in live if g(t) and t[key] > q1], kw, cut)
    print("variants tried:", n, "+ splits")
