"""Lab run 67 (2026-11-22): signal-day opening gap (vs prior close / prior low) and "gap with trend intact" as conditioners of the vol60>=1.75% live setup. Web-seeded: https://www.quantrocket.com/blog/buy-or-sell-down-gaps/ (small gaps recover, large gaps break the trend; unverified, 2014-2020 minute data). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); S = lab.load_bars()["SPY"]
    cut = (datetime.date.fromisoformat(S[-1]["t"][:10]) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2; B = breadth_series(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        d = t["t"][:10]
        if B.get(d, (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(d); v = challenger.vol60(AS[t["sym"]], i) if i else None
            if v is not None and v >= 1.75 and i >= 70:
                A = AS[t["sym"]]; c = A["c"]
                gap = A["o"][i] / c[i-1] - 1
                sd = v / 100 if v > .5 else v   # vol60 in pct
                live.append(dict(t, gap=gap, gz=gap / (v / 100), lowgap=A["o"][i] < A["l"][i-1],
                                 intra=c[i] / A["o"][i] - 1, ab20=A["o"][i] > A["s20"][i] if A["s20"][i] else False))
    row("LIVE ref", live, kw, cut); n = 1
    import statistics
    print("mean gap", statistics.mean(t["gap"] for t in live), "median gz", statistics.median(t["gz"] for t in live))
    for z in (-1.5, -1.0, -0.5, 0):
        n += 2
        row(f"gap z (gap/vol60) <= {z}", [t for t in live if t["gz"] <= z], kw, cut)
        row(f"gap z > {z}", [t for t in live if t["gz"] > z], kw, cut)
    n += 2
    row("open < prior low", [t for t in live if t["lowgap"]], kw, cut)
    row("open >= prior low", [t for t in live if not t["lowgap"]], kw, cut)
    n += 2
    row("open>SMA20 (trend intact)", [t for t in live if t["ab20"]], kw, cut)
    row("open<=SMA20", [t for t in live if not t["ab20"]], kw, cut)
    n += 2
    row("gap<0 & open<=SMA20", [t for t in live if t["gap"] < 0 and not t["ab20"]], kw, cut)
    row("gap>=0 (open at/above prior close)", [t for t in live if t["gap"] >= 0], kw, cut)
    n += 2
    row("intraday (o->c) <0", [t for t in live if t["intra"] < 0], kw, cut)
    row("intraday (o->c) >=0", [t for t in live if t["intra"] >= 0], kw, cut)
    print("variants tried:", n)
    for lab_, f in (("<=2023", lambda t: t["t"][:4] <= "2023"), (">=2024", lambda t: t["t"][:4] >= "2024")):
        sub = [t for t in live if f(t)]
        row("half " + lab_ + " all", sub, kw, cut); row("half " + lab_ + " gz>-1", [t for t in sub if t["gz"] > -1], kw, cut)
