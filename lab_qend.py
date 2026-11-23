"""Lab run 73 (2026-11-23): quarter-end / window-dressing calendar as conditioner of the live vol60+zreg setup (web seed: Quantified Strategies end-of-quarter page, search hit only). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats
from lab_zscore import zreg

def qflags():
    d = [b["t"][:10] for b in lab.load_bars()["SPY"]]; f = {}
    for i, t in enumerate(d):
        q = (int(t[5:7]) - 1) // 3; key = (t[:4], q)
        j = i
        while j + 1 < len(d) and (d[j+1][:4], (int(d[j+1][5:7]) - 1) // 3) == key: j += 1
        k = i
        while k - 1 >= 0 and (d[k-1][:4], (int(d[k-1][5:7]) - 1) // 3) == key: k -= 1
        f[t] = (i - k + 1, j - i + 1)   # trading day from quarter start, days to quarter end incl.
    return f

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(spy) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2; B = breadth_series(AS); F = feats(AS); Q = qflags()
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(t["t"][:10]); v = challenger.vol60(AS[t["sym"]], i)
            if v is not None and v >= 1.75 and i is not None and i >= 25 and zreg(AS[t["sym"]], i, 20) < -1.5 and t["t"][:10] in Q:
                live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0), _q=Q[t["t"][:10]]))
    row("LIVE (vol60+zreg)", live, kw, cut)
    V = [("last 5 days of quarter", lambda q: q[1] <= 5),
         ("NOT last 5 days", lambda q: q[1] > 5),
         ("last 10 days of quarter", lambda q: q[1] <= 10),
         ("first 5 days of quarter", lambda q: q[0] <= 5),
         ("window: last 5 + first 5", lambda q: q[1] <= 5 or q[0] <= 5),
         ("NOT window", lambda q: not (q[1] <= 5 or q[0] <= 5)),
         ("quarter days 6-55 (middle)", lambda q: 5 < q[0] and q[1] > 5)]
    for nm, f in V:
        T = [t for t in live if f(t["_q"])]
        row(nm, T, kw, cut)
    print("variants tried:", len(V))
    for nm, f in (("early 2021-23", lambda t: t["t"][:4] <= "2023"), ("late 2024-26", lambda t: t["t"][:4] >= "2024")):
        row(nm + " ref", [t for t in live if f(t)], kw, cut)
        row(nm + " NOT last5", [t for t in live if f(t) and t["_q"][1] > 5], kw, cut)
        row(nm + " last5", [t for t in live if f(t) and t["_q"][1] <= 5], kw, cut)
