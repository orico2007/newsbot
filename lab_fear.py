"""Lab idea 2026-11-05: market-fear filter on champion entries (skip when SPY fell sharply / is stretched below its 5-day high). Backtest only."""
import datetime
import lab, research, sweep, challenger
import portfolio_test as PT
from lab_52wh import row

def spy_feats():
    spy = lab.load_bars()["SPY"]; f = {}
    for i in range(10, len(spy)):
        c = spy[i]["c"]; d1 = (c / spy[i-1]["c"] - 1) * 100; d3 = (c / spy[i-3]["c"] - 1) * 100
        dd5 = (c / max(b["c"] for b in spy[i-5:i+1]) - 1) * 100
        f[spy[i]["t"][:10]] = (d1, d3, dd5)
    return f

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); F = spy_feats()
    print("sample t:", champ[0]["t"], "keys", list(champ[0])[:12])
    row("CHAMPION", champ, kw, cut)
    V = [("skip if SPY 1d < -1%", lambda x: x[0] >= -1.0),
         ("skip if SPY 1d < -2%", lambda x: x[0] >= -2.0),
         ("skip if SPY 3d < -3%", lambda x: x[1] >= -3.0),
         ("skip if SPY >3% below 5d high", lambda x: x[2] >= -3.0),
         ("ONLY if SPY 3d < -1% (fear helps?)", lambda x: x[1] < -1.0)]
    print("variants tried:", len(V))
    for name, ok in V:
        T = [t for t in champ if t["t"][:10] in F and ok(F[t["t"][:10]])]
        row(name, T, kw, cut)
