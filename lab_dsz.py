"""Lab run 52 (2026-11-14): dispersion size tilt (follow-up of run 51) and prior-21d-return conditioning of the LIVE setup (web-inspired: Alpha Architect / CFA FAJ 2024 liquidity-provision reversal notes, unverified). Backtest only. Size tilt emulated by scaling pnl_pct (PF size-weighted)."""
import datetime, statistics, copy
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
    for i, d in enumerate(ds):
        w = [D[x] for x in ds[max(0, i-250):i]]
        rank[d] = sum(1 for x in w if x < D[d]) / len(w) if len(w) >= 60 else None
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    base = [t for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    for t in base:
        d = t["t"][:10]; t["_r"] = rank.get(d)
        i = IX[t["sym"]].get(d); c = AS[t["sym"]]["c"]
        t["_m21"] = (c[i] / c[i-21] - 1) * 100 if i and i >= 21 else None
    def tilt(hi, lo):
        out = []
        for t in base:
            u = dict(t); r = t["_r"]; f = hi if (r is not None and r >= .5) else lo
            u["pnl_pct"] = t["pnl_pct"] * f; out.append(u)
        return out
    print("variants tried: 6 (3 tilts, 3 m21 splits)")
    row("LIVE ref", base, kw, cut)
    row("tilt 1.5x if disp>=.5 else 0.75x", tilt(1.5, .75), kw, cut)
    row("tilt 1.25x if disp>=.5 else 0.75x", tilt(1.25, .75), kw, cut)
    row("tilt 1.5x if disp>=.5 else 1.0x", tilt(1.5, 1.0), kw, cut)
    row("prior 21d ret < -10%", [t for t in base if t["_m21"] is not None and t["_m21"] < -10], kw, cut)
    row("prior 21d ret >= -10%", [t for t in base if t["_m21"] is not None and t["_m21"] >= -10], kw, cut)
    row("prior 21d ret >= 0%", [t for t in base if t["_m21"] is not None and t["_m21"] >= 0], kw, cut)
