"""Lab run 22 (2026-11-16): liquidity / price-level conditioners on the LIVE setup trades (20d dollar volume, share price).
Web hint: cross-sectional reversal papers/blogs screen on >$5M dollar volume and price>$5 (https://delphicalpha.substack.com/p/us-equity-cross-sectional-mean-reversion , unverified). Backtest only."""
import datetime, statistics
import lab, sweep, challenger
import portfolio_test as PT
import lab_breadth, lab_sector
from lab_52wh import row

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = challenger.DEF_PORT
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    B = lab_breadth.breadth_series(AS); F = lab_sector.feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    def dv(t):
        A = AS[t["sym"]]; i = IX[t["sym"]][t["t"][:10]]
        return statistics.median(A["c"][k] * A["v"][k] for k in range(i - 19, i + 1))
    def px(t): return AS[t["sym"]]["c"][IX[t["sym"]][t["t"][:10]]]
    # time-neutral: percentile of the stock's 20d dollar volume among ALL universe stocks on the same date
    CACHE = {}
    def pct(t):
        d = t["t"][:10]
        if d not in CACHE:
            vals = {}
            for s2, A in AS.items():
                j = IX[s2].get(d)
                if j is not None and j >= 19: vals[s2] = statistics.median(A["c"][k] * A["v"][k] for k in range(j - 19, j + 1))
            r = sorted(vals.values()); CACHE[d] = (vals, r)
        vals, r = CACHE[d]; return sum(1 for x in r if x <= vals[t["sym"]]) / len(r)
    D = sorted(pct(t) for t in live); P_ = sorted(px(t) for t in live)
    q = lambda L, f: L[int(f * (len(L) - 1))]
    dv = pct; q = lambda L, f: f if L is D else L[int(f * (len(L) - 1))]
    print("n live", len(live), "time-neutral dollar-vol percentile (universe, same date); price terciles", q(P_, .33), q(P_, .67))
    V = [("dollar vol top 2/3", lambda t: dv(t) >= q(D, .33)), ("dollar vol bottom 2/3", lambda t: dv(t) <= q(D, .67)),
         ("dollar vol top 1/3", lambda t: dv(t) >= q(D, .67)), ("dollar vol bottom 1/3", lambda t: dv(t) <= q(D, .33)),
         ("price >= $20", lambda t: px(t) >= 20), ("price < $50", lambda t: px(t) < 50),
         ("price top 2/3", lambda t: px(t) >= q(P_, .33)), ("price bottom 2/3", lambda t: px(t) <= q(P_, .67))]
    print("variants tried:", len(V) + 1)
    row("LIVE (vol175)", live, kw, cut)
    for n, f in V: row(n, [t for t in live if f(t)], kw, cut)
