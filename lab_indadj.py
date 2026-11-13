"""Lab run 40 (2026-11-13): industry-adjusted short-term reversal (stock 3d return minus same-sector peer mean 3d return) as conditioner of the LIVE vol60>=1.75% setup.
Web hint: Dimensional/Medhat-Novy-Marx note on industry-adjusted reversal (unverified; rules are my own). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth
from lab_sector import feats

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); raw = lab.load_bars(); last = raw["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    B = lab_breadth.breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    base = [t for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t) and (t["sym"], t["t"]) in F]
    for t in base:
        t["_f"] = F[(t["sym"], t["t"])]; t["score"] = -t["_f"]["m3"]
    ids = sorted(t["_f"]["idio"] for t in base); n = len(ids)
    med, q1, q2 = ids[n//2], ids[n//3], ids[2*n//3]
    print("n", n, "idio median", round(med,2), "tertiles", round(q1,2), round(q2,2))
    V = [("LIVE ref (peer-weakness rank)", lambda t: True),
         ("idio below median (lagging its sector)", lambda t: t["_f"]["idio"] < med),
         ("idio above median (sector fell with it)", lambda t: t["_f"]["idio"] >= med),
         ("idio bottom tertile", lambda t: t["_f"]["idio"] < q1),
         ("idio top tertile", lambda t: t["_f"]["idio"] >= q2),
         ("skip idio bottom tertile", lambda t: t["_f"]["idio"] >= q1)]
    print("variants tried:", len(V) - 1 + 1)
    for nm, f in V: row(nm, [t for t in base if f(t)], kw, cut)
    row("rank by most negative idio", [dict(t, score=-t["_f"]["idio"]) for t in base], kw, cut)
