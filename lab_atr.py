"""Lab run 12 (2026-11-09, own idea): ATR% (ATR14/close) as the volatility measure for the LIVE setup, vs vol60 stdev; thresholds chosen on 2021-23, checked on 2024-26. Backtest only."""
import datetime, math
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row as _row
def row(nm, T, kw, cut):
    if len(T) < 5: print(f'{nm:42} n={len(T)} (too few)'); return None
    return _row(nm, T, kw, cut)
from lab_breadth import breadth_series
from lab_sector import feats

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); B = breadth_series(AS); F = feats(AS)
    m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    def feat(t):
        A = AS[t["sym"]]; i = IX[t["sym"]].get(t["t"][:10])
        if i is None or i < 70 or not A["atr"][i]: return None
        r = [A["c"][j]/A["c"][j-1]-1 for j in range(i-59, i+1)]
        m = sum(r)/60; sd = math.sqrt(sum((x-m)**2 for x in r)/59)*100
        return dict(vol=sd, atr=A["atr"][i]/A["c"][i]*100)
    live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            u = dict(t); u["score"] = -m3(t); u["_f"] = feat(t); live.append(u)
    live = [t for t in live if t["_f"]]
    at = sorted(t["_f"]["atr"] for t in live); q = lambda p: at[int(p*(len(at)-1))]
    print("ATR% terciles", round(q(1/3),2), round(q(2/3),2))
    row("LIVE ref", live, kw, cut); n = 1
    for lo, hi, nm in ((0, q(1/3), "ATR% low tercile"), (q(1/3), q(2/3), "ATR% mid"), (q(2/3), 99, "ATR% high")):
        row(nm, [t for t in live if lo <= t["_f"]["atr"] < hi], kw, cut); n += 1
    for th in (2.5, 3, 3.5, 4, 5):
        row(f"ATR%>={th}", [t for t in live if t["_f"]["atr"] >= th], kw, cut); n += 1
    row("vol60>=1.75 (run 8 candidate)", [t for t in live if t["_f"]["vol"] >= 1.75], kw, cut)
    for th in (3, 4):
        row(f"vol>=1.75 & ATR%>={th}", [t for t in live if t["_f"]["vol"] >= 1.75 and t["_f"]["atr"] >= th], kw, cut)
        row(f"vol>=1.75 & ATR%<{th}", [t for t in live if t["_f"]["vol"] >= 1.75 and t["_f"]["atr"] < th], kw, cut)
        row(f"vol<1.75 & ATR%>={th}", [t for t in live if t["_f"]["vol"] < 1.75 and t["_f"]["atr"] >= th], kw, cut); n += 3
    # early/late split
    for nm, ys in (("EARLY 21-23", ("2021","2022","2023")), ("LATE 24-26", ("2024","2025","2026"))):
        for th in (0, 3, 4):
            T = [t for t in live if t["t"][:4] in ys and t["_f"]["atr"] >= th]
            row(f"{nm} ATR%>={th}", T, kw, cut); n += 1
    print("variants tried this run:", n)
