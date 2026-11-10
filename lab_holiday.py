"""Lab run 17 (2026-11-10, web idea): pre-holiday effect (Quantpedia 'Pre-Holiday Effect', commodities/indices; daily-bar translation to the cached stock universe). (a) tag LIVE-setup signals by pre-holiday proximity; (b) standalone 1-day pre-holiday sleeve; (c) v3 volume exclusion on top of vol60>=1.75%. Backtest only."""
import datetime, statistics
import lab, sweep, challenger
import portfolio_test as PT
from sweep import sim, trend_ok
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def pre_holiday_days(dates, k):
    """Set of trading days within k trading days before a market closure (gap of >1 weekday)."""
    out = set()
    for j in range(len(dates) - 1):
        a = datetime.date.fromisoformat(dates[j]); b = datetime.date.fromisoformat(dates[j + 1])
        wd = sum(1 for n in range(1, (b - a).days) if (a + datetime.timedelta(n)).weekday() < 5)
        if wd >= 1:
            for q in range(max(0, j - k + 1), j + 1): out.add(dates[q])
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    dates = [b["t"][:10] for b in spy]
    PH1, PH2 = pre_holiday_days(dates, 1), pre_holiday_days(dates, 2)
    print("pre-holiday days k=1:", len(PH1), "k=2:", len(PH2))
    champ = PT.gen(AS, ctx, challenger.ruleset()); B = breadth_series(AS); F = feats(AS)
    m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            u = dict(t); u["score"] = -m3(t); live.append(u)
    row("LIVE", live, kw, cut)
    for nm, S in (("k=1", PH1), ("k=2", PH2)):
        row(f"LIVE signal on pre-holiday {nm}", [t for t in live if t["t"][:10] in S], kw, cut)
        row(f"LIVE excluding pre-holiday {nm}", [t for t in live if t["t"][:10] not in S], kw, cut)
    # standalone sleeve: buy close of last day before closure, sell next close
    sg = []
    for sym, A in AS.items():
        for i in range(210, len(A["c"]) - 2):
            d = A["t"][i][:10]
            if d not in PH1 or not A["atr"][i] or A["atr"][i] / A["c"][i] > 0.06: continue
            if not trend_ok(A, i, "long", "s50_200") or not PT.gate_ok(ctx, d, "long", "spy200"): continue
            sg.append((sym, i))
    T = []
    for sym, i in sg:
        r = sim(AS[sym], i, "long", 4.0, "none", 1)
        if r: r.update(sym=sym, t_exit=r["te"], score=-(AS[sym]["c"][i]/AS[sym]["c"][i-3]-1), side="long", rule="preh"); T.append(r)
    row("standalone pre-holiday 1d sleeve", T, kw, cut)
    row("   + champion (shared slots)", champ + T, kw, cut)
    # vol60>=1.75% candidate with v3 exclusion
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    def rv(t):
        A = AS[t["sym"]]; i = IX[t["sym"]].get(t["t"][:10])
        if i is None or i < 61: return None
        c = A["c"]; return statistics.pstdev([c[k]/c[k-1]-1 for k in range(i-59, i+1)])
    def v3(t):
        A = AS[t["sym"]]; i = IX[t["sym"]].get(t["t"][:10])
        if i is None or i < 25 or not A["vavg"][i]: return None
        return sum(A["v"][i-2:i+1])/3/A["vavg"][i]
    cand = [t for t in live if (rv(t) or 0) >= .0175]
    row("vol60>=1.75% candidate", cand, kw, cut)
    for th in (0.85, 1.0):
        row(f"  cand + v3>={th}", [t for t in cand if (v3(t) or 0) >= th], kw, cut)
    row("  cand excl pre-holiday k=1", [t for t in cand if t["t"][:10] not in PH1], kw, cut)
    print("variants tried: ~12")
