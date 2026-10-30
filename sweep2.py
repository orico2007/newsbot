"""סבב 2: חידוד לונג mean-reversion (טריגרים משולבים, מסננים, יציאות) עם דרישת עקביות בכל שנה כולל 2022."""
import itertools, pickle, sys
import lab, sweep
from sweep import *

def trig2(A, i, side, kind):
    return all(trigger(A, i, side, k) for k in kind.split("&"))

def extra_ok(A, i, kind):
    c, atr, v, va = A["c"][i], A["atr"][i], A["v"][i], A["vavg"][i]
    if kind == "none": return True
    if kind == "atrpct4": return atr / c * 100 < 4
    if kind == "nocrash": return A["ret3"][i] > -12
    if kind == "rvol_lo": return bool(va) and v / va < 1.2
    if kind == "rvol_hi": return bool(va) and v / va >= 1.2
    if kind == "price15": return c >= 15
    return True

TRIGS2 = ["r2_5", "r2_10", "r2_5&ibs_0.25", "r2_10&ext_1.5atr", "r2_5&dn5pct", "ext_2.5atr", "ext_2.0atr&r2_15", "ll7_r2_20&ibs_0.2", "down3_r2_20"]
EXTRAS = ["none", "atrpct4", "nocrash", "rvol_lo", "rvol_hi", "price15"]
EX2 = [("prevhl", 3), ("prevhl", 5), ("prevhl", 7), ("prevhl", 10), ("ma5", 7)]
ST2 = [3.0, 4.0, 6.0]

def sig2(AS, ctx, side, trend, trig, gate, extra, lo=205):
    out = []
    for sym, A in AS.items():
        n = len(A["c"]); cd = 0
        for i in range(lo, n - 2):
            if i < cd: continue
            if trig2(A, i, side, trig) and trend_ok(A, i, side, trend) and gate_ok(ctx, A["t"][i], side, gate) and extra_ok(A, i, extra):
                out.append((sym, i)); cd = i + 3
    return out

def main():
    AS, ctx = load_all(); rows = []
    for trend, trig, gate, extra in itertools.product(["s200", "s50_200"], TRIGS2, ["spy200", "notbear"], EXTRAS):
        sg = sig2(AS, ctx, "long", trend, trig, gate, extra)
        if len(sg) < 120: continue
        for (em, hold), sk in itertools.product(EX2, ST2):
            ts = [r for r in (sim(AS[s], i, "long", sk, em, hold) for s, i in sg) if r]
            sel = [t for t in ts if t["t"] < SEAL]
            if len(sel) < 300: continue
            yrs = {y: stats(v) for y, v in per_year(sel).items() if len(v) >= 15}
            if len(yrs) < 4: continue
            worst = min(s["pf"] for s in yrs.values())
            rows.append({"rule": f"{trend}|{trig}|{gate}|{extra}|{em}{hold}|stop{sk}", "all": stats(sel), "years": yrs, "worst": worst, "seal": stats([t for t in ts if t["t"] >= SEAL])})
    pickle.dump(rows, open(lab.CACHE / "sweep2_long.pkl", "wb"))
    print(len(rows), "rules")
    for name, key in (("by worst-year PF", lambda r: (-r["worst"], -r["all"]["pf"])), ("by overall PF (worst>=0.95)", lambda r: -r["all"]["pf"] if r["worst"] >= 0.95 else 99)):
        print(f"\n=== {name} ===")
        for r in sorted(rows, key=key)[:22]:
            a, s = r["all"], r["seal"]
            print(f"{r['rule']:62} n={a['n']:5} win={a['win']:5} pf={a['pf']:5} avg={a['avg']:6} worstyr={r['worst']:5} | SEAL n={s['n']} win={s['win']} pf={s['pf']}")

if __name__ == "__main__":
    main()
