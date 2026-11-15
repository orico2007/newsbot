"""Lab run 28: capitulation-bar reversion sleeve (large ATR-sized down day + volume spike), web-seeded. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from sweep import sim, trend_ok
from lab_52wh import row

def signals(AS, ctx, atrx, volx, ibs_max=1.0, hv=False, cool=5):
    out = []
    for sym, A in AS.items():
        c, n = A["c"], len(A["c"]); cd = 0
        for i in range(260, n - 2):
            if i < cd or not A["atr"][i]: continue
            drop = (c[i-1] - c[i]) / A["atr"][i]
            if drop < atrx or A["ibs"][i] > ibs_max: continue
            if volx and not (A["vavg"][i] and A["v"][i] >= volx * A["vavg"][i]): continue
            if c[i] <= A["sma200"][i] if "sma200" in A else not trend_ok(A, i, "long", "s50_200"): continue
            if not challenger.gate2(ctx, A["t"][i], "long", "spy200"): continue
            if A["atr"][i] / c[i] > 0.09: continue
            if hv:
                v = challenger.vol60(A, i)
                if v is None or v < 1.75: continue
            out.append((sym, i, drop)); cd = i + cool
    return out

def trades(AS, sg, hold=7, stop=4.0, ex="prevhl"):
    out = []
    for sym, i, sc in sg:
        r = sim(AS[sym], i, "long", stop, ex, hold)
        if r: r.update(sym=sym, t_exit=r["te"], score=sc, side="long", rule="climax"); out.append(r)
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
    V = [("drop>=2ATR vol>=2x", 2, 2, 1.0, False), ("drop>=3ATR vol>=2x", 3, 2, 1.0, False),
         ("drop>=2ATR vol>=2x ibs<=.2", 2, 2, .2, False), ("drop>=2ATR no vol", 2, 0, 1.0, False),
         ("drop>=3ATR vol>=2x +vol60", 3, 2, 1.0, True), ("drop>=2ATR vol>=3x", 2, 3, 1.0, False)]
    print("variants tried:", len(V))
    for name, a, vx, ib, h in V:
        T = trades(AS, signals(AS, ctx, a, vx, ib, h))
        row(name, T, kw, cut)
        row("   + LIVE combined", live + T, kw, cut)
