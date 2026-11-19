"""Lab run 54: slow-oscillator trend-pullback sleeve (RSI14 oversold inside a stock uptrend; web: quantifiedstrategies RSI pullback page). Long-only, daily bars, same simulator. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
import lab_breadth, lab_sector
from lab_52wh import row
from sweep import sim, trend_ok, gate_ok

def signals(AS, ctx, rmax=40, pb=None, lo=260, cool=10, vmin=None):
    out = []
    for sym, A in AS.items():
        if sym == "SPY": continue
        c, h, atr, r14 = A["c"], A["h"], A["atr"], A["r14"]; cd = 0
        for i in range(lo, len(c) - 2):
            if i < cd or not atr[i] or r14[i] is None: continue
            if r14[i] >= rmax: continue
            if not trend_ok(A, i, "long", "s50_200") or not gate_ok(ctx, A["t"][i], "long", "spy200"): continue
            if atr[i] / c[i] > 0.06: continue
            if pb is not None and c[i] > (1 - pb) * max(h[i-20:i]): continue
            if vmin is not None:
                v = challenger.vol60(A, i)
                if v is None or v < vmin: continue
            out.append((sym, i, 100 - r14[i])); cd = i + cool
    return out

def trades(AS, sg, hold, stop=4.0):
    out = []
    for sym, i, rs in sg:
        r = sim(AS[sym], i, "long", stop, "none", hold)
        if r: r.update(sym=sym, t_exit=r["te"], score=rs, side="long", rule="pb14"); out.append(r)
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
    V = [("RSI14<40 pullback, hold10", dict(), 10),
         ("RSI14<35, hold10", dict(rmax=35), 10),
         ("RSI14<35 + 8% off 20d high, hold10", dict(rmax=35, pb=0.08), 10),
         ("RSI14<35, hold5", dict(rmax=35), 5),
         ("RSI14<40 + vol60>=1.75, hold10", dict(vmin=1.75), 10),
         ("RSI14<45 + 8% off 20d high, hold10", dict(rmax=45, pb=0.08), 10),
         ("RSI14<50 + 10% off 20d high, hold10", dict(rmax=50, pb=0.10), 10)]
    print("variants tried:", len(V))
    for nme, k, hold in V:
        T = trades(AS, signals(AS, ctx, **k), hold)
        if len(T) < 5: print(nme, "n=", len(T), "too few"); continue
        row(nme, T, kw, cut); row("   + live combined", live + T, kw, cut)
