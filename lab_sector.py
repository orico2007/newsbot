"""Lab idea 2026-11-05 (run 7): sector-relative reversion filter on champion entries (own idea; idiosyncratic vs sector-wide drops). Backtest only."""
import datetime
import lab, sweep, challenger, market
import portfolio_test as PT
from lab_52wh import row

def feats(AS):
    """Per (sym, date): peer-mean 3d/20d return in the same sector (self excluded), share of peers above SMA50."""
    sec = {}
    for s in AS:
        sec.setdefault(market.SECTOR_OF.get(s), []).append(s)
    ix = {s: {t: i for i, t in enumerate(A["t"])} for s, A in AS.items()}
    F = {}
    for s, A in AS.items():
        peers = [p for p in sec.get(market.SECTOR_OF.get(s), []) if p != s]
        if len(peers) < 2: continue
        for i in range(25, len(A["c"])):
            d = A["t"][i]; r3, r20, ab = [], [], []
            for p in peers:
                j = ix[p].get(d)
                if j is None or j < 25: continue
                B = AS[p]; r3.append(B["c"][j] / B["c"][j-3] - 1); r20.append(B["c"][j] / B["c"][j-20] - 1)
                if B["s50"][j]: ab.append(B["c"][j] > B["s50"][j])
            if len(r3) < 2 or not ab: continue
            m3 = sum(r3) / len(r3) * 100
            F[(s, d)] = dict(m3=m3, m20=sum(r20) / len(r20) * 100, ab=sum(ab) / len(ab), idio=(A["c"][i] / A["c"][i-3] - 1) * 100 - m3)
    return F

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); F = feats(AS)
    row("CHAMPION", champ, kw, cut)
    print("champ trades with sector features:", sum(1 for t in champ if (t["sym"], t["t"]) in F), "of", len(champ))
    g = lambda t: F.get((t["sym"], t["t"]))
    V = [("idio 3d < -3% (stock-specific drop)", lambda f: f["idio"] < -3),
         ("idio 3d >= -3% (sector-wide drop)", lambda f: f["idio"] >= -3),
         ("idio 3d < -1.5%", lambda f: f["idio"] < -1.5),
         ("peers 3d < -1% (sector also weak)", lambda f: f["m3"] < -1),
         ("peers 20d > 0 (strong sector)", lambda f: f["m20"] > 0),
         ("peers 20d <= 0 (weak sector)", lambda f: f["m20"] <= 0),
         ("weakest in strong sector: idio<-3 & m20>0", lambda f: f["idio"] < -3 and f["m20"] > 0),
         ("peers >=50% above SMA50", lambda f: f["ab"] >= 0.5)]
    print("variants tried:", len(V))
    for n, fn in V:
        row(n, [t for t in champ if g(t) and fn(g(t))], kw, cut)
