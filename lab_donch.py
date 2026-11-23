"""Lab run 75 (2026-11-23): Donchian (Turtle-style) long breakout sleeve, N-day-high entry / M-day-low exit, with own slots, alone and combined with LIVE (web idea: StrategyQuant Turtles transcript). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from sweep import SLIP
from lab_52wh import row
import lab_breadth, lab_sector

def mk(A, i, stop_k, M, maxhold):
    c, l, o, n = A["c"], A["l"], A["o"], len(A["c"]); atr = A["atr"][i]
    if not atr: return None
    entry = c[i] * (1 + SLIP / 100); stop = entry - stop_k * atr; last = min(n - 1, i + maxhold)
    if last <= i: return None
    px, je = None, last
    for j in range(i + 1, last + 1):
        if o[j] <= stop: px = o[j]; je = j; break
        if l[j] <= stop: px = stop; je = j; break
        if j >= M and c[j] < min(c[j - M:j]): px = c[j]; je = j; break
    if px is None: px = c[last]
    px *= 1 - SLIP / 100; pnl = (px - entry) / entry * 100
    return {"t": A["t"][i], "te": A["t"][je], "t_exit": A["t"][je], "pnl_pct": pnl, "R": pnl / (stop_k * atr / entry * 100), "held": je - i}

def trades(AS, ctx, N, M, volx=0, mom=False, stop=3.0, maxhold=60, cool=10):
    out = []
    for sym, A in AS.items():
        c, n, cd = A["c"], len(A["c"]), 0
        for i in range(260, n - 2):
            if i < cd or c[i] <= max(c[i-N:i]): continue
            if not (A["s50"][i] and A["s200"][i] and c[i] > A["s50"][i] > A["s200"][i]): continue
            if not challenger.gate2(ctx, A["t"][i], "long", "spy200"): continue
            if volx and not (A["vavg"][i] and A["v"][i] >= volx * A["vavg"][i]): continue
            if not A["atr"][i] or A["atr"][i] / c[i] > 0.06: continue
            r = mk(A, i, stop, M, maxhold)
            if r: r.update(sym=sym, side="long", rule="donch", score=(c[i] / c[i-126] - 1) * 100 if mom else 0); out.append(r); cd = i + cool
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    B = lab_breadth.breadth_series(AS); F = lab_sector.feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in PT.gen(AS, ctx, challenger.ruleset()) if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    row("LIVE vol175", live, kw, cut)
    V = [("D20/exit10", 20, 10, 0, False), ("D55/exit20", 55, 20, 0, False), ("D20/exit10 vol>=1.5x", 20, 10, 1.5, False),
         ("D55/exit20 mom-ranked", 55, 20, 0, True), ("D20/exit10 mom-ranked", 20, 10, 0, True), ("D100/exit20", 100, 20, 0, False)]
    print("variants tried:", len(V))
    for nm, N, M, vx, mo in V:
        T = trades(AS, ctx, N, M, vx, mo)
        row(nm, T, kw, cut); row("   + LIVE combined", live + T, kw, cut)
        a = [t["pnl_pct"] for t in T]
        print("   split early(<=2023) PF/n:", row("   early", [t for t in T if t["t"][:4] <= "2023"], kw, cut)["pf_pct"], " late:", row("   late", [t for t in T if t["t"][:4] >= "2024"], kw, cut)["pf_pct"])
