"""Lab run 33: 'washout cascade' conditioners (consecutive lower lows, close at N-day low, 5d depth in ATR) on the LIVE setup (web-seeded: Algomatic '5-day mean reversion' cascade-of-lower-lows). Backtest only."""
import datetime
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
    print("keys:", list(AS[live[0]["sym"]].keys())[:12])
    BARS = lab.load_bars()
    def feat(t):
        b = BARS[t["sym"]]; di = {x["t"][:10]: i for i, x in enumerate(b)}; i = di.get(t["t"][:10])
        if i is None or i < 25: return None
        ll = 0
        while i - ll - 1 >= 0 and b[i-ll]["l"] < b[i-ll-1]["l"]: ll += 1
        lo = lambda n: b[i]["c"] <= min(x["c"] for x in b[i-n:i])
        rng = b[i]["h"] - b[i]["l"]; ibs = (b[i]["c"] - b[i]["l"]) / rng if rng > 0 else 0.5
        atr = sum(max(b[j]["h"], b[j-1]["c"]) - min(b[j]["l"], b[j-1]["c"]) for j in range(i-13, i+1)) / 14
        dep5 = (b[i-5]["c"] - b[i]["c"]) / atr
        return dict(ll=ll, lo5=lo(5), lo10=lo(10), lo20=lo(20), ibs=ibs, dep5=dep5)
    FT = {id(t): feat(t) for t in live}
    f = lambda t: FT[id(t)] or {}
    row("LIVE vol175", live, kw, cut)
    V = [("lower-lows streak >=2", lambda t: f(t).get("ll", 0) >= 2), ("lower-lows streak >=3", lambda t: f(t).get("ll", 0) >= 3),
         ("lower-lows streak <=1", lambda t: f(t).get("ll", 9) <= 1),
         ("close = 5d closing low", lambda t: f(t).get("lo5", False)), ("close = 10d closing low", lambda t: f(t).get("lo10", False)),
         ("close = 20d closing low", lambda t: f(t).get("lo20", False)),
         ("signal-day IBS <= 0.25", lambda t: f(t).get("ibs", 9) <= 0.25), ("signal-day IBS > 0.25", lambda t: f(t).get("ibs", -1) > 0.25),
         ("5d depth >= 3 ATR", lambda t: f(t).get("dep5", -9) >= 3), ("5d depth < 3 ATR", lambda t: f(t).get("dep5", 99) < 3)]
    print("variants tried:", len(V))
    for n, g in V: row(n, [t for t in live if g(t)], kw, cut)
    def tilt(hi, lo, th=3):
        out = []
        for t in live:
            u = dict(t); m = hi if f(t).get("ll", 0) >= th else lo; u["pnl_pct"] = t["pnl_pct"] * m; out.append(u)
        return out
    TV = ((1.5, 1.0), (1.25, 0.75), (1.5, 0.75))
    for hi, lo in TV: row(f"size LL>=3 x{hi} else x{lo}", tilt(hi, lo), kw, cut)
    print("tilt variants:", len(TV), "(total this run", len(V) + len(TV), ")")
