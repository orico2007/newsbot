"""Lab run 13 (own idea): bear-regime long sleeve on top of the NEW live setup (breadth>=10% filter + weakest-sector-peer rank), with the breadth filter applied to the sleeve too. Backtest only."""
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
    def ranked(ts):
        out = []
        for t in ts:
            u = dict(t); u["score"] = -m3(t); out.append(u)
        return out
    live = ranked([t for t in champ if br(t) >= .10])
    bear = bear_long(AS, ctx)
    print("bear sleeve n:", len(bear), "variants tried: 6")
    row("OLD champion", champ, kw, cut)
    row("NEW LIVE (breadth+rank)", live, kw, cut)
    row("bear sleeve alone", ranked(bear), kw, cut)
    row("bear sleeve alone, breadth>=10%", ranked([t for t in bear if br(t) >= .10]), kw, cut)
    row("bear sleeve alone, breadth>=20%", ranked([t for t in bear if br(t) >= .20]), kw, cut)
    row("LIVE + bear (no breadth on sleeve)", live + ranked(bear), kw, cut)
    row("LIVE + bear breadth>=10%", live + ranked([t for t in bear if br(t) >= .10]), kw, cut)
    row("LIVE + bear breadth>=20%", live + ranked([t for t in bear if br(t) >= .20]), kw, cut)
    bb = [t for t in bear if br(t) >= .10]
    for nm, sub in (("2021-23", lambda t: t["t"][:4] <= "2023"), ("2024-26", lambda t: t["t"][:4] >= "2024")):
        row("split LIVE+bear10 " + nm, [t for t in live + ranked(bb) if sub(t)], kw, cut)
        row("split LIVE " + nm, [t for t in live if sub(t)], kw, cut)
