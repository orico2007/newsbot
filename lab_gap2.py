"""Lab run 7 (2026-11-09): gap-recover sleeve on top of the LIVE setup (breadth>=10% + weakest-peer rank). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats
import lab_gap

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    B = breadth_series(AS); F = feats(AS)
    m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    okb = lambda t: B.get(t["t"][:10], (0, 0))[0] >= .10
    def live_(T, lowprio=0):
        out = []
        for t in T:
            if okb(t):
                u = dict(t); u["score"] = -m3(t) - lowprio; out.append(u)
        return out
    champ = live_(PT.gen(AS, ctx, challenger.ruleset()))
    row("LIVE champion", champ, kw, cut)
    V = []
    for k, nm in (("gap2_recover", "gap<-2% & close>open"), ("gap3_recover", "gap<-3% & close>open"), ("gap1_recover", "gap<-1% & close>open")):
        S = lab_gap.trades(AS, lab_gap.signals(AS, ctx, k), 7, "prevhl")
        V.append((nm + " (breadth-gated, ranked)", live_(S)))
        V.append((nm + " (gated, ranked AFTER rule signals)", live_(S, 1000)))
    print("variants tried:", len(V))
    for nm, S in V:
        row(nm + " alone", S, kw, cut)
        row("   + live combined", champ + S, kw, cut)
