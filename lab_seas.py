"""Lab run 43 (2026-11-13): own-stock same-calendar-month seasonality (Heston-Sadka) as conditioner of the LIVE vol60>=1.75% setup.
Feature: mean return of the stock in the same calendar month in the prior 2-5 years (fully completed months only). Backtest only."""
import datetime, statistics
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth

def mret(A):
    t, c = A["t"], A["c"]; last = {}
    for i, d in enumerate(t): last[d[:7]] = i
    keys = sorted(last); out = {}
    for k0, k1 in zip(keys, keys[1:]):
        out[k1] = c[last[k1]] / c[last[k0]] - 1
    return out

def seas(M, d, ny=5):
    y, m = int(d[:4]), int(d[5:7]); v = [M[f"{y-k}-{m:02d}"] for k in range(1, ny + 1) if f"{y-k}-{m:02d}" in M]
    return statistics.mean(v) if len(v) >= 2 else None

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); raw = lab.load_bars(); last = raw["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    B = lab_breadth.breadth_series(AS); MR = {s: mret(A) for s, A in AS.items()}; SM = mret({"t": [b["t"] for b in raw["SPY"]], "c": [b["c"] for b in raw["SPY"]]})
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    base = [t for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    for t in base:
        t["_s"] = seas(MR[t["sym"]], t["t"][:10]); s = seas(SM, t["t"][:10]); t["_r"] = None if t["_s"] is None or s is None else t["_s"] - s
    ok = [t for t in base if t["_s"] is not None]
    print("base", len(base), "with seasonality", len(ok))
    v = sorted(t["_s"] for t in ok); med = v[len(v)//2]; q1, q2 = v[len(v)//3], v[2*len(v)//3]
    print("median", round(med*100,2), "tertiles", round(q1*100,2), round(q2*100,2))
    V = [("LIVE ref (all)", base), ("LIVE ref (with feature)", ok),
         ("seasonal >= median", [t for t in ok if t["_s"] >= med]),
         ("seasonal < median", [t for t in ok if t["_s"] < med]),
         ("seasonal top tertile", [t for t in ok if t["_s"] >= q2]),
         ("seasonal bottom tertile", [t for t in ok if t["_s"] < q1]),
         ("skip bottom tertile", [t for t in ok if t["_s"] >= q1])]
    print("variants tried:", len(V) + 1)
    for n, L in V: row(n, L, kw, cut)
    row("rank by highest seasonal", [dict(t, score=t["_s"]) for t in ok], kw, cut)
    # stock month seasonal vs SPY: univariate edge check (mean trade return by half)
