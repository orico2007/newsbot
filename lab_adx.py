"""Lab run 25 (2026-11-11): trend-strength (ADX14, Kaufman efficiency ratio 10d) as conditioner of the LIVE vol60>=1.75% setup. Web idea (ADX-filtered mean reversion). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth
from lab_sector import feats

def adx_series(A, n=14):
    h, l, c = A["h"], A["l"], A["c"]; N = len(c); out = [None] * N
    if N < 3 * n: return out
    tr = [0] * N; pd = [0] * N; md = [0] * N
    for i in range(1, N):
        up, dn = h[i] - h[i-1], l[i-1] - l[i]
        pd[i] = up if up > dn and up > 0 else 0; md[i] = dn if dn > up and dn > 0 else 0
        tr[i] = max(h[i] - l[i], abs(h[i] - c[i-1]), abs(l[i] - c[i-1]))
    st, sp, sm = sum(tr[1:n+1]), sum(pd[1:n+1]), sum(md[1:n+1]); dx = [None] * N
    for i in range(n, N):
        if i > n: st = st - st / n + tr[i]; sp = sp - sp / n + pd[i]; sm = sm - sm / n + md[i]
        pi, mi = 100 * sp / st if st else 0, 100 * sm / st if st else 0
        dx[i] = 100 * abs(pi - mi) / (pi + mi) if pi + mi else 0
    a = sum(dx[n:2*n]) / n; out[2*n-1] = a
    for i in range(2*n, N): a = (a * (n - 1) + dx[i]) / n; out[i] = a
    return out

def er(A, i, n=10):
    c = A["c"]
    if i < n: return None
    p = sum(abs(c[j] - c[j-1]) for j in range(i-n+1, i+1))
    return abs(c[i] - c[i-n]) / p if p else None

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    B = lab_breadth.breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    AD = {s: adx_series(A) for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    base = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10]
    live = [t for t in base if hv(t)]
    def ad(t):
        i = IX[t["sym"]].get(t["t"][:10]); return None if i is None else AD[t["sym"]][i]
    def e(t):
        i = IX[t["sym"]].get(t["t"][:10]); return None if i is None else er(AS[t["sym"]], i)
    vals = sorted(x for x in map(ad, live) if x is not None); print("ADX quartiles", [round(vals[int(len(vals)*q)],1) for q in (.25,.5,.75)])
    row("LIVE (vol175)", live, kw, cut)
    V = [("ADX<20", lambda t: (ad(t) or 99) < 20), ("ADX 20-30", lambda t: 20 <= (ad(t) or -1) < 30),
         ("ADX>=25", lambda t: (ad(t) or -1) >= 25), ("ADX>=30", lambda t: (ad(t) or -1) >= 30),
         ("ER10<0.5", lambda t: (e(t) if e(t) is not None else 9) < .5), ("ER10>=0.5", lambda t: (e(t) if e(t) is not None else -1) >= .5)]
    print("variants tried:", len(V))
    for n, f in V: row(n, [t for t in live if f(t)], kw, cut)
    print("-- on live setup WITHOUT vol filter (does ADX substitute for vol?)")
    row("no-vol base", base, kw, cut)
    for n, f in V[:4]: row("novol " + n, [t for t in base if f(t)], kw, cut)
