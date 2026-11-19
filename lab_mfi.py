"""Lab run 49 (2026-11-19): money-flow (MFI-3) / OBV / down-volume-share conditioners of the vol60>=1.75% LIVE setup
(web-seeded: Connors RSI2 / scaling-in search results; MFI/OBV never tested in earlier runs). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth

def mfi(A, i, n):
    pos = neg = 0.0
    for k in range(i - n + 1, i + 1):
        tp = (A["h"][k] + A["l"][k] + A["c"][k]) / 3; tp0 = (A["h"][k-1] + A["l"][k-1] + A["c"][k-1]) / 3
        mf = tp * A["v"][k]
        if tp > tp0: pos += mf
        elif tp < tp0: neg += mf
    return 100 * pos / (pos + neg) if pos + neg else 50
def obv_chg(A, i, n):
    s = 0.0; vs = 0.0
    for k in range(i - n + 1, i + 1):
        d = A["c"][k] - A["c"][k-1]; s += A["v"][k] * (1 if d > 0 else -1 if d < 0 else 0); vs += A["v"][k]
    return s / vs if vs else 0
def dnvol(A, i, n):
    d = t = 0.0
    for k in range(i - n + 1, i + 1):
        t += A["v"][k]
        if A["c"][k] < A["c"][k-1]: d += A["v"][k]
    return d / t if t else 0.5

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    BR = lab_breadth.breadth_series(AS); T0 = PT.gen(AS, ctx, challenger.ruleset())
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [t for t in T0 if BR.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    row("LIVE ref", live, kw, cut)
    def F(fn):
        out = []
        for t in live:
            i = IX[t["sym"]].get(t["t"][:10]); A = AS[t["sym"]]
            if i and i > 12 and fn(A, i): out.append(t)
        return out
    V = [("MFI3 < 20", lambda A, i: mfi(A, i, 3) < 20), ("MFI3 >= 20", lambda A, i: mfi(A, i, 3) >= 20),
         ("MFI5 < 30", lambda A, i: mfi(A, i, 5) < 30), ("MFI5 >= 30", lambda A, i: mfi(A, i, 5) >= 30),
         ("OBV5 net flow < -0.2", lambda A, i: obv_chg(A, i, 5) < -0.2), ("OBV5 net flow >= -0.2", lambda A, i: obv_chg(A, i, 5) >= -0.2),
         ("down-vol share 5d > 0.7", lambda A, i: dnvol(A, i, 5) > 0.7), ("down-vol share 5d <= 0.7", lambda A, i: dnvol(A, i, 5) <= 0.7)]
    print("variants tried:", len(V))
    for n, fn in V: row(n, F(fn), kw, cut)
