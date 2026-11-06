"""Lab run 10: monthly sector-momentum rotation (Faber / Quantpedia) as an uncorrelated sleeve, ETF and stock forms. Backtest only."""
import datetime, statistics
from collections import defaultdict
import lab, research, sweep, challenger, market
import portfolio_test as PT
from lab_52wh import row
SLIP = 0.05

def month_firsts(spy):
    d = [b["t"][:10] for b in spy]; return [i for i in range(1, len(d)) if d[i][:7] != d[i-1][:7]]

def mk(B, i, j, sym, score):
    e = B[i]["c"] * (1 + SLIP/100); x = B[j]["c"] * (1 - SLIP/100); p = (x/e - 1) * 100
    return {"t": B[i]["t"], "t_exit": B[j]["t"], "pnl_pct": p, "R": p / 8.0, "held": j - i, "sym": sym, "score": score, "side": "long", "rule": "rot"}

def rotation(bars, syms, lb, skip, topn, gate, hold=21, ctx=None):
    spy = bars["SPY"]; idx = {b["t"]: k for k, b in enumerate(spy)}; out = []
    for i in month_firsts(spy):
        t = spy[i]["t"]
        if i < lb + skip + 1 or i + hold >= len(spy): continue
        if gate and not ctx["a200"].get(t[:10], False): continue
        sc = []
        for s in syms:
            B = bars.get(s)
            if not B or len(B) < 260: continue
            m = {b["t"]: k for k, b in enumerate(B)}
            if t not in m: continue
            k = m[t]
            if k < lb + skip + 1 or k + hold >= len(B): continue
            sc.append((B[k - skip]["c"] / B[k - lb]["c"] - 1, s, k))
        sc.sort(reverse=True)
        for r, s, k in sc[:topn]: out.append(mk(bars[s], k, k + hold, s, r * 100))
    return out

def monthly_corr(a, b, size=10):
    def mm(T):
        d = defaultdict(float)
        for t in T: d[t["t_exit"][:7]] += size * t["pnl_pct"] / 100
        return d
    A, B = mm(a), mm(b); ks = sorted(set(A) & set(B))
    return statistics.correlation([A[k] for k in ks], [B[k] for k in ks]) if len(ks) > 5 else None

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); bars = lab.load_bars(); spy = bars["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset())
    row("CHAMPION", champ, kw, cut)
    etfs = list(market.SECTORS); stocks = list(AS)
    sk = dict(size_pct=10, max_pos=12, per_day=12, sector_cap=0)
    V = [("ETF top3 12-1m mom, no gate", etfs, 252, 21, 3, False),
         ("ETF top3 12-1m mom, SPY>200d", etfs, 252, 21, 3, True),
         ("ETF top3 6m mom, SPY>200d", etfs, 126, 0, 3, True),
         ("ETF top3 3m mom, SPY>200d", etfs, 63, 0, 3, True),
         ("stocks top10 12-1m mom, SPY>200d", stocks, 252, 21, 10, True),
         ("stocks top10 6m mom, SPY>200d", stocks, 126, 0, 10, True)]
    print("variants tried:", len(V))
    for name, syms, lb, skp, n, g in V:
        T = rotation(bars, syms, lb, skp, n, g, ctx=ctx)
        P = row(name, T, sk, cut)
        print(f"   monthly-return corr with champion: {monthly_corr(P['trades'], lab.portfolio(champ, **kw)['trades']):.2f}" if P['trades'] else "")
        row("   + champion combined (18 pos, 6/day)", champ + T, dict(size_pct=10, max_pos=18, per_day=6), cut)
