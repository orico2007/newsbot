"""Lab run 42 (2026-11-13): exit-rule variants (RSI2>70, close>SMA5, close>SMA10, prior-high OR rsi2>70) re-tested on the NEW live vol60>=1.75% setup. Own idea (run 25 was on the old setup). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from sweep import SLIP, rsi_wilder, sma_arr
from lab_52wh import row
import lab_breadth
from lab_sector import feats

def make_sim(mode=None):
    cache = {}
    def sim(A, i, side, stop_k, exit_mode, hold):
        c, h, l, o = A["c"], A["h"], A["l"], A["o"]; n = len(c); atr = A["atr"][i]
        if not atr or side != "long" or mode is None: return sweep.sim(A, i, side, stop_k, exit_mode, hold)
        key = id(A)
        if key not in cache: cache[key] = (rsi_wilder(c, 2), sma_arr(c, 5), sma_arr(c, 10))
        r2, m5, m10 = cache[key]
        entry = c[i] * (1 + SLIP / 100); stop = entry - stop_k * atr
        last = min(n - 1, i + hold)
        if last <= i: return None
        px, jx = None, last
        for j in range(i + 1, last + 1):
            if o[j] <= stop: px = o[j]; jx = j; break
            if l[j] <= stop: px = stop; jx = j; break
            ph = c[j] > h[j-1]
            if mode == "rsi70" and r2[j] is not None and r2[j] > 70: px = c[j]; jx = j; break
            if mode == "ph_or_rsi70" and (ph or (r2[j] is not None and r2[j] > 70)): px = c[j]; jx = j; break
            if mode == "ma5" and m5[j] is not None and c[j] > m5[j]: px = c[j]; jx = j; break
            if mode == "ma10" and m10[j] is not None and c[j] > m10[j]: px = c[j]; jx = j; break
            if mode == "ph_and_ma5" and ph and m5[j] is not None and c[j] > m5[j]: px = c[j]; jx = j; break
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
    V = ["LIVE ref", "rsi70", "ph_or_rsi70", "ma5", "ma10", "ph_and_ma5"]
    print("variants tried:", len(V))
    for n in V:
        PT.sim = make_sim(None if n == "LIVE ref" else n); T0 = PT.gen(AS, ctx, challenger.ruleset())
        live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
                for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
        row(n, live, kw, cut)
