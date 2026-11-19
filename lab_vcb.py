"""Lab run 52: volatility-contraction Donchian-20 breakout continuation sleeve (web: Donchian/turtle breakout pages; Minervini-style VCP proxy). Long-only, daily bars, same simulator. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
import lab_breadth, lab_sector
from lab_52wh import row
from sweep import sim, trend_ok, gate_ok

def signals(AS, ctx, n=20, contr=None, volx=0, hold=10, rsmin=None, lo=260, cool=10):
    out = []
    for sym, A in AS.items():
        if sym == "SPY": continue
        c, h, l, atr = A["c"], A["h"], A["l"], A["atr"]; cd = 0
        for i in range(lo, len(c) - 2):
            if i < cd or not atr[i]: continue
            if c[i] <= max(h[i-n:i]): continue
            if not trend_ok(A, i, "long", "s50_200") or not gate_ok(ctx, A["t"][i], "long", "spy200"): continue
            if atr[i] / c[i] > 0.06: continue
            if contr is not None:   # prior 10-day avg range vs prior 60-day avg range (contraction)
                r10 = sum(h[j]-l[j] for j in range(i-10, i)) / 10; r60 = sum(h[j]-l[j] for j in range(i-60, i)) / 60
                if r10 > contr * r60: continue
            if volx and not (A["vavg"][i] and A["v"][i] > volx * A["vavg"][i]): continue
            rs = (c[i] / c[i-126] - 1) * 100
            if rsmin is not None and rs < rsmin: continue
            out.append((sym, i, rs)); cd = i + cool
    return out

def trades(AS, sg, hold, stop=4.0):
    out = []
    for sym, i, rs in sg:
        r = sim(AS[sym], i, "long", stop, "none", hold)
        if r: r.update(sym=sym, t_exit=r["te"], score=rs, side="long", rule="vcb"); out.append(r)
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; lastd = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(lastd) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = challenger.DEF_PORT
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    B = lab_breadth.breadth_series(AS); F = lab_sector.feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    print("data through", lastd); row("LIVE vol175", live, kw, cut)
    V = [("D20 breakout, hold10", dict(), 10),
         ("D20 + contraction r10<=0.8*r60, hold10", dict(contr=0.8), 10),
         ("D20 + contraction + vol>1.5x, hold10", dict(contr=0.8, volx=1.5), 10),
         ("D20 + contraction + 6m RS>=20%, hold10", dict(contr=0.8, rsmin=20), 10),
         ("D20 + contraction, hold 20", dict(contr=0.8), 20)]
    print("variants tried:", len(V))
    for nme, k, hold in V:
        T = trades(AS, signals(AS, ctx, **k), hold)
        row(nme, T, kw, cut); row("   + live combined", live + T, kw, cut)
