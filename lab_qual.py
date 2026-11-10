"""Lab run 8 (2026-11-10): stock-quality filters (126d momentum, 60d realized vol, 200d MA slope, 252d range position) on the LIVE setup. Backtest only."""
import datetime, statistics
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); B = breadth_series(AS)
    from lab_sector import feats
    F = feats(AS); m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            u = dict(t); u["score"] = -m3(t); live.append(u)
    ix = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    def at(t):
        A = AS[t["sym"]]; return A, ix[t["sym"]].get(t["t"])
    def mom126(t):
        A, i = at(t); return None if i is None or i < 127 else A["c"][i] / A["c"][i-126] - 1
    def rvol(t):
        A, i = at(t)
        if i is None or i < 61: return None
        c = A["c"]; r = [c[k]/c[k-1]-1 for k in range(i-59, i+1)]; return statistics.pstdev(r)
    def slope(t):
        A, i = at(t)
        return None if i is None or i < 221 or not A.get("s200") or not A["s200"][i] or not A["s200"][i-20] else A["s200"][i]/A["s200"][i-20]-1
    def rng(t):
        A, i = at(t)
        if i is None or i < 253: return None
        h = max(A["c"][i-252:i+1]); l = min(A["c"][i-252:i+1]); return (A["c"][i]-l)/(h-l) if h > l else None
    med = lambda f: statistics.median([x for x in map(f, live) if x is not None])
    M, V, R = med(mom126), med(rvol), med(rng)
    print("medians mom126 %.3f rvol %.4f range %.3f" % (M, V, R))
    row("LIVE", live, kw, cut)
    Vs = [("mom126 > median", lambda t: (mom126(t) or -9) > M), ("mom126 < median", lambda t: (mom126(t) or 9) < M),
          ("mom126 > 0", lambda t: (mom126(t) or -9) > 0),
          ("rvol60 < median (low vol)", lambda t: (rvol(t) or 9) < V), ("rvol60 > median", lambda t: (rvol(t) or 0) > V),
          ("SMA200 rising", lambda t: (slope(t) or -9) > 0),
          ("252d range pos > median", lambda t: (rng(t) or -1) > R), ("252d range pos < median", lambda t: (rng(t) or 9) < R)]
    print("variants tried:", len(Vs))
    for n, f in Vs: row(n, [t for t in live if f(t)], kw, cut)
    print("--- neighbours of the vol filter (fixed thresholds, not tuned on a split) ---")
    for th in (0.012, 0.014, 0.016, 0.018, 0.020, 0.022):
        row("rvol60 > %.1f%%" % (th*100), [t for t in live if (rvol(t) or 0) > th], kw, cut)
    for lo, hi in ((0, .0135), (.0135, .0185), (.0185, 1)):
        row("rvol60 in [%.2f,%.2f)" % (lo*100, hi*100), [t for t in live if lo <= (rvol(t) or 9) < hi], kw, cut)
    for t in live: t["score_old"] = t["score"]
    r = []
    for t in live:
        u = dict(t); u["score"] = (rvol(t) or 0); r.append(u)
    row("rank by HIGH rvol first (no filter)", r, kw, cut)
    print("early (<=2023) vs late (2024+) split of rvol>median:")
    for n, f in (("early", lambda t: t["t"][:4] <= "2023"), ("late", lambda t: t["t"][:4] >= "2024")):
        row("  live " + n, [t for t in live if f(t)], kw, cut)
        row("  rvol>med " + n, [t for t in live if f(t) and (rvol(t) or 0) > V], kw, cut)
