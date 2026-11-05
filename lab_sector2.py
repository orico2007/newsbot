"""Lab run 7b: robustness of the 'sector peers weak' filter (neighbour thresholds, and as priority rank rather than hard filter). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_sector import feats

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); F = feats(AS)
    g = lambda t: F.get((t["sym"], t["t"]))
    row("CHAMPION", champ, kw, cut)
    for th in (0, -0.5, -1, -1.5, -2, -3):
        row(f"peers 3d < {th}%", [t for t in champ if g(t)["m3"] < th], kw, cut)
    # soft: keep all trades but rank sector-weak first (rule tier kept? pure rank by -m3)
    T = []
    for t in champ:
        u = dict(t); u["score"] = -g(t)["m3"]; T.append(u)
    row("rank by weakest peers first (no filter)", T, kw, cut)
    T = []
    for t in champ:
        u = dict(t); u["score"] = t["score"] * 1e6 + (-g(t)["m3"]); T.append(u)
    row("rank within rule tier by weak peers", T, kw, cut)
    print("variants (this script):", 8, "; total this run 16")
