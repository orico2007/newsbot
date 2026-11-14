"""Lab run 56 (2026-11-14): sector/index ETF short-term reversion sleeve, standalone and added to the LIVE setup (web-seeded; lab_etf.py). Backtest only.
Sources (titles/snippets only, not fetched): https://quantifiedstrategies.substack.com/p/best-etf-for-mean-reversion-strategies , https://concretumgroup.substack.com/p/a-mean-reversion-model-for-us-sectors"""
import datetime
import lab, sweep, challenger, market
import portfolio_test as PT
from sweep import build, sim, trend_ok
from sweep2 import trig2
import lab_breadth, lab_sector
from lab_52wh import row

ETFS = ["XLB","XLC","XLE","XLF","XLI","XLK","XLP","XLRE","XLU","XLV","XLY","QQQ","IWM","DIA","XBI"]

def etf_trades(EA, ctx, trig, hold=7, stop=4.0, trend="s200", gate="spy200", exit_="prevhl", per_day_cool=3):
    out = []
    for sym, A in EA.items():
        cd = 0
        for i in range(205, len(A["c"]) - 2):
            if i < cd: continue
            if trig2(A, i, "long", trig) and trend_ok(A, i, "long", trend) and sweep.gate_ok(ctx, A["t"][i], "long", gate):
                r = sim(A, i, "long", stop, exit_, hold)
                if r:
                    r.update(sym=sym, t_exit=r["te"], score=-A["ret3"][i], side="long", rule="etf:" + trig); out.append(r)
                cd = i + per_day_cool
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); raw = lab.load_bars(); spy = raw["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    EA = {s: build(raw[s]) for s in ETFS if s in raw and len(raw[s]) > 260}
    print("ETFs", sorted(EA))
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    B = lab_breadth.breadth_series(AS); F = lab_sector.feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    V60 = lambda t: challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10]))
    live = [(dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t)
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and (V60(t) or 0) >= 1.75]
    row("LIVE ref", live, kw, cut)
    TR = ["r2_10", "r2_5", "down3_r2_20", "r2_5&ibs_0.25"]
    print("variants tried:", len(TR) * 2 + 1)
    for tr in TR:
        E = etf_trades(EA, ctx, tr)
        row(f"ETF alone {tr}", E, dict(size_pct=10, max_pos=6, per_day=2), cut)
        row(f"LIVE + ETF {tr}", live + E, kw, cut)
    E = etf_trades(EA, ctx, "r2_10", gate="none", trend="s200")
    row("ETF alone r2_10 no SPY gate", E, dict(size_pct=10, max_pos=6, per_day=2), cut)
    # correlation of daily pnl (by exit date) live vs etf r2_10
    import collections
    E = etf_trades(EA, ctx, "r2_10")
    def daily(T):
        d = collections.defaultdict(float)
        for t in T: d[t["t_exit"][:10]] += t["pnl_pct"]
        return d
    a, b = daily(live), daily(E); ds = sorted(set(a) | set(b))
    import numpy as np
    x = np.array([a.get(k, 0) for k in ds]); y = np.array([b.get(k, 0) for k in ds])
    print("daily pnl corr live vs ETF r2_10:", round(float(np.corrcoef(x, y)[0, 1]), 3), "overlap days", sum(1 for k in ds if k in a and k in b))
