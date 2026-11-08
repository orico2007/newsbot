"""Lab run 31 (own idea; follow-up of runs 11/13): size of the bear-regime sleeve (10% / 7.5% / 5% / 0) on top of the LIVE setup. Sleeve pnl scaled post-hoc (weight multiplier); slots still count one per trade. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats
from lab_bear import bear_long

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); B = breadth_series(AS); F = feats(AS)
    br = lambda t: B.get(t["t"][:10], (0, 0))[0]
    m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    rk = lambda ts, w=1.0: [dict(t, score=-m3(t), pnl_pct=t["pnl_pct"] * w) for t in ts]
    live = rk([t for t in champ if br(t) >= .10]); bear = [t for t in bear_long(AS, ctx) if br(t) >= .10]
    print("variants tried: 4 (+2 splits)")
    row("LIVE", live, kw, cut)
    for w in (1.0, .75, .5):
        row(f"LIVE + sleeve w={w}", live + rk(bear, w), kw, cut)
    for nm, sub in (("2021-23", lambda t: t["t"][:4] <= "2023"), ("2024-26", lambda t: t["t"][:4] >= "2024")):
        row("split LIVE " + nm, [t for t in live if sub(t)], kw, cut)
        row("split LIVE+sleeve.5 " + nm, [t for t in live + rk(bear, .5) if sub(t)], kw, cut)
