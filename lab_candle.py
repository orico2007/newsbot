"""Lab run 30 (2026-11-11): signal-day candle structure (lower-low vs inside day, close below prior low, range expansion, red body size) as conditioner
of the LIVE vol60>=1.75% setup. Web seed: Quantified Strategies / Connors-style 'lower low' pullback write-ups (unverified). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    base = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10]
    live = [t for t in base if (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))]
    def f(t):
        A = AS[t["sym"]]; i = IX[t["sym"]].get(t["t"][:10])
        if not i or i < 21: return None
        o, h, l, c = A["o"], A["h"], A["l"], A["c"]
        rng = h[i]-l[i]; avg = sum(h[j]-l[j] for j in range(i-20, i))/20
        return dict(lowerlow=l[i] < l[i-1], inside=h[i] <= h[i-1] and l[i] >= l[i-1],
                    belowlow=c[i] < l[i-1], rx=rng/avg if avg else 0, body=(o[i]-c[i])/o[i] if o[i] else 0,
                    low3=c[i] < min(l[i-3:i]))
    row("LIVE ref", live, kw, cut)
    V = [("lower low today", lambda x: x["lowerlow"]), ("NOT lower low", lambda x: not x["lowerlow"]),
         ("close < prior low", lambda x: x["belowlow"]), ("close >= prior low", lambda x: not x["belowlow"]),
         ("range >= 1.5x avg20", lambda x: x["rx"] >= 1.5), ("range < 1.5x", lambda x: x["rx"] < 1.5),
         ("red body >= 2%", lambda x: x["body"] >= .02), ("red body < 2%", lambda x: x["body"] < .02),
         ("close < min low prior 3d", lambda x: x["low3"]), ("not", lambda x: not x["low3"])]
    print("variants tried:", len(V)+1)
    for n, fn in V:
        S = [t for t in live if (lambda x: x is not None and fn(x))(f(t))]
        row(n, S, kw, cut)
