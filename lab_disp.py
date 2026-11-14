"""Lab run 51 (2026-11-14): cross-sectional dispersion (stdev of 1d returns across the universe) and 5d dispersion trend as conditioner of the LIVE setup (own idea; lab_disp.py). Backtest only."""
import datetime, statistics
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    B = lab_breadth.breadth_series(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    raw = lab.load_bars(); R = {}
    for s, bars in raw.items():
        if s not in AS: continue
        for i in range(1, len(bars)):
            R.setdefault(bars[i]["t"][:10], []).append(bars[i]["c"] / bars[i-1]["c"] - 1)
    D = {d: statistics.pstdev(v) * 100 for d, v in R.items() if len(v) >= 30}
    ds = sorted(D); rank = {}
    for i, d in enumerate(ds):  # trailing 250d percentile (no look-ahead)
        w = [D[x] for x in ds[max(0, i-250):i]]
        rank[d] = sum(1 for x in w if x < D[d]) / len(w) if len(w) >= 60 else None
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    base = [t for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    for t in base: t["_r"] = rank.get(t["t"][:10])
    V = [("LIVE ref", lambda r: True), ("dispersion pct >= 0.5", lambda r: r is not None and r >= .5),
         ("dispersion pct < 0.5", lambda r: r is not None and r < .5),
         ("dispersion pct >= 0.8", lambda r: r is not None and r >= .8),
         ("dispersion pct < 0.8", lambda r: r is not None and r < .8)]
    print("variants tried:", len(V) - 1, "| signals with rank:", sum(1 for t in base if t["_r"] is not None), "of", len(base))
    for n, f in V: row(n, [t for t in base if f(t["_r"])], kw, cut)
