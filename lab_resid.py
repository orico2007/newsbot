"""Lab run 30 (2026-11-08): residual (SPY-beta-adjusted) short-term reversal conditioning of the LIVE setup (web idea: Blitz/Huij/Lansdorp/Verbeek 'residual reversal'). Backtest only."""
import datetime
import numpy as np
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def resid5(AS, spy, t, W=60):
    A = AS[t["sym"]]
    try: i = A["t"].index(t["t"])
    except ValueError: return None
    sidx = {x["t"]: k for k, x in enumerate(spy)}
    j = sidx.get(t["t"])
    if i < W + 6 or j is None or j < W + 6: return None
    c = A["c"]; s = [x["c"] for x in spy]
    # align by date for the 60d window
    try: ds = [sidx[A["t"][k]] for k in range(i-W, i+1)]
    except KeyError: return None
    sc = [s[k] for k in ds]; ac = c[i-W:i+1]
    rs = np.diff(sc)/np.array(sc[:-1]); ra = np.diff(ac)/np.array(ac[:-1])
    v = rs.var()
    if v == 0: return None
    beta = np.cov(ra, rs)[0, 1]/v
    r5a = c[i]/c[i-5]-1; r5s = s[j]/s[j-5]-1 if sidx.get(A["t"][i-5]) is not None else None
    r5s = s[j]/s[sidx[A["t"][i-5]]]-1
    return r5a - beta*r5s

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); B = breadth_series(AS); F = feats(AS)
    m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            u = dict(t); u["score"] = -m3(t); u["r"] = resid5(AS, spy, t); live.append(u)
    row("LIVE ref", live, kw, cut)
    ok = [t for t in live if t["r"] is not None]; print("with feats:", len(ok), "of", len(live))
    q = np.percentile([t["r"] for t in ok], [10,25,50,75,90]); print("resid5 quantiles", q.round(3))
    V = [("resid5 below median", lambda t: t["r"] < q[2]), ("resid5 above median", lambda t: t["r"] >= q[2]),
         ("resid5 bottom quartile", lambda t: t["r"] < q[1]), ("resid5 top quartile", lambda t: t["r"] >= q[3])]
    print("variants tried:", len(V)+2)
    for n, fn in V: row(n, [t for t in ok if fn(t)], kw, cut)
    for lab_, f in (("rank most-negative residual first", lambda t: -t["r"]), ("rank least-negative residual first", lambda t: t["r"])):
        T = []
        for t in ok:
            u = dict(t); u["score"] = f(t); T.append(u)
        row(lab_, T, kw, cut)
