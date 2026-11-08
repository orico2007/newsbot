"""Lab run 27 (2026-11-08): Bollinger %B and ATR-normalised drop filters on the LIVE setup (web idea: Connors %B strategy). Backtest only."""
import datetime, statistics
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def pctb(AS, t):
    A = AS[t["sym"]]
    try: i = A["t"].index(t["t"])
    except ValueError: return None
    if i < 25: return None
    w = A["c"][i-19:i+1]; m = sum(w)/20; sd = statistics.pstdev(w)
    return None if sd == 0 else (A["c"][i] - (m - 2*sd)) / (4*sd)

def drop_atr(AS, t):
    """5-day close decline in units of 14d mean absolute close change."""
    A = AS[t["sym"]]
    try: i = A["t"].index(t["t"])
    except ValueError: return None
    if i < 20: return None
    c = A["c"]; a = sum(abs(c[j]-c[j-1]) for j in range(i-13, i+1))/14
    return None if a == 0 else (c[i-5] - c[i]) / a

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); B = breadth_series(AS); F = feats(AS)
    m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            u = dict(t); u["score"] = -m3(t); u["b"] = pctb(AS, t); u["d"] = drop_atr(AS, t); live.append(u)
    row("LIVE ref", live, kw, cut)
    ok = [t for t in live if t["b"] is not None and t["d"] is not None]; print("with feats:", len(ok), "of", len(live))
    import numpy as np
    print("pctb quantiles", np.percentile([t["b"] for t in ok], [10,25,50,75,90]).round(2), "drop quantiles", np.percentile([t["d"] for t in ok], [10,25,50,75,90]).round(2))
    V = [("%B<0 (below lower band)", lambda t: t["b"] < 0), ("%B<0.1", lambda t: t["b"] < .1), ("%B>=0.1", lambda t: t["b"] >= .1),
         ("5d drop >=4 avg-moves", lambda t: t["d"] >= 4), ("5d drop >=6", lambda t: t["d"] >= 6), ("5d drop <6", lambda t: t["d"] < 6)]
    print("variants tried:", len(V))
    for n, fn in V: row(n, [t for t in ok if fn(t)], kw, cut)
    for lab_, f in (("rank biggest 5d drop first", lambda t: t["d"]), ("rank lowest %B first", lambda t: -t["b"])):
        T = []
        for t in ok:
            u = dict(t); u["score"] = f(t); T.append(u)
        row(lab_, T, kw, cut)
