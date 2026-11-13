"""Lab run 47 (2026-11-13): idle-cash overlay - park unused capital of the LIVE setup in SPY (when SPY>200d) (own idea). Backtest only.
Daily series: trade pnl realised on exit date (size% x pnl%), overlay = cash fraction(prev close of day) x SPY daily return."""
import datetime
from collections import defaultdict
import lab, sweep, challenger
import portfolio_test as PT
import lab_breadth

def hv_filter(AS):
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    return lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))

def series(taken, spy, mode, cap=1.0, size=10.0, mult=1.0):
    ds = [x["t"][:10] for x in spy]; c = [x["c"] for x in spy]
    sma = [None] * len(c)
    for i in range(200, len(c)): sma[i] = sum(c[i - 200:i]) / 200
    ex = defaultdict(float); openn = defaultdict(int)
    idx = {d: i for i, d in enumerate(ds)}
    for t in taken:
        ex[t["t_exit"][:10]] += size / 100 * t["pnl_pct"] / 100
        a, b = idx.get(t["t"][:10]), idx.get(t["t_exit"][:10])
        if a is None or b is None: continue
        for k in range(a + 1, b + 1): openn[ds[k]] += 1
    start = min(t["t"][:10] for t in taken); rets = []
    for i in range(1, len(ds)):
        d = ds[i]
        if d < start: continue
        r = ex.get(d, 0.0)
        if mode != "none":
            cash = max(0.0, 1 - size / 100 * openn.get(d, 0)) * cap
            on = (mode == "always") or (sma[i - 1] is not None and c[i - 1] > sma[i - 1])
            if on: r += mult * cash * (c[i] / c[i - 1] - 1)
        rets.append((d, r))
    return rets

def stats(rets, cut):
    eq, peak, mdd = 1.0, 1.0, 0.0; yr = defaultdict(lambda: 1.0); l12 = 1.0; pk = {}
    for d, r in rets:
        eq *= 1 + r; peak = max(peak, eq); mdd = max(mdd, (peak - eq) / peak * 100)
        yr[d[:4]] *= 1 + r
        if d >= cut: l12 *= 1 + r
    import statistics
    m = defaultdict(float)
    for d, r in rets: m[d[:7]] += r
    ms = list(m.values()); sh = statistics.mean(ms) / statistics.pstdev(ms) * 12 ** .5
    return round((eq - 1) * 100, 1), round(mdd, 1), round(sh, 2), round((l12 - 1) * 100, 1), {y: round((v - 1) * 100, 1) for y, v in sorted(yr.items())}

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    B = lab_breadth.breadth_series(AS); hv = hv_filter(AS)
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    base = [t for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    P = lab.portfolio(base, **kw); tk = P["trades"]
    print("LIVE n", P["n"], "PF", P["pf_pct"], "ret", P["ret_pct"], "mdd", P["mdd"], "| last", last)
    V = [("LIVE alone", "none", 1.0), ("cash->SPY when SPY>200d, 100% of cash", "spy200", 1.0),
         ("cash->SPY when SPY>200d, 50% of cash", "spy200", .5), ("cash->SPY always, 50% of cash", "always", .5),
         ("cash->SPY always, 100% of cash", "always", 1.0)]
    print("variants tried:", len(V) - 1)
    for nm, mode, cap in V:
        r = series(tk, spy, mode, cap); print(f"{nm:42}", stats(r, cut))
    # SPY buy&hold over same window, and avg cash fraction
    st = tk and min(t["t"][:10] for t in tk)
    bh = [(x["t"][:10], x["c"] / spy[i - 1]["c"] - 1) for i, x in enumerate(spy) if i and x["t"][:10] >= st]
    print("SPY buy&hold", stats(bh, cut))
    ds = [x["t"][:10] for x in spy]
    print("done")
