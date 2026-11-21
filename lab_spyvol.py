"""Lab run 57 (2026-11-21): SPY signal-day volume ratio (SPY vol / 20d avg) as conditioner of the live vol60>=1.75% setup. Own idea. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); bars = lab.load_bars(); S = bars["SPY"]
    spy = S[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(spy) - datetime.timedelta(days=365)).isoformat()
    sv = {b["t"][:10]: b.get("v") for b in S}; ds = [b["t"][:10] for b in S]
    ratio = {}
    for k in range(20, len(S)):
        a = [S[j].get("v") for j in range(k-20, k)]
        if all(a) and S[k].get("v"): ratio[ds[k]] = S[k]["v"] / (sum(a)/20)
    print("SPY vol ratios:", len(ratio))
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2; B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        d = t["t"][:10]
        if B.get(d, (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(d); v = challenger.vol60(AS[t["sym"]], i) if i else None
            if v is not None and v >= 1.75 and i >= 70 and d in ratio:
                live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0), sr=ratio[d]))
    import statistics
    med = statistics.median(t["sr"] for t in live); print("median SPY vol ratio on signal days", round(med, 2))
    row("LIVE ref (before zreg)", live, kw, cut)
    print("variants tried: 4")
    row("SPY vol ratio >= median", [t for t in live if t["sr"] >= med], kw, cut)
    row("SPY vol ratio < median", [t for t in live if t["sr"] < med], kw, cut)
    row("SPY vol ratio >= 1.2", [t for t in live if t["sr"] >= 1.2], kw, cut)
    row("SPY vol ratio < 1.2", [t for t in live if t["sr"] < 1.2], kw, cut)
    def tilt(T, thr, hi, lo):
        out = []
        for t in T:
            m = hi if t["sr"] >= thr else lo
            u = dict(t); u["pnl_pct"] = t["pnl_pct"]*m
            if "R" in u: u["R"] = t["R"]*m
            out.append(u)
        return out
    print("--- size tilts")
    V = [(med, 1.25, .75), (med, 1.5, .5), (1.2, 1.5, 1.0), (med, 1.0, .5)]
    for thr, hi, lo in V: row(f"tilt spyvol>={thr:.2f}: {hi}x else {lo}x", tilt(live, thr, hi, lo), kw, cut)
    print("variants tried total: 8")
    for nm, f in (("<=2023", lambda t: t["t"][:4] <= "2023"), (">=2024", lambda t: t["t"][:4] >= "2024")):
        S = [t for t in live if f(t)]
        row("live " + nm, S, kw, cut); row("tilt 1.5/.5 " + nm, tilt(S, med, 1.5, .5), kw, cut)
