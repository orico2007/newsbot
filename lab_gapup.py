"""Lab run 26: gap-up continuation sleeve (earnings-gap / runaway-gap drift proxy; web idea). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from sweep import sim, trend_ok
from lab_52wh import row

def signals(AS, ctx, gmin, volx, ibs_min=0.6, hv=False, cool=10):
    out = []
    for sym, A in AS.items():
        c, o, n = A["c"], A["o"], len(A["c"]); cd = 0
        for i in range(260, n - 2):
            if i < cd: continue
            gap = (o[i] / c[i-1] - 1) * 100
            if gap < gmin or c[i] <= o[i] or A["ibs"][i] < ibs_min: continue
            if not (A["vavg"][i] and A["v"][i] >= volx * A["vavg"][i]): continue
            if not trend_ok(A, i, "long", "s50_200") or not challenger.gate2(ctx, A["t"][i], "long", "spy200"): continue
            if not A["atr"][i] or A["atr"][i] / c[i] > 0.08: continue
            if hv:
                v = challenger.vol60(A, i)
                if v is None or v < 1.75: continue
            out.append((sym, i, gap)); cd = i + cool
    return out

def trades(AS, sg, hold, stop=4.0, ex="none"):
    out = []
    for sym, i, sc in sg:
        r = sim(AS[sym], i, "long", stop, ex, hold)
        if r: r.update(sym=sym, t_exit=r["te"], score=sc, side="long", rule="gapup"); out.append(r)
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset())
    import lab_breadth, lab_sector
    B = lab_breadth.breadth_series(AS); F = lab_sector.feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in champ if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    row("LIVE vol175 champion", live, kw, cut)
    V = [("gap>=3% vol>=2x h10", 3, 2, 10, False), ("gap>=3% vol>=2x h20", 3, 2, 20, False),
         ("gap>=5% vol>=2x h10", 5, 2, 10, False), ("gap>=2% vol>=1.5x h10", 2, 1.5, 10, False),
         ("gap>=3% vol>=2x h10 +vol60", 3, 2, 10, True), ("gap>=5% vol>=2x h20", 5, 2, 20, False)]
    print("variants tried:", len(V))
    for name, g, vx, h, hvf in V:
        T = trades(AS, signals(AS, ctx, g, vx, hv=hvf), h)
        row(name, T, kw, cut)
        row("   + LIVE combined", live + T, kw, cut)
