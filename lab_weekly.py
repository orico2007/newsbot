"""Lab run 34 (2026-11-12): weekly short-term reversal sleeve (buy last-week losers on the last session of the week, hold ~5 sessions).
Web-seeded (QuantConnect/Quantpedia short-term reversal, unverified); rules my own. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from sweep import sim, trend_ok, gate_ok
from lab_52wh import row
import lab_breadth

def weekly_signals(AS, ctx, minret=-5.0, vol=1.75, trend=True, lo=260):
    out = []
    for sym, A in AS.items():
        c, t, n = A["c"], A["t"], len(A["c"])
        for i in range(lo, n - 2):
            d0 = datetime.date.fromisoformat(t[i][:10]); d1 = datetime.date.fromisoformat(t[i+1][:10])
            if d0.isocalendar()[1] == d1.isocalendar()[1]: continue   # only last session of a week
            if trend and not trend_ok(A, i, "long", "s50_200"): continue
            if not gate_ok(ctx, t[i], "long", "spy200"): continue
            v = challenger.vol60(A, i)
            if vol and (v is None or v < vol): continue
            if not A["atr"][i] or A["atr"][i] / c[i] > 0.08: continue
            r5 = (c[i] / c[i-5] - 1) * 100
            if r5 > minret: continue
            out.append((sym, i, -r5))
    return out

def trades(AS, sg, hold, stop):
    out = []
    for sym, i, sc in sg:
        r = sim(AS[sym], i, "long", stop, "none", hold)
        if r: r.update(sym=sym, t_exit=r["te"], score=sc, side="long", rule="weekly"); out.append(r)
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    B = lab_breadth.breadth_series(AS)
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [t for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    row("LIVE (vol60>=1.75, breadth>=10%)", live, kw, cut)
    V = [("wk r5<=-5%, vol60>=1.75, hold5 stop4", dict(), 5, 4.0),
         ("wk r5<=-8%, vol60>=1.75, hold5", dict(minret=-8.0), 5, 4.0),
         ("wk r5<=-5%, no vol filter, hold5", dict(vol=0), 5, 4.0),
         ("wk r5<=-5%, vol60>=1.75, no trend, hold5", dict(trend=False), 5, 4.0),
         ("wk r5<=-5%, vol60>=1.75, hold10", dict(), 10, 4.0)]
    print("variants tried:", len(V))
    for name, k, hold, stop in V:
        T = trades(AS, weekly_signals(AS, ctx, **k), hold, stop)
        row(name, T, kw, cut)
        row("   + live combined", live + T, kw, cut)
