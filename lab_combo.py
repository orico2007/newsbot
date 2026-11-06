"""Combined test of the two best lab findings on champion entries: breadth filter (>=10% of universe with RSI2<10) and ranking by weakest sector peers. Backtest only."""
import datetime, copy
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
    br = lambda t: B.get(t["t"][:10], (0, 0))[0]
    m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    def ranked(ts):
        out = []
        for t in ts:
            u = dict(t); u["score"] = -m3(t); out.append(u)
        return out
    row("CHAMPION", champ, kw, cut)
    row("breadth>=10% filter", [t for t in champ if br(t) >= .10], kw, cut)
    row("rank by weakest sector peers", ranked(champ), kw, cut)
    row("breadth>=10% filter + rank weakest peers", ranked([t for t in champ if br(t) >= .10]), kw, cut)
    row("breadth>=10% + peers 3d<0 filter", [t for t in champ if br(t) >= .10 and m3(t) < 0], kw, cut)
    row("breadth>=10% + peers 3d<0 + rank", ranked([t for t in champ if br(t) >= .10 and m3(t) < 0]), kw, cut)
