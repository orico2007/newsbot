"""Lab run 42 (2026-11-19): diversification filter on the LIVE vol60>=1.75% setup: skip a same-day signal if its 60d daily-return correlation with the
currently OPEN positions is high (mean or max). Own idea, seeded by a web search on concentration of correlated reversion positions (search hits only,
nothing fetched, unverified: https://quantpedia.com/testing-an-ai-assisted-research-workflow-for-multi-asset-pullback-strategy-discovery/). Backtest only."""
import datetime
from collections import defaultdict
import numpy as np
import lab, sweep, challenger, market
import portfolio_test as PT
import lab_breadth, lab_sector
from lab_52wh import row

def select(trades, corr, mode, thr, max_pos=12, per_day=4, sector_cap=2):
    by = defaultdict(list)
    for t in trades: by[t["t"]].append(t)
    openp, taken = [], []
    for d in sorted(by):
        openp = [p for p in openp if p["t_exit"] > d]
        slots = max_pos - len(openp)
        if slots <= 0: continue
        held = {p["sym"] for p in openp}; secs = defaultdict(int)
        for p in openp: secs[market.SECTOR_OF.get(p["sym"])] += 1
        n = 0
        for t in sorted(by[d], key=lambda x: -x.get("score", 0)):
            if n >= per_day or n >= slots: break
            if t["sym"] in held: continue
            sec = market.SECTOR_OF.get(t["sym"])
            if sec and sector_cap and secs[sec] >= sector_cap: continue
            if mode and openp:
                cs = [c for c in (corr(t["sym"], p["sym"], d) for p in openp) if c is not None]
                if cs:
                    v = max(cs) if mode == "max" else sum(cs) / len(cs)
                    if v > thr: continue
            openp.append(t); taken.append(t); held.add(t["sym"]); secs[sec] += 1; n += 1
    return taken

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    T0 = PT.gen(AS, ctx, challenger.ruleset()); B = lab_breadth.breadth_series(AS); F = lab_sector.feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    R = {}
    def rets(s):
        if s not in R:
            c = np.array(AS[s]["c"], float); r = np.zeros(len(c)); r[1:] = c[1:] / c[:-1] - 1; R[s] = r
        return R[s]
    cache = {}
    def corr(a, b, d):
        k = (a, b, d)
        if k in cache: return cache[k]
        ia, ib = IX[a].get(d), IX[b].get(d); v = None
        if ia and ib and ia >= 61 and ib >= 61:
            # align by date: both series should share calendar; use index offsets from the common date
            x, y = rets(a)[ia - 59:ia + 1], rets(b)[ib - 59:ib + 1]
            if x.std() > 0 and y.std() > 0: v = float(np.corrcoef(x, y)[0, 1])
        cache[k] = v; return v
    V = [("ref (own selector, no filter)", None, 0), ("mean corr to open > 0.6 skip", "mean", .6), ("mean corr > 0.5 skip", "mean", .5),
         ("max corr > 0.8 skip", "max", .8), ("max corr > 0.7 skip", "max", .7)]
    print("variants tried:", len(V) - 1, "(+ref)")
    for n, m, thr in V:
        tk = select(live, corr, m, thr)
        row(n, tk, dict(size_pct=10, max_pos=99, per_day=99, sector_cap=0), cut)
    row("LIVE ref via lab.portfolio", live, kw, cut)
