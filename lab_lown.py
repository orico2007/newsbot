"""Lab run 54 (2026-11-21): 'signal-day close is the lowest close of the last N days' filter on the live vol60>=1.75% + zreg setup. Own idea. Backtest only."""
import datetime
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
            if v is not None and v >= 1.75 and i >= 70:
                c = AS[t["sym"]]["c"]
                live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0),
                                 lown={N: c[i] <= min(c[i-N:i]) for N in (10, 20, 40, 60)}))
    row("LIVE ref (vol only, before zreg)", live, kw, cut)
    print("variants tried: 8")
    for N in (10, 20, 40, 60):
        row(f"close = {N}d low", [t for t in live if t["lown"][N]], kw, cut)
        row(f"close NOT {N}d low (complement)", [t for t in live if not t["lown"][N]], kw, cut)
