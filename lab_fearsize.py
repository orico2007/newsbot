"""Lab run 10 (2026-11-06): SPY-dip as a SIZE tier (not a filter) on champion trades. Post-hoc scaling of taken champion trades; backtest only."""
import datetime, statistics
from collections import defaultdict
import lab, sweep, challenger, research
import portfolio_test as PT
from lab_fear import spy_feats

def curve(taken, mult):
    eq = 100.0; peak = eq; mdd = 0; mon = defaultdict(float); ys = defaultdict(lambda: [0.0, 0.0])
    for t in sorted(taken, key=lambda t: t["t_exit"]):
        w = 10 * mult(t) / 100; r = w * t["pnl_pct"] / 100
        eq *= 1 + r; peak = max(peak, eq); mdd = max(mdd, (peak - eq) / peak * 100); mon[t["t_exit"][:7]] += r * 100
        ys[t["t"][:4]][0 if r > 0 else 1] += abs(r)
    ms = list(mon.values()); sh = statistics.mean(ms) / statistics.pstdev(ms) * 12 ** .5
    pf = {y: round(g / l, 2) if l else None for y, (g, l) in sorted(ys.items())}
    return round(eq - 100, 1), round(mdd, 1), round(sh, 2), pf

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); F = spy_feats()
    taken = lab.portfolio(champ, **kw)["trades"]
    dip = lambda t: F.get(t["t"][:10], (0, 0, 0))[1] < -1.0
    for name, m in [("CHAMPION flat", lambda t: 1), ("1.5x on SPY3d<-1%, 1x else", lambda t: 1.5 if dip(t) else 1),
                    ("1.5x dip, 0.75x else", lambda t: 1.5 if dip(t) else .75), ("1.3x dip only", lambda t: 1.3 if dip(t) else 1)]:
        print(f"{name:30}", curve(taken, m))
    print("n dip trades", sum(dip(t) for t in taken), "of", len(taken))
    # early/late split
    for lo, hi in [("2021","2023"),("2024","2026")]:
        s = [t for t in taken if lo <= t["t"][:4] <= hi]
        print(lo, hi, "flat", curve(s, lambda t: 1)[:3], "1.5/.75", curve(s, lambda t: 1.5 if dip(t) else .75)[:3])
