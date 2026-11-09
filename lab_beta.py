"""Lab run 8 (2026-11-09): realized-volatility / SPY-beta / low-price conditioning of the LIVE setup (web idea: Alpha Architect
'How volatility and turnover affect return reversals': higher vol -> faster, stronger reversals). Backtest only."""
import datetime, math
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); bars = lab.load_bars(); spy = bars["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); B = breadth_series(AS); F = feats(AS)
    m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            u = dict(t); u["score"] = -m3(t); live.append(u)
    sc = {b["t"][:10]: b["c"] for b in spy}; sd = sorted(sc)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    def ret(A, j): return A["c"][j] / A["c"][j-1] - 1
    def feat(t):
        A = AS[t["sym"]]; i = IX[t["sym"]].get(t["t"][:10])
        if i is None or i < 70: return None
        rs, rm = [], []
        for j in range(i - 59, i + 1):
            d = A["t"][j]; dp = A["t"][j-1]
            if d not in sc or dp not in sc: return None
            rs.append(ret(A, j)); rm.append(sc[d] / sc[dp] - 1)
        ms, mm = sum(rs)/60, sum(rm)/60
        cov = sum((a-ms)*(b-mm) for a, b in zip(rs, rm)); vm = sum((b-mm)**2 for b in rm)
        vs = sum((a-ms)**2 for a in rs)
        return dict(vol=math.sqrt(vs/59)*100, beta=cov/vm if vm else 1, px=A["c"][i])
    for t in live: t["_f"] = feat(t)
    ok = [t for t in live if t["_f"]]
    print("with feats", len(ok), "of", len(live))
    vs = sorted(t["_f"]["vol"] for t in ok); bs = sorted(t["_f"]["beta"] for t in ok)
    q = lambda a, p: a[int(len(a)*p)]
    v33, v67, b33, b67 = q(vs, .33), q(vs, .67), q(bs, .33), q(bs, .67)
    print(f"vol terciles {v33:.2f}/{v67:.2f}  beta terciles {b33:.2f}/{b67:.2f}")
    row("LIVE ref", live, kw, cut)
    V = [("vol low tercile", lambda f: f["vol"] < v33), ("vol mid tercile", lambda f: v33 <= f["vol"] < v67),
         ("vol high tercile", lambda f: f["vol"] >= v67), ("beta low tercile", lambda f: f["beta"] < b33),
         ("beta mid tercile", lambda f: b33 <= f["beta"] < b67), ("beta high tercile", lambda f: f["beta"] >= b67),
         ("price < $50", lambda f: f["px"] < 50), ("price >= $50", lambda f: f["px"] >= 50)]
    print("variants tried:", len(V) + 1)
    for n, fn in V:
        S = [t for t in ok if fn(t["_f"])]
        row(n, S, kw, cut)
        h = [t for t in S if t["t"][:4] <= "2023"]; l = [t for t in S if t["t"][:4] >= "2024"]
        print("   split <=2023 n=%d | >=2024 n=%d" % (len(h), len(l)))
