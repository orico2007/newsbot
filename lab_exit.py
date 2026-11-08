"""Lab run 25 (2026-11-08): exit-rule variants (Connors RSI2>70, MA10, pure time) on the LIVE setup. Backtest only."""
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
    B = breadth_series(AS); F = feats(AS)
    m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    V = [("LIVE ref (prevhl, hold7)", {}), ("exit RSI2>70, hold7", dict(exit_="rsi2", hold=7)),
         ("exit RSI2>70, hold10", dict(exit_="rsi2", hold=10)), ("exit MA10, hold12", dict(exit_="ma10", hold=12)),
         ("exit MA5, hold7", dict(exit_="ma5", hold=7)), ("no signal exit, time 7", dict(exit_="none", hold=7))]
    print("variants tried:", len(V))
    for n, k in V:
        champ = PT.gen(AS, ctx, challenger.ruleset(**k)); live = []
        for t in champ:
            if B.get(t["t"][:10], (0, 0))[0] >= .10:
                u = dict(t); u["score"] = -m3(t); live.append(u)
        row(n, live, kw, cut)
