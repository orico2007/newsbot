"""Lab run 72 (2026-11-23): Amihud illiquidity (20d mean |ret| / dollar volume) as a conditioner on the live vol60+zreg setup. Own idea. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats
from lab_zscore import zreg

def amihud(A, i, n=20):
    c, v = A["c"], A["v"]
    xs = [abs(c[j] / c[j-1] - 1) / max(c[j] * v[j], 1.0) for j in range(i - n + 1, i + 1)]
    return sum(xs) / n * 1e9

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(spy) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2; B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(t["t"][:10]); v = challenger.vol60(AS[t["sym"]], i)
            if v is not None and v >= 1.75 and i is not None and i >= 25 and zreg(AS[t["sym"]], i, 20) < -1.5:
                live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0), _a=amihud(AS[t["sym"]], i)))
    row("LIVE (vol60+zreg)", live, kw, cut)
    s = sorted(t["_a"] for t in live); q1, q2 = s[len(s)//3], s[2*len(s)//3]
    row("liquid third (low Amihud)", [t for t in live if t["_a"] <= q1], kw, cut)
    row("middle third", [t for t in live if q1 < t["_a"] <= q2], kw, cut)
    row("illiquid third (high Amihud)", [t for t in live if t["_a"] > q2], kw, cut)
    row("skip illiquid third", [t for t in live if t["_a"] <= q2], kw, cut)
    print("variants tried: 4")
    for nm, f in (("early 2021-23", lambda t: t["t"][:4] <= "2023"), ("late 2024-26", lambda t: t["t"][:4] >= "2024")):
        row(nm + " ref", [t for t in live if f(t)], kw, cut)
        row(nm + " skip illiquid", [t for t in live if f(t) and t["_a"] <= q2], kw, cut)
