"""Lab run 23: prior 21d / 5d return and distance-from-20d-high conditioning of the vol60>=1.75% LIVE setup (own idea). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
import lab_breadth, lab_sector
from lab_52wh import row

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = challenger.DEF_PORT
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    B = lab_breadth.breadth_series(AS); F = lab_sector.feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    def at(t): return AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(*[AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])]))
    live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    def r(t, n):
        A, i = at(t); return None if i is None or i < n+1 else (A["c"][i]/A["c"][i-n]-1)*100
    def dh(t):
        A, i = at(t)
        if i is None or i < 21: return None
        return (A["c"][i]/max(A["c"][i-20:i+1])-1)*100
    row("LIVE vol175", live, kw, cut)
    V = []
    for n in (21, 10, 5):
        vals = sorted(v for v in (r(t, n) for t in live) if v is not None); med = vals[len(vals)//2]
        print(f"ret{n} median {med:.2f}")
        V += [(f"ret{n} > median", lambda t, n=n, m=med: (r(t, n) or -999) > m),
              (f"ret{n} <= median", lambda t, n=n, m=med: (r(t, n) if r(t, n) is not None else 999) <= m)]
    vals = sorted(v for v in (dh(t) for t in live) if v is not None); med = vals[len(vals)//2]
    print(f"dist from 20d high median {med:.2f}")
    V += [("dist20high < median (deeper)", lambda t: (dh(t) if dh(t) is not None else 0) < med),
          ("dist20high >= median (shallow)", lambda t: (dh(t) if dh(t) is not None else -999) >= med)]
    print("variants tried:", len(V))
    for n, f in V: row(n, [t for t in live if f(t)], kw, cut)
