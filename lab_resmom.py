"""Lab run 71: residual (beta-adjusted) 12-1m momentum and low-volatility monthly sleeves (Blitz/Huij/Martens; Quantpedia low-vol). Backtest only."""
import datetime
import numpy as np
import lab, sweep, challenger
import portfolio_test as PT
import lab_breadth, lab_sector, lab_rotation as R
from lab_52wh import row

def scored(bars, syms, fn, topn, gate, ctx, hold=21, reverse=True):
    spy = bars["SPY"]; out = []
    sc_cache = {}
    for i in R.month_firsts(spy):
        t = spy[i]["t"]
        if i < 275 or i + hold >= len(spy): continue
        if gate and not ctx["a200"].get(t[:10], False): continue
        sc = []
        for s in syms:
            B = bars.get(s)
            if not B or len(B) < 300: continue
            m = sc_cache.setdefault(s, {b["t"]: k for k, b in enumerate(B)})
            k = m.get(t)
            if k is None or k < 275 or k + hold >= len(B): continue
            # align SPY index by date
            v = fn(B, k, spy, i)
            if v is not None and np.isfinite(v): sc.append((v, s, k))
        sc.sort(reverse=reverse)
        for v, s, k in sc[:topn]: out.append(R.mk(bars[s], k, k + hold, s, v))
    return out

def rets(B, k, n): 
    c = np.array([B[j]["c"] for j in range(k - n, k + 1)]); return c[1:] / c[:-1] - 1

def resmom(B, k, spy, i):
    if B[k]["t"] != spy[i]["t"] or B[k-252]["t"] != spy[i-252]["t"]: return None
    r = rets(B, k, 252); m = rets(spy, i, 252)
    b = np.cov(r, m)[0, 1] / np.var(m, ddof=1); res = r - b * m
    x = res[:-21]; sd = x.std()
    return x.sum() / sd if sd > 0 else None

def rawmom(B, k, spy, i): return B[k-21]["c"] / B[k-252]["c"] - 1
def lowvol(B, k, spy, i): return rets(B, k, 60).std()
def lowbeta(B, k, spy, i):
    if B[k]["t"] != spy[i]["t"] or B[k-60]["t"] != spy[i-60]["t"]: return None
    r = rets(B, k, 60); m = rets(spy, i, 60); return np.cov(r, m)[0, 1] / np.var(m, ddof=1)

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); bars = lab.load_bars(); spy = bars["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = challenger.DEF_PORT
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    B = lab_breadth.breadth_series(AS); F = lab_sector.feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    row("LIVE vol175 (champion)", live, kw, cut)
    syms = [s for s in AS if s != "SPY"]
    V = [("resmom 12-1 top10 gate", resmom, 10, True, True),
         ("resmom 12-1 top20 gate", resmom, 20, True, True),
         ("rawmom 12-1 top10 gate (ctrl)", rawmom, 10, True, True),
         ("lowvol60 top10 gate", lowvol, 10, True, False),
         ("lowvol60 top20 nogate", lowvol, 20, False, False),
         ("lowbeta60 top10 gate", lowbeta, 10, True, False)]
    print("variants tried:", len(V))
    for name, fn, n, g, rev in V:
        T = scored(bars, syms, fn, n, g, ctx, reverse=rev)
        row(name, T, kw, cut)
        row("   + champion combined", live + T, kw, cut)
        print("   monthly corr vs live:", R.monthly_corr(live, T))
