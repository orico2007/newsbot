"""Lab run 77 (2026-11-23): Heston-Sadka same-calendar-month stock seasonality (web: https://www.nber.org/papers/w20815).
(a) monthly sleeve: long top/bottom quintile by mean return in the same calendar month of prior years; (b) tercile conditioner on live vol60+zreg setup. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from sweep import sim, trend_ok
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats
from lab_zscore import zreg

def month_rets(A):
    """{(year,month): return} using last close of month vs last close of previous month."""
    last = {}
    for i, d in enumerate(A["t"]): last[d[:7]] = i
    keys = sorted(last); out = {}
    for a, b in zip(keys, keys[1:]):
        out[b] = A["c"][last[b]] / A["c"][last[a]] - 1
    return out

def seas(MR, ym, minn=2):
    y, m = int(ym[:4]), ym[5:]
    v = [MR[f"{yy}-{m}"] for yy in range(2018, y) if f"{yy}-{m}" in MR]
    return sum(v) / len(v) if len(v) >= minn else None

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(spy) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    MR = {s: month_rets(A) for s, A in AS.items()}
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    B = breadth_series(AS); F = feats(AS)
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(t["t"][:10]); v = challenger.vol60(AS[t["sym"]], i)
            if v is not None and v >= 1.75 and i is not None and i >= 65 and zreg(AS[t["sym"]], i, 20) < -1.5:
                live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0)))
    row("LIVE ref", live, kw, cut)
    # (b) conditioner: seasonal mean of the signal's own month
    for t in live:
        t["_s"] = seas(MR[t["sym"]], t["t"][:7])
    ok = [t for t in live if t["_s"] is not None]
    row("LIVE with seasonal data", ok, kw, cut)
    s = sorted(t["_s"] for t in ok); q1, q2 = s[len(s)//3], s[2*len(s)//3]
    row("seasonal low third", [t for t in ok if t["_s"] <= q1], kw, cut)
    row("seasonal mid third", [t for t in ok if q1 < t["_s"] <= q2], kw, cut)
    row("seasonal high third", [t for t in ok if t["_s"] > q2], kw, cut)
    row("seasonal skip low third", [t for t in ok if t["_s"] > q1], kw, cut)
    row("seasonal >0", [t for t in ok if t["_s"] > 0], kw, cut)
    # (a) sleeves
    firsts = {}
    spyA = AS["SPY"] if "SPY" in AS else None
    dates = sorted({d for A in AS.values() for d in A["t"]})
    for d in dates:
        firsts.setdefault(d[:7], d)
    for tag, top in (("top", True), ("bottom", False)):
        T = []
        for ym, d in firsts.items():
            if ym < "2021-01": continue
            sc = []
            for s_, A in AS.items():
                i = IX[s_].get(d)
                if i is None or i < 200: continue
                if not trend_ok(A, i, "long", "s50_200") or not PT.gate_ok(ctx, d, "long", "spy200"): continue
                x = seas(MR[s_], ym)
                if x is not None: sc.append((x, s_, i))
            sc.sort(reverse=top); k = max(1, len(sc) // 5)
            for x, s_, i in sc[:k]:
                r = sim(AS[s_], i, "long", 4.0, "none", 21)
                if r: r.update(sym=s_, t_exit=r["te"], score=x, side="long", rule="seasmo"); T.append(r)
        P = row(f"sleeve {tag} quintile hold21", T, kw, cut)
        if top: row("   + live combined", live + T, kw, cut)
    print("variants tried: 6 conditioner + 2 sleeves")
