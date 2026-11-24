"""Lab run 80 (2026-11-24): day-of-month buckets (payday / mid-month) as conditioner of live vol60+zreg setup (own idea). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_zscore import zreg

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(spy) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2; B = breadth_series(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(t["t"][:10]); v = challenger.vol60(AS[t["sym"]], i)
            if v is not None and v >= 1.75 and i is not None and i >= 65 and zreg(AS[t["sym"]], i, 20) < -1.5:
                live.append(t)
    row("LIVE ref", live, kw, cut)
    dom = lambda t: int(t["t"][8:10])
    B4 = [("d1-7", 1, 7), ("d8-14", 8, 14), ("d15-21", 15, 21), ("d22-31", 22, 31)]
    for n, a, b in B4: row("only " + n, [t for t in live if a <= dom(t) <= b], kw, cut)
    for n, a, b in B4: row("skip " + n, [t for t in live if not a <= dom(t) <= b], kw, cut)
    row("payday d13-17 only", [t for t in live if 13 <= dom(t) <= 17], kw, cut)
    row("skip payday d13-17", [t for t in live if not 13 <= dom(t) <= 17], kw, cut)
    print("variants tried: 11")
