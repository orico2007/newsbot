"""Lab run 15 (web idea: PEAD, TradingView/StockSharp open PEAD strategies; unverified): post-earnings-drift PROXY from daily bars.
Earnings dates are not available offline, so an 'earnings-like' day = big gap + volume spike. Long continuation after gap-up (drift) and
gap-down reversal; standalone sleeve and combined with the NEW live setup. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from sweep import sim
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def signals(AS, ctx, gmin, vmult, up=True, need_ibs=None, gate=True, cool=10):
    out = []
    for sym, A in AS.items():
        c, o, v, n = A["c"], A["o"], A["v"], len(A["c"]); cd = 0
        for i in range(205, n - 2):
            if i < cd or not A["vavg"][i] or not A["atr"][i]: continue
            if gate and not challenger.gate2(ctx, A["t"][i], "long", "spy200"): continue
            if A["atr"][i] / c[i] > 0.09: continue
            gap = (o[i] / c[i-1] - 1) * 100
            if v[i] < vmult * A["vavg"][i]: continue
            if up:
                if gap < gmin or c[i] <= o[i]: continue
            else:
                if gap > -gmin or c[i] <= o[i]: continue
            if need_ibs is not None and A["ibs"][i] < need_ibs: continue
            out.append((sym, i, abs(gap))); cd = i + cool
    return out

def trades(AS, sg, hold, exit_, stop=4.0):
    out = []
    for sym, i, sc in sg:
        r = sim(AS[sym], i, "long", stop, exit_, hold)
        if r: r.update(sym=sym, t_exit=r["te"], score=sc, side="long", rule="pead"); out.append(r)
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    B = breadth_series(AS); F = feats(AS)
    T = PT.gen(AS, ctx, challenger.ruleset()); live = []
    for t in T:
        if B.get(t["t"][:10], (0, 0))[0] < .10: continue
        f = F.get((t["sym"], t["t"])); live.append(dict(t, score=-f["m3"]) if f else t)
    row("LIVE (breadth+rank)", live, kw, cut)
    V = [("gap-up>=5% vol>=3x close>open h10", dict(gmin=5, vmult=3), 10, "none"),
         ("gap-up>=5% vol>=3x h20", dict(gmin=5, vmult=3), 20, "none"),
         ("gap-up>=8% vol>=3x h20", dict(gmin=8, vmult=3), 20, "none"),
         ("gap-up>=5% vol>=3x IBS>.7 h10", dict(gmin=5, vmult=3, need_ibs=.7), 10, "none"),
         ("gap-up>=5% vol>=3x h10 no SPY gate", dict(gmin=5, vmult=3, gate=False), 10, "none"),
         ("gap-down<=-5% vol>=3x recover h7 prevhl", dict(gmin=5, vmult=3, up=False), 7, "prevhl")]
    print("variants tried:", len(V))
    for name, k, h, ex in V:
        S = trades(AS, signals(AS, ctx, **k), h, ex)
        row(name, S, kw, cut)
        row("   + live combined", live + S, kw, cut)
