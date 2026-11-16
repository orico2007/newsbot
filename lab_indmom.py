"""Lab run 22 (2026-11-16): industry-momentum conditioning of the LIVE setup (Novy-Marx 'reversals and industry momentum' idea).
Sector-peer mean 126d / 252d-ex-21d return (self excluded) at signal day; keep reversal signals only in winning sectors. Backtest only."""
import datetime
import lab, sweep, challenger, market
import portfolio_test as PT
from challenger import R, A, E, F
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats
from lab_retune import live

def indmom(AS):
    sec = {}
    for s in AS: sec.setdefault(market.SECTOR_OF.get(s), []).append(s)
    ix = {s: {t: i for i, t in enumerate(a["t"])} for s, a in AS.items()}
    M = {}
    for s, a in AS.items():
        peers = [p for p in sec.get(market.SECTOR_OF.get(s), []) if p != s]
        if len(peers) < 2: continue
        for i in range(260, len(a["c"])):
            d = a["t"][i]; r6, r12 = [], []
            for p in peers:
                j = ix[p].get(d)
                if j is None or j < 260: continue
                c = AS[p]["c"]; r6.append(c[j] / c[j-126] - 1); r12.append(c[j-21] / c[j-252] - 1)
            if len(r6) >= 2: M[(s, d)] = (sum(r6) / len(r6) * 100, sum(r12) / len(r12) * 100)
    return M

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    B = breadth_series(AS); Fs = feats(AS); IX = {s: {d: i for i, d in enumerate(a["t"])} for s, a in AS.items()}
    M = indmom(AS)
    rules = [R(**x) for x in (A, E, F)]
    base = live(AS, ctx, rules, B, Fs, IX, volmin=1.75)
    base0 = live(AS, ctx, rules, B, Fs, IX, volmin=0)   # no vol filter (live before run 8)
    g = lambda t: M.get((t["sym"], t["t"]))
    def sub(T, fn): return [t for t in T if g(t) and fn(g(t))]
    print("data through", last, "signals with sector mom:", sum(1 for t in base if g(t)), "of", len(base))
    V = [("LIVE (vol175)", base), ("sector 126d > 0", sub(base, lambda m: m[0] > 0)), ("sector 126d <= 0", sub(base, lambda m: m[0] <= 0)),
         ("sector 126d > 5", sub(base, lambda m: m[0] > 5)), ("sector 12-1m > 0", sub(base, lambda m: m[1] > 0)),
         ("sector 12-1m <= 0", sub(base, lambda m: m[1] <= 0)), ("sector 12-1m > 10", sub(base, lambda m: m[1] > 10)),
         ("NO-VOL base (breadth+rank)", base0), ("NO-VOL + sector 126d > 0", sub(base0, lambda m: m[0] > 0)),
         ("NO-VOL + sector 126d <= 0", sub(base0, lambda m: m[0] <= 0))]
    print("variants tried:", len(V))
    for n, T in V: row(n, T, kw, cut)
