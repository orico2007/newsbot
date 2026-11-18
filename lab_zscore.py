"""Lab run 44 (2026-11-18): Bollinger-style z-score of close vs 20d mean/std (and 20d linear-regression residual z) as conditioner of the vol60>=1.75% LIVE setup. Web-seeded (algomatictrading linear-regression mean reversion). Backtest only."""
import datetime, statistics as S
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def z20(A, i):
    w = A["c"][i-19:i+1]; sd = S.pstdev(w)
    return (A["c"][i] - sum(w)/20) / sd if sd else 0
def zreg(A, i, n=20):
    y = A["c"][i-n+1:i+1]; x = list(range(n)); mx = (n-1)/2; my = sum(y)/n
    b = sum((a-mx)*(c-my) for a, c in zip(x, y)) / sum((a-mx)**2 for a in x)
    res = [c - (my + b*(a-mx)) for a, c in zip(x, y)]; sd = S.pstdev(res)
    return res[-1]/sd if sd else 0

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(spy) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    champ = PT.gen(AS, ctx, challenger.ruleset()); live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            v = challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10]))
            if v is not None and v >= 1.75: live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0)))
    row("LIVE ref", live, kw, cut)
    for t in live:
        A = AS[t["sym"]]; i = IX[t["sym"]][t["t"][:10]]; t["z"] = z20(A, i); t["zr"] = zreg(A, i)
    zs = sorted(t["z"] for t in live); print("z20 quartiles", [round(zs[int(len(zs)*q)], 2) for q in (.25, .5, .75)])
    n = 0
    for k, lab_ in (("z", "z20"), ("zr", "zreg20")):
        for th in (-1.5, -2.0):
            for nm, f in ((f"{lab_} < {th}", lambda t: t[k] < th), (f"{lab_} >= {th}", lambda t: t[k] >= th)):
                sub = [t for t in live if f(t)]; n += 1
                if len(sub) > 15: row(nm, sub, kw, cut)
                else: print(nm, "n=", len(sub))
    print("variants tried:", n)
