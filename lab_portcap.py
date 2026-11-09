"""Lab run 34 (own idea): position-count / per-day-cap / size grid on the NEW live setup (breadth>=10% + weakest-peer rank). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); B = breadth_series(AS); F = feats(AS)
    br = lambda t: B.get(t["t"][:10], (0, 0))[0]
    m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    T = []
    for t in champ:
        if br(t) >= .10:
            u = dict(t); u["score"] = -m3(t); T.append(u)
    grid = [(10,12,4),(10,12,2),(10,12,3),(10,12,6),(10,8,4),(10,16,4),(8,12,4),(12,12,4),(15,8,4),(7,16,4),(10,20,6)]
    print("variants tried:", len(grid))
    for s, m, d in grid:
        row(f"size {s}% x {m} pos, {d}/day", T, dict(size_pct=s, max_pos=m, per_day=d), cut)
