"""Lab run 21 (2026-11-10): pullback depth in ATR units / distance below SMA10 / relative strength vs SPY as conditioners
of the LIVE setup (vol60>=1.75%). Web-inspired (Connors-style 'deeper pullback = stronger reversion'; unverified). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
import lab_breadth
from lab_52wh import row
from lab_sector import feats

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); bars = lab.load_bars(); spy = bars["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = challenger.DEF_PORT
    T0 = PT.gen(AS, ctx, challenger.ruleset()); B = lab_breadth.breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    sc = [b["c"] for b in spy]; sx = {b["t"][:10]: i for i, b in enumerate(spy)}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    def ft(t):
        A = AS[t["sym"]]; i = IX[t["sym"]].get(t["t"][:10]); j = sx.get(t["t"][:10])
        if i is None or j is None or i < 70 or j < 70 or not A["atr"][i]: return None
        c = A["c"]; atr = A["atr"][i]
        return dict(d3=(c[i-3]-c[i])/atr, d5=(max(c[i-5:i])-c[i])/atr, s10=(A["s10"][i]-c[i])/atr,
                    rs60=(c[i]/c[i-60]-sc[j]/sc[j-60])*100, rs20=(c[i]/c[i-20]-sc[j]/sc[j-20])*100)
    ff = {id(t): ft(t) for t in live}
    row("LIVE (vol175)", live, kw, cut)
    V = [("3d drop >= 1.5 ATR", lambda f: f["d3"] >= 1.5), ("3d drop >= 2.5 ATR", lambda f: f["d3"] >= 2.5),
         ("3d drop < 2.5 ATR", lambda f: f["d3"] < 2.5), ("close >= 2 ATR under SMA10", lambda f: f["s10"] >= 2.0),
         ("close < 2 ATR under SMA10", lambda f: f["s10"] < 2.0),
         ("rel strength 60d vs SPY > 0", lambda f: f["rs60"] > 0), ("rel strength 60d vs SPY <= 0", lambda f: f["rs60"] <= 0),
         ("rel strength 20d vs SPY < -5%", lambda f: f["rs20"] < -5)]
    print("variants tried:", len(V))
    for n, fn in V: row(n, [t for t in live if ff[id(t)] and fn(ff[id(t)])], kw, cut)
