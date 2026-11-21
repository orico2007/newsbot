"""Lab run 55 (2026-11-21): 12-1 month momentum (close[i-21]/close[i-252]-1) as conditioner of live vol60>=1.75% setup. Web-seeded by search hits (Novy-Marx reversals paper, snippet only). Backtest only."""
import datetime, statistics
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(spy) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2; B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(t["t"][:10]); v = challenger.vol60(AS[t["sym"]], i) if i else None
            if v is not None and v >= 1.75 and i >= 260:
                c = AS[t["sym"]]["c"]
                live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0), m=c[i-21]/c[i-252]-1))
    med = statistics.median(x["m"] for x in live); print("n", len(live), "median", round(med, 3))
    row("LIVE ref", live, kw, cut)
    print("variants tried: 4")
    row("mom121 >= median", [t for t in live if t["m"] >= med], kw, cut)
    row("mom121 < median", [t for t in live if t["m"] < med], kw, cut)
    row("mom121 > 0", [t for t in live if t["m"] > 0], kw, cut)
    row("mom121 <= 0", [t for t in live if t["m"] <= 0], kw, cut)
