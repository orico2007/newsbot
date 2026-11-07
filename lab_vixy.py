"""Lab run 19 (2026-11-07): VIXY (VIX-futures ETF) volatility-regime filters and cross-asset (IWM/SPY) filter on the LIVE setup. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def series(bars, sym):
    return bars[sym]

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
    # VIXY features: close vs 20d SMA, 5d change. Note VIXY decays (roll), so use relative measures only.
    v = bars["VIXY"]; vf = {}
    for i in range(20, len(v)):
        c = v[i]["c"]; sma = sum(b["c"] for b in v[i-20:i]) / 20
        vf[v[i]["t"][:10]] = (c / sma - 1, c / v[i-5]["c"] - 1, c / min(b["c"] for b in v[i-60:i+1]) if i >= 60 else None)
    # IWM vs SPY 20d relative strength
    iw = {b["t"][:10]: b["c"] for b in bars["IWM"]}; sp = {b["t"][:10]: b["c"] for b in spy}
    days = [b["t"][:10] for b in spy]; rs = {}
    for i in range(20, len(days)):
        d, p = days[i], days[i-20]
        if d in iw and p in iw: rs[d] = (iw[d] / iw[p]) / (sp[d] / sp[p]) - 1
    d10 = lambda t: t["t"][:10]
    row("LIVE ref", live, kw, cut)
    V = [("VIXY > 20d SMA by 10%+ (fear spike present)", lambda t: d10(t) in vf and vf[d10(t)][0] > .10),
         ("VIXY not > SMA+25% (skip panic)", lambda t: d10(t) in vf and vf[d10(t)][0] <= .25),
         ("VIXY 5d change < +15%", lambda t: d10(t) in vf and vf[d10(t)][1] < .15),
         ("VIXY above its 20d SMA at all", lambda t: d10(t) in vf and vf[d10(t)][0] > 0),
         ("VIXY below its 20d SMA", lambda t: d10(t) in vf and vf[d10(t)][0] <= 0),
         ("IWM 20d RS vs SPY > 0 (risk-on)", lambda t: d10(t) in rs and rs[d10(t)] > 0),
         ("IWM 20d RS vs SPY < 0", lambda t: d10(t) in rs and rs[d10(t)] <= 0)]
    print("variants tried:", len(V) + 1)
    for name, ok in V:
        row(name, [t for t in live if ok(t)], kw, cut)
