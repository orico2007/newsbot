"""Lab run 46 (2026-11-13): Stockbee-style "4% momentum burst" continuation sleeve (web-seeded; rules are my own). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from sweep import sim, trend_ok, gate_ok
from lab_52wh import row
import lab_breadth

def signals(AS, ctx, ret=4.0, vol=1.5, clo=0.75, lo=205, cool=5):
    out = []
    for sym, A in AS.items():
        c, h, l, n = A["c"], A["h"], A["l"], len(A["c"]); cd = 0
        for i in range(lo, n - 2):
            if i < cd: continue
            r = (c[i] / c[i - 1] - 1) * 100
            if r < ret: continue
            if vol and not (A["vavg"][i] and A["v"][i] > vol * A["vavg"][i]): continue
            rg = h[i] - l[i]
            if rg <= 0 or (c[i] - l[i]) / rg < clo: continue
            if not trend_ok(A, i, "long", "s50_200") or not gate_ok(ctx, A["t"][i], "long", "spy200"): continue
            if not A["atr"][i] or A["atr"][i] / c[i] > 0.06: continue
            out.append((sym, i, r)); cd = i + cool
    return out

def trades(AS, sg, hold, stop, ex="none"):
    out = []
    for sym, i, sc in sg:
        r = sim(AS[sym], i, "long", stop, ex, hold)
        if r: r.update(sym=sym, t_exit=r["te"], score=sc, side="long", rule="burst"); out.append(r)
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    B = lab_breadth.breadth_series(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    base = [t for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    row("LIVE ref", base, kw, cut)
    V = [("burst 4%, vol1.5x, hold5", dict(ret=4), 5), ("burst 4%, vol1.5x, hold3", dict(ret=4), 3),
         ("burst 4%, vol1.5x, hold10", dict(ret=4), 10), ("burst 6%, vol1.5x, hold5", dict(ret=6), 5),
         ("burst 4%, no vol, hold5", dict(ret=4, vol=0), 5), ("burst 4%, vol2x, close-top10%, hold5", dict(ret=4, vol=2, clo=.9), 5)]
    print("variants tried:", len(V))
    for name, kk, hold in V:
        T = trades(AS, signals(AS, ctx, **kk), hold, 4.0)
        row(name, T, kw, cut)
        row("   + LIVE combined", base + T, kw, cut)
