"""Lab run 29 (2026-11-11): earnings-proximity proxy (volume+gap spikes, ~63d periodicity) on the LIVE vol60>=1.75% setup. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth
from lab_sector import feats

def spikes(A):
    c, o, v, va = A["c"], A["o"], A["v"], A["vavg"]; out = []; last = -99
    for i in range(21, len(c)):
        if not va[i - 1]: continue
        big = v[i] >= 2.5 * va[i - 1] and (abs(o[i] / c[i - 1] - 1) >= 0.03 or abs(c[i] / c[i - 1] - 1) >= 0.05)
        if big and i - last > 15: out.append(i); last = i
    return out

def flags(A, i, SP, lo=60, hi=67, win=8):
    """pred: a spike 60-67 trading days ago would put next report inside (i, i+win]; real: spike inside (i, i+7] (look-ahead)"""
    pred = any(lo <= (i + d) - s <= hi for s in SP if s < i for d in range(1, win + 1))
    real = any(i < s <= i + 7 for s in SP)
    return pred, real

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = challenger.DEF_PORT
    B = lab_breadth.breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    SPK = {s: spikes(A) for s, A in AS.items()}
    print("avg spikes per symbol", sum(len(x) for x in SPK.values()) / len(SPK))
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    base = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10]
    live = [t for t in base if (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))]
    fl = {id(t): flags(AS[t["sym"]], IX[t["sym"]][t["t"][:10]], SPK[t["sym"]]) for t in live}
    fb = {id(t): flags(AS[t["sym"]], IX[t["sym"]][t["t"][:10]], SPK[t["sym"]]) for t in base}
    print("live n", len(live), "pred flagged", sum(fl[id(t)][0] for t in live), "real flagged", sum(fl[id(t)][1] for t in live))
    for nm, T, F_ in (("LIVE vol175", live, fl), ("BASE novol", base, fb)):
        row(nm, T, kw, cut)
        row(nm + " | skip predicted-earnings", [t for t in T if not F_[id(t)][0]], kw, cut)
        row(nm + " | only predicted-earnings", [t for t in T if F_[id(t)][0]], kw, cut)
        row(nm + " | skip real-earnings (look-ahead)", [t for t in T if not F_[id(t)][1]], kw, cut)
        row(nm + " | only real-earnings (look-ahead)", [t for t in T if F_[id(t)][1]], kw, cut)
