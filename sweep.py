"""סריקה שיטתית של חוקי כניסה/יציאה על נרות יומיים (לונג + שורט), עם עקביות לפי שנה - לא רק ממוצע כולל.
המטרה: win% גבוה ו-profit factor גבוה, באופן עקבי בכל השנים (כולל שוק דובי 2022) ובתקופה אטומה (2026)."""
import itertools, sys, pickle
from collections import defaultdict
import lab, market

SLIP = 0.05
SEAL = "2026-01-01"        # תקופה אטומה: לא משתמשים בה לבחירה

# ------------------------------------------------------------------ מערכי מאפיינים
def rsi_wilder(c, n):
    out = [None] * len(c)
    if len(c) <= n: return out
    gains = losses = 0.0
    for i in range(1, n + 1):
        d = c[i] - c[i - 1]; gains += max(d, 0); losses += max(-d, 0)
    ag, al = gains / n, losses / n
    out[n] = 100 - 100 / (1 + ag / al) if al > 0 else 100.0
    for i in range(n + 1, len(c)):
        d = c[i] - c[i - 1]
        ag = (ag * (n - 1) + max(d, 0)) / n; al = (al * (n - 1) + max(-d, 0)) / n
        out[i] = 100 - 100 / (1 + ag / al) if al > 0 else 100.0
    return out

def sma_arr(c, n):
    out = [None] * len(c); s = 0.0
    for i, x in enumerate(c):
        s += x
        if i >= n: s -= c[i - n]
        if i >= n - 1: out[i] = s / n
    return out

def build(bars):
    c = [b["c"] for b in bars]; h = [b["h"] for b in bars]; l = [b["l"] for b in bars]; o = [b["o"] for b in bars]; v = [b["v"] for b in bars]
    n = len(c); tr = [h[0] - l[0]] + [max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1])) for i in range(1, n)]
    atr = [None] * n; a = None
    for i in range(n):
        if i == 13: a = sum(tr[:14]) / 14; atr[i] = a
        elif i > 13: a = (a * 13 + tr[i]) / 14; atr[i] = a
    A = {"c": c, "h": h, "l": l, "o": o, "v": v, "t": [b["t"][:10] for b in bars], "atr": atr,
         "s5": sma_arr(c, 5), "s10": sma_arr(c, 10), "s20": sma_arr(c, 20), "s50": sma_arr(c, 50), "s200": sma_arr(c, 200),
         "r2": rsi_wilder(c, 2), "r14": rsi_wilder(c, 14), "vavg": sma_arr(v, 20)}
    A["ibs"] = [(c[i] - l[i]) / (h[i] - l[i]) if h[i] > l[i] else 0.5 for i in range(n)]
    A["ll7"] = [min(c[max(0, i - 6):i + 1]) for i in range(n)]; A["hh7"] = [max(c[max(0, i - 6):i + 1]) for i in range(n)]
    A["ret3"] = [(c[i] / c[i - 3] - 1) * 100 if i >= 3 else 0 for i in range(n)]
    return A

# ------------------------------------------------------------------ סימולציה מהירה של עסקה
def sim(A, i, side, stop_k, exit_mode, hold):
    long = side == "long"; c, h, l, o = A["c"], A["h"], A["l"], A["o"]; n = len(c)
    atr = A["atr"][i]
    if not atr: return None
    entry = c[i] * (1 + SLIP / 100 if long else 1 - SLIP / 100)
    stop = entry - stop_k * atr if long else entry + stop_k * atr
    last = min(n - 1, i + hold)
    if last <= i: return None
    px, j_exit = None, last
    for j in range(i + 1, last + 1):
        if long:
            if o[j] <= stop: px = o[j]; j_exit = j; break
            if l[j] <= stop: px = stop; j_exit = j; break
        else:
            if o[j] >= stop: px = o[j]; j_exit = j; break
            if h[j] >= stop: px = stop; j_exit = j; break
        if exit_mode == "ma5" and A["s5"][j] and ((c[j] > A["s5"][j]) if long else (c[j] < A["s5"][j])): px = c[j]; j_exit = j; break
        if exit_mode == "ma10" and A["s10"][j] and ((c[j] > A["s10"][j]) if long else (c[j] < A["s10"][j])): px = c[j]; j_exit = j; break
        if exit_mode == "prevhl" and ((c[j] > h[j - 1]) if long else (c[j] < l[j - 1])): px = c[j]; j_exit = j; break
        if exit_mode == "rsi2" and A["r2"][j] is not None and ((A["r2"][j] > 70) if long else (A["r2"][j] < 30)): px = c[j]; j_exit = j; break
    if px is None: px = c[last]
    px *= (1 - SLIP / 100 if long else 1 + SLIP / 100)
    pnl = ((px - entry) / entry if long else (entry - px) / entry) * 100
    return {"t": A["t"][i], "te": A["t"][j_exit], "pnl_pct": pnl, "R": pnl / (stop_k * atr / entry * 100), "held": j_exit - i}

# ------------------------------------------------------------------ ספריית טריגרים
def trend_ok(A, i, side, kind):
    c, s50, s200 = A["c"][i], A["s50"][i], A["s200"][i]
    if kind == "none": return s50 is not None
    if s200 is None or s50 is None: return False
    if side == "long": return c > s200 if kind == "s200" else (c > s50 > s200)
    return c < s200 if kind == "s200" else (c < s50 < s200)

