import sys, itertools
import lab, sweep, sweep2, sweep3
from sweep import *
from sweep2 import trig2, extra_ok
import market

RULES = [  # (side, trend, trig, gate, extra, exit, hold, stop, score)
    ("long", "s50_200", "r2_5&ibs_0.25", "spy200", "atrpct4", "prevhl", 7, 4.0, 90),
    ("long", "s200", "ext_2.5atr", "notbear", "none", "prevhl", 7, 4.0, 70),
    ("long", "s200", "r2_5", "spy200", "none", "prevhl", 7, 4.0, 60),
    ("long", "s50_200", "r2_10", "spy200", "none", "prevhl", 7, 4.0, 50),
    ("short", "s50_200", "dn5pct&ibs_0.25", "bear", "rvol_lo", "prevhl", 5, 4.0, 80),
    ("short", "s200", "r2_5&ibs_0.25", "bear", "rvol_lo", "ma5", 7, 4.0, 75),
]

def gen(AS, ctx, rules):
    out = []
    for side, trend, trig, gate, extra, em, hold, sk, score in rules:
        for sym, i in sig2_any(AS, ctx, side, trend, trig, gate, extra):
            r = sim(AS[sym], i, side, sk, em, hold)
            if r: r.update(sym=sym, t_exit=r["te"], score=score, side=side, rule=f"{side}:{trig}:{trend}"); out.append(r)
    return out

def sig2_any(AS, ctx, side, trend, trig, gate, extra, lo=205):
    out = []
    for sym, A in AS.items():
        n = len(A["c"]); cd = 0
        for i in range(lo, n - 2):
            if i < cd: continue
            if trig2(A, i, side, trig) and trend_ok(A, i, side, trend) and gate_ok(ctx, A["t"][i], side, gate) and extra_ok(A, i, extra):
                out.append((sym, i)); cd = i + 3
    return out

def report(name, trades, **kw):
    import research
    P = lab.portfolio(trades, **kw)
    T = P["trades"]
    print(f"\n{name}: trades={P['n']} win={P['win']} PF={P['pf_pct']} avg%={P['avg_pct']} return(on 100)={P['ret_pct']} maxDD={P['mdd']}% sharpe={P['sharpe']}")
    for y in sorted({t["t"][:4] for t in T}):
        ys = [t for t in T if t["t"][:4] == y]
        s = research.stat(ys)
        print(f"   {y}: n={s['n']:4} win={s['win']:5} PF={s['pf_pct']}  avg%={s['avg_pct']}")
    return P

if __name__ == "__main__":
    AS, ctx = load_all()
    allt = gen(AS, ctx, RULES)
    longs = [t for t in allt if t["side"] == "long"]
    report("LONGS only (max 8 pos, 2/day, 8% each)", longs)
    report("LONGS+SHORTS (regime-switching)", allt)
    report("SHORTS only", [t for t in allt if t["side"] == "short"])
    bars = lab.load_bars(); spy = bars["SPY"]
    c0, c1 = next(b for b in spy if b["t"][:4] == "2021")["c"], spy[-1]["c"]
    print(f"\nSPY buy&hold 2021-01 -> now: {(c1/c0-1)*100:.0f}%")
