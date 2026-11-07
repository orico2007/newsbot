"""Lab run 18 (2026-11-07): weekday-of-signal seasonality within the LIVE setup (breadth>=10% + weakest-peer rank). Backtest only."""
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
    wd = lambda t: datetime.date.fromisoformat(t["t"][:10]).weekday()
    row("LIVE (breadth+rank)", live, kw, cut)
    names = "Mon Tue Wed Thu Fri".split()
    for d in range(5):
        row(f"signal day only {names[d]}", [t for t in live if wd(t) == d], kw, cut)
    for d in range(5):
        row(f"skip signal day {names[d]}", [t for t in live if wd(t) != d], kw, cut)
