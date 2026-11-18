"""Lab run 44b: robustness plateau of the regression-residual z filter (window and threshold). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats
from lab_zscore import zreg
if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(spy) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            v = challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10]))
            if v is not None and v >= 1.75: live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0)))
    n = 0
    for W in (10, 20, 30, 60):
        for t in live:
            i = IX[t["sym"]][t["t"][:10]]; t["z"] = zreg(AS[t["sym"]], i, W)
        for th in (-1.0, -1.25, -1.5, -1.75):
            sub = [t for t in live if t["z"] < th]; n += 1
            row(f"zreg{W} < {th}", sub, kw, cut)
    print("variants:", n)
