"""Lab run 21 (2026-11-07): month-of-year seasonality within the LIVE setup. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def pf(ts):
    w = sum(t["pnl_pct"] for t in ts if t["pnl_pct"] > 0); l = -sum(t["pnl_pct"] for t in ts if t["pnl_pct"] <= 0)
    return round(w / l, 2) if l else 99

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
    print(list(live[0].keys()))
    mo = lambda t: int(t["t"][5:7]); yr = lambda t: int(t["t"][:4])
    row("LIVE (breadth+rank)", live, kw, cut)
    print("month: n / PF all / PF 2021-23 / PF 2024-26")
    for m in range(1, 13):
        a = [t for t in live if mo(t) == m]
        print(m, len(a), pf(a), pf([t for t in a if yr(t) <= 2023]), pf([t for t in a if yr(t) >= 2024]))
    # walk-forward: pick 3 worst months on 2021-23 (excl 2022 weirdness included), skip, test 2024-26
    sel = [t for t in live if yr(t) <= 2023]
    worst = sorted(range(1, 13), key=lambda m: pf([t for t in sel if mo(t) == m]) if [t for t in sel if mo(t) == m] else 99)[:3]
    print("worst3 on 2021-23:", worst)
    row("skip worst3 (chosen 2021-23)", [t for t in live if mo(t) not in worst], kw, cut)
    row("skip Sep (literature weak month)", [t for t in live if mo(t) != 9], kw, cut)
    row("skip Sep+Oct", [t for t in live if mo(t) not in (9, 10)], kw, cut)
    row("skip Jan-Feb (Jan reversal-weak)", [t for t in live if mo(t) not in (1, 2)], kw, cut)
