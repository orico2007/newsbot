"""Lab run 33 (2026-11-12): no-bounce time stop (exit at close of day k if still below entry) and day-1 weakness exit on the LIVE vol60>=1.75% setup. Own idea. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from sweep import SLIP
from lab_52wh import row
import lab_breadth
from lab_sector import feats

def make_sim(k=None, thr=0.0):
    """After day k's close, if close < entry*(1+thr/100) exit at that close. Otherwise live rules (stop, close>prior high, hold)."""
    def sim(A, i, side, stop_k, exit_mode, hold):
        c, h, l, o = A["c"], A["h"], A["l"], A["o"]; n = len(c); atr = A["atr"][i]
        if not atr or side != "long" or k is None: return sweep.sim(A, i, side, stop_k, exit_mode, hold)
        entry = c[i] * (1 + SLIP / 100); stop = entry - stop_k * atr
        last = min(n - 1, i + hold)
        if last <= i: return None
        px, jx = None, last
        for j in range(i + 1, last + 1):
            if o[j] <= stop: px = o[j]; jx = j; break
            if l[j] <= stop: px = stop; jx = j; break
            if exit_mode == "prevhl" and c[j] > h[j-1]: px = c[j]; jx = j; break
            if j - i == k and c[j] < entry * (1 + thr / 100): px = c[j]; jx = j; break
        if px is None: px = c[last]
        px *= (1 - SLIP / 100); pnl = (px - entry) / entry * 100
        return {"t": A["t"][i], "te": A["t"][jx], "pnl_pct": pnl, "R": pnl / (stop_k * atr / entry * 100), "held": jx - i}
    return sim

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    B = lab_breadth.breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    V = [("LIVE ref", {}), ("day2 close<entry -> exit", dict(k=2)), ("day3 close<entry -> exit", dict(k=3)),
         ("day4 close<entry -> exit", dict(k=4)), ("day3 close<entry-1% -> exit", dict(k=3, thr=-1.0))]
    print("variants tried:", len(V))
    for n, kk in V:
        PT.sim = make_sim(**kk); T0 = PT.gen(AS, ctx, challenger.ruleset())
        live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
                for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
        row(n, live, kw, cut)
