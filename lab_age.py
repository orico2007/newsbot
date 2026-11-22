"""Lab run 64 (2026-11-22): age of the decline (days since 60d closing high) and 20d trend slope as conditioners of the vol60>=1.75% live setup. Own idea (web search found only generic pullback pages). Backtest only."""
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
                c = AS[t["sym"]]["c"]; w = c[i-60:i+1]
                age = 60 - w.index(max(w)); 
                slope = c[i] / c[i-20] - 1
                live.append(dict(t, age=age, slope=slope))
    row("LIVE ref", live, kw, cut); n = 1
    for a in (5, 10, 20, 30):
        n += 2
        row(f"age<={a}", [t for t in live if t["age"] <= a], kw, cut)
        row(f"age>{a}", [t for t in live if t["age"] > a], kw, cut)
    for s in (-.10, -.05, 0):
        n += 2
        row(f"20d ret<={s}", [t for t in live if t["slope"] <= s], kw, cut)
        row(f"20d ret>{s}", [t for t in live if t["slope"] > s], kw, cut)
    print("variants tried:", n)
    from lab_wftilt import scaled
    row("20d>-5% & age<=20", [t for t in live if t["slope"] > -.05 and t["age"] <= 20], kw, cut)
    row("20d>-7.5%", [t for t in live if t["slope"] > -.075], kw, cut)
    row("20d>-3%", [t for t in live if t["slope"] > -.03], kw, cut)
    for lo in (.5, .75):
        row(f"size {lo}x if 20d<=-5% else 1x", scaled(live, [lo if t["slope"] <= -.05 else 1 for t in live]), kw, cut)
    row("size 1.25x if 20d>-5% else .5x", scaled(live, [1.25 if t["slope"] > -.05 else .5 for t in live]), kw, cut)
    print("total variants:", n + 6)
    # walk-forward style: split halves for the 20d<=-5% bucket
    for lab_, f in (("<=2023", lambda t: t["t"][:4] <= "2023"), (">=2024", lambda t: t["t"][:4] >= "2024")):
        sub = [t for t in live if f(t)]
        row("half " + lab_ + " all", sub, kw, cut); row("half " + lab_ + " 20d>-5%", [t for t in sub if t["slope"] > -.05], kw, cut)
