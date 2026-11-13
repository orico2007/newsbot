"""Lab run 41 (2026-11-13): signal-day cluster size and per-day / position caps on the LIVE vol60>=1.75% setup (own idea). Backtest only."""
import datetime, collections
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); raw = lab.load_bars(); last = raw["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    B = lab_breadth.breadth_series(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    base = [t for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    cnt = collections.Counter(t["t"][:10] for t in base)
    print("n", len(base), "signals/day distribution", sorted(collections.Counter(cnt.values()).items()))
    row("LIVE ref (4/day, 12 pos, 10%)", base, kw, cut)
    V = [("per_day 1", dict(kw, per_day=1)), ("per_day 2", dict(kw, per_day=2)), ("per_day 3", dict(kw, per_day=3)),
         ("per_day 6", dict(kw, per_day=6)), ("max_pos 8", dict(kw, max_pos=8)), ("max_pos 16", dict(kw, max_pos=16))]
    print("variants tried:", len(V) + 4)
    for nm, k in V: row(nm, base, k, cut)
    row("signal-day cluster 1-2 signals", [t for t in base if cnt[t["t"][:10]] <= 2], kw, cut)
    row("signal-day cluster 3+ signals", [t for t in base if cnt[t["t"][:10]] >= 3], kw, cut)
    row("signal-day cluster 5+ signals", [t for t in base if cnt[t["t"][:10]] >= 5], kw, cut)
    # 3-day trailing heat: signals on this and prior 2 calendar signal days
    days = sorted(cnt); dix = {d: i for i, d in enumerate(days)}
    heat = lambda d: sum(cnt[days[j]] for j in range(max(0, dix[d]-2), dix[d]+1))
    hs = sorted(heat(d) for d in days); med = hs[len(hs)//2]; print("heat median", med)
    row("3-signal-day heat <= median", [t for t in base if heat(t["t"][:10]) <= med], kw, cut)
