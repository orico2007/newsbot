"""Lab run 24 (2026-11-11): stop distance (ATR) and max-hold re-checked on the LIVE vol60>=1.75% setup (high-vol names may want different stops). Own idea. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth
from lab_sector import feats

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    B = lab_breadth.breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    def live(**k):
        T0 = PT.gen(AS, ctx, challenger.ruleset(**k))
        return [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
                for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    V = [("LIVE (stop4,hold7)", {}), ("stop 3", dict(stop=3)), ("stop 5", dict(stop=5)), ("stop 6", dict(stop=6)),
         ("hold 5", dict(hold=5)), ("hold 10", dict(hold=10)), ("hold 12", dict(hold=12))]
    print("variants tried:", len(V))
    for n, k in V:
        try: row(n, live(**k), kw, cut)
        except Exception as e: print(n, "ERR", e)