def trigger(A, i, side, kind):
    r2, ibs, atr, c, s20 = A["r2"][i], A["ibs"][i], A["atr"][i], A["c"][i], A["s20"][i]
    if r2 is None or not atr or s20 is None: return False
    long = side == "long"
    if kind.startswith("r2_"):
        x = float(kind[3:]); return r2 < x if long else r2 > 100 - x
    if kind.startswith("ibs_"):
        x = float(kind[4:]); return ibs < x if long else ibs > 1 - x
    if kind == "down3_r2_20":
        return (c < A["c"][i - 1] < A["c"][i - 2] < A["c"][i - 3] and r2 < 20) if long else (c > A["c"][i - 1] > A["c"][i - 2] > A["c"][i - 3] and r2 > 80)
    if kind.startswith("ext_"):
        k = float(kind[4:-3]); return c < s20 - k * atr if long else c > s20 + k * atr
    if kind == "ll7_r2_20": return (c <= A["ll7"][i] and r2 < 20) if long else (c >= A["hh7"][i] and r2 > 80)
    if kind == "dn5pct": return A["ret3"][i] < -5 if long else A["ret3"][i] > 5
    return False

def gate_ok(ctx, d, side, kind):
    if kind == "none": return True
    reg = ctx["reg"].get(d, "neutral"); a200 = ctx["a200"].get(d, True)
    if side == "long": return a200 if kind == "spy200" else (reg != "bear" if kind == "notbear" else reg == "bull")
    return (not a200) if kind == "spy200" else (reg == "bear" if kind == "bear" else reg != "bull")

LONG_TRENDS = ["s200", "s50_200"]; SHORT_TRENDS = ["s200", "s50_200", "none"]
TRIGS = ["r2_5", "r2_10", "r2_15", "ibs_0.1", "ibs_0.2", "down3_r2_20", "ext_1.5atr", "ext_2.5atr", "ll7_r2_20", "dn5pct"]
GATES_L = ["none", "spy200", "notbear"]; GATES_S = ["none", "spy200", "bear"]
EXITS = [("ma5", 7), ("ma5", 10), ("prevhl", 7), ("rsi2", 7), ("ma10", 12)]
STOPS = [2.0, 3.0, 4.0]

def signals(AS, ctx, side, trend, trig, gate, lo=205):
    out = []
    for sym, A in AS.items():
        n = len(A["c"]); cd = 0
        for i in range(lo, n - 2):
            if i < cd: continue
            if trigger(A, i, side, trig) and trend_ok(A, i, side, trend) and gate_ok(ctx, A["t"][i], side, gate):
                out.append((sym, i)); cd = i + 3
    return out

def pf(ts):
    w = sum(t["pnl_pct"] for t in ts if t["pnl_pct"] > 0); l = -sum(t["pnl_pct"] for t in ts if t["pnl_pct"] <= 0)
    return round(w / l, 2) if l > 0 else (99.0 if w > 0 else 0.0)

def stats(ts):
    if not ts: return {"n": 0, "win": 0, "pf": 0, "avg": 0}
    return {"n": len(ts), "win": round(100 * sum(1 for t in ts if t["pnl_pct"] > 0) / len(ts), 1), "pf": pf(ts), "avg": round(sum(t["pnl_pct"] for t in ts) / len(ts), 3)}

def per_year(ts):
    d = defaultdict(list)
    for t in ts: d[t["t"][:4]].append(t)
    return d

def run(side, AS, ctx, min_n=250):
    rows = []
    trends, gates = (LONG_TRENDS, GATES_L) if side == "long" else (SHORT_TRENDS, GATES_S)
    for trend, trig, gate in itertools.product(trends, TRIGS, gates):
        sg = signals(AS, ctx, side, trend, trig, gate)
        if len(sg) < 60: continue
        for (em, hold), sk in itertools.product(EXITS, STOPS):
            ts = [r for r in (sim(AS[s], i, side, sk, em, hold) for s, i in sg) if r]
            sel = [t for t in ts if t["t"] < SEAL]
            if len(sel) < min_n: continue
            yrs = {y: stats(v) for y, v in per_year(sel).items() if len(v) >= 8}
            good = sum(1 for s in yrs.values() if s["pf"] >= 1.1)
            rows.append({"rule": f"{side}|{trend}|{trig}|{gate}|{em}{hold}|stop{sk}", "all": stats(sel), "years": yrs, "good": good, "ny": len(yrs),
                         "seal": stats([t for t in ts if t["t"] >= SEAL])})
    return rows

def load_all():
    bars = lab.load_bars()
    uni = [s for s in bars if s not in market.SECTORS and s not in ("SPY", "QQQ", "IWM", "DIA", "VIXY")]
    AS = {s: build(bars[s]) for s in uni if len(bars[s]) > 260}
    spy = bars["SPY"]
    ctx = {"reg": lab.spy_regime_series(spy), "a200": lab.sma_flags(spy, 200)}
    return AS, ctx

def show(rows, side, k=25):
    rows = sorted(rows, key=lambda r: (-(r["good"] / max(1, r["ny"])), -r["all"]["pf"]))
    print(f"\n=== {side}: {len(rows)} rules; top by year-consistency ===")
    for r in rows[:k]:
        a, s = r["all"], r["seal"]
        print(f"{r['rule']:58} n={a['n']:5} win={a['win']:5} pf={a['pf']:5} avg={a['avg']:6} yrs {r['good']}/{r['ny']} | SEAL n={s['n']} win={s['win']} pf={s['pf']}")

def main():
    AS, ctx = load_all()
    for side in ("long", "short"):
        rows = run(side, AS, ctx)
        pickle.dump(rows, open(lab.CACHE / f"sweep_{side}.pkl", "wb"))
        show(rows, side)

if __name__ == "__main__":
    main()
