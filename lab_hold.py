"""Lab run 14 (web idea: Quantpedia AI pullback article, short holds + vol-targeted sizing): short max-hold and ATR-scaled sizing on the NEW live setup (breadth>=10% + weakest-peer rank). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats
from lab_fearsize import curve

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    B = breadth_series(AS); F = feats(AS)
    def live(**k):
        T = PT.gen(AS, ctx, challenger.ruleset(**k)); out = []
        for t in T:
            if B.get(t["t"][:10], (0, 0))[0] < .10: continue
            f = F.get((t["sym"], t["t"]))
            out.append(dict(t, score=-f["m3"]) if f else t)
        return out
    print("variants tried: 6 (5 hold/exit + 2 sizing post-hoc)")
    for nm, k in [("LIVE hold 7 (ref)", {}), ("hold 1", dict(hold=1)), ("hold 2", dict(hold=2)), ("hold 3", dict(hold=3)), ("hold 5", dict(hold=5)), ("hold 10", dict(hold=10))]:
        row(nm, live(**k), kw, cut)
    taken = lab.portfolio(live(), **kw)["trades"]
    idx = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    def atrp(t):
        A = AS[t["sym"]]; i = idx[t["sym"]].get(t["t"][:10]); 
        return (A["atr"][i] / A["c"][i] * 100) if i is not None and A["atr"][i] else 3.0
    print("median ATR%", sorted(atrp(t) for t in taken)[len(taken) // 2])
    for nm, m in [("flat", lambda t: 1), ("vol-target size = 2.5/ATR%, cap 1.5x", lambda t: min(1.5, 2.5 / atrp(t))),
                  ("vol-target 2.5/ATR%, cap 1.0x", lambda t: min(1.0, 2.5 / atrp(t)))]:
        print(f"{nm:40}", curve(taken, m))
    for lo, hi in [("2021", "2023"), ("2024", "2026")]:
        s = [t for t in taken if lo <= t["t"][:4] <= hi]
        print(lo, hi, "flat", curve(s, lambda t: 1)[:3], "vt1.5", curve(s, lambda t: min(1.5, 2.5 / atrp(t)))[:3])
