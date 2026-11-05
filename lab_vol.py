"""Lab idea 2026-11-05 (run 6): volume-conditioned short-term reversal (Avramov/Chordia/Goyal 2006; Cooper 1999). Filter champion entries by signal-day volume ratio; backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); row("CHAMPION", champ, kw, cut)
    idx = {s: {t: i for i, t in enumerate(A["t"])} for s, A in AS.items()}
    def vr(t):
        A = AS[t["sym"]]; i = idx[t["sym"]][t["t"]]
        return A["v"][i] / A["vavg"][i] if A["vavg"][i] else None
    def dv(t):  # 3-day avg volume ratio (declining volume into the drop?)
        A = AS[t["sym"]]; i = idx[t["sym"]][t["t"]]
        return sum(A["v"][i-2:i+1]) / 3 / A["vavg"][i] if A["vavg"][i] else None
    print(champ[0].keys())
    V = [("vol ratio < 0.8", lambda t: (vr(t) or 9) < 0.8), ("vol ratio < 1.0", lambda t: (vr(t) or 9) < 1.0),
         ("vol ratio >= 1.0", lambda t: (vr(t) or 0) >= 1.0), ("vol ratio >= 1.5", lambda t: (vr(t) or 0) >= 1.5),
         ("vol ratio >= 2.0", lambda t: (vr(t) or 0) >= 2.0), ("3d avg vol < 1.0x", lambda t: (dv(t) or 9) < 1.0),
         ("3d avg vol >= 1.3x", lambda t: (dv(t) or 0) >= 1.3)]
    print("variants tried:", len(V))
    for n, f in V:
        row(n, [t for t in champ if f(t)], kw, cut)
