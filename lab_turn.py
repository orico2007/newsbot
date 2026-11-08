"""Lab run 32 (2026-11-08): market-state timing of the LIVE setup: SPY direction on signal day and breadth deepening vs easing. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); B = breadth_series(AS); F = feats(AS)
    m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            u = dict(t); u["score"] = -m3(t); live.append(u)
    dates = [x["t"][:10] for x in spy]; sc = [x["c"] for x in spy]; ix = {d: i for i, d in enumerate(dates)}
    bd = sorted(B); bi = {d: i for i, d in enumerate(bd)}
    def spy_r(t, n):
        i = ix.get(t["t"][:10]); return None if i is None or i < n else sc[i]/sc[i-n]-1
    def bchg(t, n=1):
        i = bi.get(t["t"][:10]); return None if i is None or i < n else B[bd[i]][0]-B[bd[i-n]][0]
    kw_ = kw
    row("LIVE ref", live, kw, cut)
    V = [("SPY up on signal day", lambda t: (spy_r(t,1) or 0) > 0),
         ("SPY down on signal day", lambda t: (spy_r(t,1) or 0) <= 0),
         ("breadth easing (today<yesterday)", lambda t: (bchg(t,1) or 0) < 0),
         ("breadth deepening (today>=yesterday)", lambda t: (bchg(t,1) or 0) >= 0),
         ("SPY 3d return < -2%", lambda t: (spy_r(t,3) or 0) < -.02),
         ("SPY 3d return >= -2%", lambda t: (spy_r(t,3) or 0) >= -.02)]
    print("variants tried:", len(V)+1)
    for n, fn in V:
        S = [t for t in live if fn(t)]
        row(n, S, kw, cut)
        h = [t for t in S if t["t"][:4] <= "2023"]; l = [t for t in S if t["t"][:4] >= "2024"]
        print("   split <=2023 n=%d | >=2024 n=%d" % (len(h), len(l)))
