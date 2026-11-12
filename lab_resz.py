"""Lab run 39 (2026-11-12): beta-adjusted residual shock z-score (Asymmetric Idiosyncratic Reversal, NBER w35840) as conditioner of the LIVE vol60>=1.75% setup.
Residual = stock ret - beta*SPY ret (beta from prior 120d, ending day before window); z = 3d summed residual / (residual daily stdev over prior 60d * sqrt3). Backtest only."""
import datetime, statistics
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth

def resid_z(A, spyc, spyix, i, k=3):
    t = A["t"]; c = A["c"]
    if i < 190: return None
    idx = [spyix.get(t[j]) for j in range(i - 180, i + 1)]
    if any(x is None for x in idx) or idx[0] < 1: return None
    sr = [spyc[x] / spyc[x-1] - 1 for x in idx[1:]]
    r = [c[j] / c[j-1] - 1 for j in range(i - 179, i + 1)]
    # beta from days [0:120], resid vol from days [120:177] excluding last k
    bs, br = sr[:120], r[:120]
    mv = statistics.pvariance(bs)
    if mv == 0: return None
    beta = statistics.mean((a - statistics.mean(bs)) * (b - statistics.mean(br)) for a, b in zip(bs, br)) / mv
    res = [b - beta * a for a, b in zip(sr, r)]
    sd = statistics.pstdev(res[-63:-k])
    if sd == 0: return None
    return sum(res[-k:]) / (sd * k ** 0.5)

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); raw = lab.load_bars(); spy = raw["SPY"]; last = spy[-1]["t"][:10]
    spyc = [b["c"] for b in spy]; spyix = {b["t"][:10]: i for i, b in enumerate(spy)}
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    B = lab_breadth.breadth_series(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    base = [t for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    for t in base:
        i = IX[t["sym"]].get(t["t"][:10]); t["_z"] = resid_z(AS[t["sym"]], spyc, spyix, i, 3) if i else None
        t["_z1"] = resid_z(AS[t["sym"]], spyc, spyix, i, 1) if i else None
    zs = sorted(t["_z"] for t in base if t["_z"] is not None); med = zs[len(zs)//2]
    print("n base", len(base), "with z", len(zs), "median z3", round(med, 2), "tertiles", round(zs[len(zs)//3],2), round(zs[2*len(zs)//3],2))
    q1, q2 = zs[len(zs)//3], zs[2*len(zs)//3]
    V = [("LIVE ref", lambda t: True),
         ("z3 more negative than median (idio-heavy drop)", lambda t: t["_z"] is not None and t["_z"] < med),
         ("z3 above median (market-driven drop)", lambda t: t["_z"] is not None and t["_z"] >= med),
         ("z3 bottom tertile", lambda t: t["_z"] is not None and t["_z"] < q1),
         ("z3 top tertile", lambda t: t["_z"] is not None and t["_z"] >= q2),
         ("skip z3 top tertile", lambda t: t["_z"] is not None and t["_z"] < q2)]
    print("variants tried:", len(V) - 1 + 1)
    for n, f in V: row(n, [t for t in base if f(t)], kw, cut)
    row("rank by most negative z3", [dict(t, score=-(t["_z"] or 0)) for t in base], kw, cut)
