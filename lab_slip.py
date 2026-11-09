"""Lab run 11 (2026-11-09): execution-cost / stop-gap slippage stress on LIVE vs vol60>=1.75% candidate. Backtest only."""
import datetime, math
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); bars = lab.load_bars(); spy = bars["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); B = breadth_series(AS); F = feats(AS)
    m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    def vol(t):
        A = AS[t["sym"]]; i = IX[t["sym"]].get(t["t"][:10])
        if i is None or i < 70: return None
        rs = [A["c"][j]/A["c"][j-1]-1 for j in range(i-59, i+1)]
        m = sum(rs)/60; return math.sqrt(sum((x-m)**2 for x in rs)/59)*100
    live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            u = dict(t); u["score"] = -m3(t); u["_v"] = vol(t); live.append(u)
    live = [t for t in live if t["_v"] is not None]
    hv = [t for t in live if t["_v"] >= 1.75]
    print("SLIP base:", sweep.SLIP)
    stops = [t for t in hv if t["R"] <= -0.99]; print("hv trades", len(hv), "stop-outs", len(stops), "of which gap beyond stop (R<-1.15):", sum(t["R"] < -1.15 for t in hv))
    ls = [t for t in live if t["R"] <= -0.99]; print("live trades", len(live), "stop-outs", len(ls), "gap:", sum(t["R"] < -1.15 for t in live))
    n = 0
    for rt, sp in ((0,0),(0.1,0),(0.2,0),(0.4,0),(0,1),(0,2),(0.2,1),(0.4,2)):
        for nm, S in (("LIVE", live), ("vol>=1.75", hv)):
            T = []
            for t in S:
                u = dict(t); u["pnl_pct"] = t["pnl_pct"] - rt - (sp if t["R"] <= -0.99 else 0); T.append(u)
            row(f"{nm} extra rt {rt}% stop {sp}%", T, kw, cut); n += 1
    # 15x8 sizing under heavy stress
    T = [dict(t, pnl_pct=t["pnl_pct"] - 0.4 - (2 if t["R"] <= -0.99 else 0)) for t in hv]
    row("vol>=1.75 15x8 rt0.4 stop2", T, dict(size_pct=15, max_pos=8, per_day=4), cut)
    print("variants:", n + 1)
