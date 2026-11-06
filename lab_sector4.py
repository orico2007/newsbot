"""Lab run 9: cross-check run 7/8 sector-peer filter using the sector ETFs (XL*, SMH, XBI) instead of peer averages, to rule out a survivor-universe artifact. Backtest only."""
import datetime
import lab, sweep, challenger, market
import portfolio_test as PT
from lab_52wh import row
from lab_sector import feats

def etf_feats(bars, syms):
    out = {}
    for s in syms:
        e = market.SECTOR_OF.get(s)
        B = bars.get(e)
        if not B or e in out: continue
        c = [b["c"] for b in B]; t = [b["t"] for b in B]
        out[e] = {t[i]: (c[i] / c[i-3] - 1) * 100 for i in range(20, len(c))}, {t[i]: (c[i] / c[i-20] - 1) * 100 for i in range(20, len(c))}
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); bars = lab.load_bars(); spy = bars["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); F = feats(AS); E = etf_feats(bars, AS)
    print("ETFs available:", sorted(E))
    def e3(t):
        e = market.SECTOR_OF.get(t["sym"]); return E[e][0].get(t["t"]) if e in E else None
    def e20(t):
        e = market.SECTOR_OF.get(t["sym"]); return E[e][1].get(t["t"]) if e in E else None
    g = lambda t: F.get((t["sym"], t["t"]))
    have = [t for t in champ if e3(t) is not None and e20(t) is not None and g(t)]
    print("trades with both ETF and peer features:", len(have), "of", len(champ))
    row("CHAMPION (all)", champ, kw, cut)
    row("CHAMPION (same subset)", have, kw, cut)
    row("ETF 3d<0", [t for t in have if e3(t) < 0], kw, cut)
    row("ETF 3d<0 & ETF 20d>0", [t for t in have if e3(t) < 0 and e20(t) > 0], kw, cut)
    row("peers 3d<0 & 20d>0 (run 8 ref)", [t for t in have if g(t)["m3"] < 0 and g(t)["m20"] > 0], kw, cut)
    row("ETF AND peers 3d<0 & 20d>0", [t for t in have if e3(t) < 0 and e20(t) > 0 and g(t)["m3"] < 0 and g(t)["m20"] > 0], kw, cut)
    row("ETF 3d<0 but peers 3d>=0", [t for t in have if e3(t) < 0 and g(t)["m3"] >= 0], kw, cut)
    row("ETF 3d>=0 (sector up)", [t for t in have if e3(t) >= 0], kw, cut)
    row("ETF 3d>=0 & 20d>0 (control)", [t for t in have if e3(t) >= 0 and e20(t) > 0], kw, cut)
    print("variants tried: 7")
