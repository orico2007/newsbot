"""Lab run 24: SPY short-term trend / realized-vol state at signal date as conditioner of the LIVE setup (own idea). Backtest only."""
import datetime, statistics
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
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    sc = [b["c"] for b in spy]; sd = {b["t"][:10]: i for i, b in enumerate(spy)}
    def sma20(d):
        i = sd.get(d); return None if i is None or i < 20 else sc[i] / (sum(sc[i-19:i+1]) / 20) - 1
    def rv5(d):
        i = sd.get(d)
        if i is None or i < 6: return None
        return statistics.pstdev([sc[j]/sc[j-1]-1 for j in range(i-4, i+1)]) * 100
    row("LIVE vol175", live, kw, cut)
    d = lambda t: t["t"][:10]
    vals = sorted(v for v in (rv5(d(t)) for t in live) if v is not None); med = vals[len(vals)//2]
    print(f"SPY 5d rv median {med:.3f}")
    V = [("SPY > SMA20", lambda t: (sma20(d(t)) or -9) > 0), ("SPY <= SMA20", lambda t: (sma20(d(t)) if sma20(d(t)) is not None else 9) <= 0),
         ("SPY 5d rv > median", lambda t: (rv5(d(t)) or -1) > med), ("SPY 5d rv <= median", lambda t: (rv5(d(t)) if rv5(d(t)) is not None else 99) <= med)]
    print("variants tried:", len(V))
    for n, f in V: row(n, [t for t in live if f(t)], kw, cut)
