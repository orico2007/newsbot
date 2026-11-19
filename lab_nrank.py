"""Lab run 50: cross-sectional vol-normalised return reversal (Quantpedia 'Liquidity Creation in Short-Term Reversal Strategies and Volatility Risk', daily bottom-decile by return/rolling-std) as a long-only sleeve, +/- combined with the LIVE setup. Backtest only."""
import datetime, statistics
import lab, sweep, challenger
import portfolio_test as PT
import lab_breadth, lab_sector
from lab_52wh import row
from sweep import sim, trend_ok, gate_ok

def sleeve(AS, ctx, B, lb, k, hold, exit_, trend, vmin, bgate, lo=205):
    byday = {}
    for sym, A in AS.items():
        if sym == "SPY": continue
        c = A["c"]
        for i in range(max(lo, 61), len(c) - 2):
            d = A["t"][i]
            if not gate_ok(ctx, d, "long", "spy200"): continue
            if bgate and B.get(d, (0, 0))[0] < 0.10: continue
            if trend and not trend_ok(A, i, "long", "s50_200"): continue
            r = [c[j] / c[j-1] - 1 for j in range(i-59, i+1)]
            sd = statistics.pstdev(r)
            if sd * 100 < vmin or not sd: continue
            z = (c[i] / c[i-lb] - 1) / (sd * lb ** 0.5)
            byday.setdefault(d, []).append((z, sym, i))
    out = []; last = {}
    for d in sorted(byday):
        pick = sorted(byday[d])[:k]
        for z, sym, i in pick:
            if i < last.get(sym, -99): continue
            r = sim(AS[sym], i, "long", 4.0, exit_, hold)
            if r:
                r.update(sym=sym, t_exit=r["te"], score=-z, side="long", rule="nrank"); out.append(r); last[sym] = i + 5
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
    V = [("z5 bottom3 hold5 time, trend, vol1.75, breadth", dict(lb=5, k=3, hold=5, exit_="none", trend=True, vmin=1.75, bgate=True)),
         ("z5 bottom3 hold7 prevhl, trend, vol1.75, breadth", dict(lb=5, k=3, hold=7, exit_="prevhl", trend=True, vmin=1.75, bgate=True)),
         ("z1 bottom3 hold3 time, trend, vol1.75, breadth", dict(lb=1, k=3, hold=3, exit_="none", trend=True, vmin=1.75, bgate=True)),
         ("z5 bottom3 hold5 time, NO trend, vol1.75, breadth", dict(lb=5, k=3, hold=5, exit_="none", trend=False, vmin=1.75, bgate=True)),
         ("z5 bottom3 hold5 time, trend, vol1.75, no breadth", dict(lb=5, k=3, hold=5, exit_="none", trend=True, vmin=1.75, bgate=False)),
         ("z5 bottom6 hold5 time, trend, vol1.0, breadth", dict(lb=5, k=6, hold=5, exit_="none", trend=True, vmin=1.0, bgate=True))]
    print("variants tried:", len(V))
    for n, k in V:
        T = sleeve(AS, ctx, B, **k)
        row(n, T, kw, cut); row("   + live combined", live + T, kw, cut)
