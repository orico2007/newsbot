"""Lab run 29: short-term volatility expansion (5d/20d realized vol vs 60d vol) and 5d range/ATR as conditioners of the vol60>=1.75% LIVE setup (own idea). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
import lab_breadth, lab_sector
from lab_52wh import row

def sd(A, i, n):
    r = [A["c"][j] / A["c"][j - 1] - 1 for j in range(i - n + 1, i + 1)]; m = sum(r) / n
    return (sum((x - m) ** 2 for x in r) / (n - 1)) ** 0.5 * 100

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = challenger.DEF_PORT
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    B = lab_breadth.breadth_series(AS); F = lab_sector.feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    def at(t): return AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(*at(t)))
    live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    def ratio(t, n):
        A, i = at(t)
        if i is None or i < 62: return None
        return sd(A, i, n) / sd(A, i, 60)
    def rng(t):
        A, i = at(t)
        if i is None or i < 20: return None
        tr = lambda j: max(A["h"][j]-A["l"][j], abs(A["h"][j]-A["c"][j-1]), abs(A["l"][j]-A["c"][j-1]))
        atr = sum(tr(j) for j in range(i-13, i+1))/14
        return tr(i)/atr
    row("LIVE vol175", live, kw, cut)
    V = []
    for nm, f in (("sd5/sd60", lambda t: ratio(t, 5)), ("sd20/sd60", lambda t: ratio(t, 20)), ("TR/ATR14 today", rng)):
        vals = sorted(v for v in (f(t) for t in live) if v is not None); med = vals[len(vals)//2]
        print(f"{nm} median {med:.2f}")
        V += [(f"{nm} > median", lambda t, f=f, m=med: (f(t) if f(t) is not None else -9) > m),
              (f"{nm} <= median", lambda t, f=f, m=med: (f(t) if f(t) is not None else 99) <= m)]
    print("variants tried:", len(V))
    for n, f in V: row(n, [t for t in live if f(t)], kw, cut)
