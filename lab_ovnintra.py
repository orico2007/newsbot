"""Lab run 37 (2026-11-12): overnight vs intraday decomposition of the signal-day drop, as conditioner of the LIVE vol60>=1.75% setup.
Web-seeded (Lou-Polk-Skouras tug of war; Quantpedia short-term reversals + intraday transactions). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); raw = lab.load_bars(); spy = raw["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    B = lab_breadth.breadth_series(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    RB = {s: {b["t"][:10]: (j, b) for j, b in enumerate(raw[s])} for s in AS if s in raw}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    base = [t for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    for t in base:
        d = t["t"][:10]; j, b = RB[t["sym"]][d]; pc = raw[t["sym"]][j-1]["c"]
        t["_on"] = (b["o"] / pc - 1) * 100; t["_id"] = (b["c"] / b["o"] - 1) * 100
    import statistics as st
    print("median on/id", st.median(t["_on"] for t in base), st.median(t["_id"] for t in base))
    V = [("LIVE ref", lambda t: True),
         ("overnight drop dominates (on<id)", lambda t: t["_on"] < t["_id"]),
         ("intraday drop dominates (id<on)", lambda t: t["_id"] < t["_on"]),
         ("gap down (on<-0.5%)", lambda t: t["_on"] < -0.5),
         ("no gap (on>=-0.5%)", lambda t: t["_on"] >= -0.5),
         ("closed below open (id<0)", lambda t: t["_id"] < 0),
         ("closed above open (id>=0)", lambda t: t["_id"] >= 0)]
    print("variants tried:", len(V) - 1)
    for n, f in V: row(n, [t for t in base if f(t)], kw, cut)
