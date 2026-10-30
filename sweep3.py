"""סבב 3: שורט - fade של מומנטום חוזר בשוק דובי (ובמניות במגמת ירידה), עם בדיקת עקביות."""
import itertools, pickle
import lab, sweep, sweep2
from sweep import *
from sweep2 import trig2, extra_ok

TRIGS_S = ["dn5pct", "r2_5", "r2_10", "r2_5&ibs_0.25", "ext_1.5atr", "ext_2.5atr", "down3_r2_20", "ll7_r2_20&ibs_0.2", "dn5pct&r2_10", "dn5pct&ibs_0.25"]
def sig_s(AS, ctx, trend, trig, gate, extra, lo=205):
    out = []
    for sym, A in AS.items():
        n = len(A["c"]); cd = 0
        for i in range(lo, n - 2):
            if i < cd: continue
            if trig2(A, i, "short", trig) and trend_ok(A, i, "short", trend) and gate_ok(ctx, A["t"][i], "short", gate) and extra_ok(A, i, extra):
                out.append((sym, i)); cd = i + 3
    return out

def main():
    AS, ctx = load_all(); rows = []
    for trend, trig, gate, extra in itertools.product(["s200", "s50_200", "none"], TRIGS_S, ["bear", "spy200"], ["none", "atrpct4", "price15", "rvol_lo", "rvol_hi"]):
        sg = sig_s(AS, ctx, trend, trig, gate, extra)
        if len(sg) < 100: continue
        for (em, hold), sk in itertools.product([("prevhl", 3), ("prevhl", 5), ("prevhl", 7), ("ma5", 7), ("ma5", 10)], [3.0, 4.0, 6.0]):
            ts = [r for r in (sim(AS[s], i, "short", sk, em, hold) for s, i in sg) if r]
            sel = [t for t in ts if t["t"] < SEAL]
            if len(sel) < 150: continue
            yrs = {y: stats(v) for y, v in per_year(sel).items() if len(v) >= 10}
            if len(yrs) < 2: continue
            rows.append({"rule": f"{trend}|{trig}|{gate}|{extra}|{em}{hold}|stop{sk}", "all": stats(sel), "years": yrs, "worst": min(s["pf"] for s in yrs.values()),
                         "seal": stats([t for t in ts if t["t"] >= SEAL])})
    pickle.dump(rows, open(lab.CACHE / "sweep3_short.pkl", "wb"))
    print(len(rows), "rules")
    for name, key in (("worst-year PF", lambda r: (-r["worst"], -r["all"]["pf"])), ("overall PF with worst>=1.0", lambda r: -r["all"]["pf"] if r["worst"] >= 1.0 else 99)):
        print(f"\n=== {name} ===")
        for r in sorted(rows, key=key)[:18]:
            a, s = r["all"], r["seal"]
            print(f"{r['rule']:62} n={a['n']:5} win={a['win']:5} pf={a['pf']:5} avg={a['avg']:6} yrs={ {y: (v['n'], v['pf']) for y, v in sorted(r['years'].items())} } | SEAL n={s['n']} pf={s['pf']}")

if __name__ == "__main__":
    main()
