"""Lab run 22 (2026-11-15): market-conditioned exits on the LIVE vol60>=1.75% setup (own idea; exit tied to SPY's state, not the stock's).
Modes: 'hold_washout' = ignore the stock's prior-high exit while SPY RSI2 < 10 (market still washed out); 'spy_bounce' = also exit when SPY RSI2 > 70 / 80;
'spy_up' = take the prior-high exit only if SPY closed up that day. Max-hold 7 and 4 ATR stop unchanged. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from sweep import SLIP, rsi_wilder
from lab_52wh import row
import lab_breadth
from lab_sector import feats

def make_sim(mode, SP):
    def sim(A, i, side, stop_k, exit_mode, hold):
        c, h, l, o = A["c"], A["h"], A["l"], A["o"]; n = len(c); atr = A["atr"][i]
        if not atr or side != "long" or mode is None: return sweep.sim(A, i, side, stop_k, exit_mode, hold)
        entry = c[i] * (1 + SLIP / 100); stop = entry - stop_k * atr
        last = min(n - 1, i + hold)
        if last <= i: return None
        px, jx = None, last
        for j in range(i + 1, last + 1):
            if o[j] <= stop: px = o[j]; jx = j; break
            if l[j] <= stop: px = stop; jx = j; break
            ph = c[j] > h[j-1]; s = SP.get(A["t"][j][:10])
            if s is None: s = (50, 0)
            r2, ret = s
            if mode == "hold_washout" and ph and r2 >= 10: px = c[j]; jx = j; break
            if mode == "hold_washout20" and ph and r2 >= 20: px = c[j]; jx = j; break
            if mode == "spy_bounce70" and (ph or r2 > 70): px = c[j]; jx = j; break
            if mode == "spy_bounce80" and (ph or r2 > 80): px = c[j]; jx = j; break
            if mode == "spy_up" and ph and ret > 0: px = c[j]; jx = j; break
            if mode == "spy_dn_ok" and ph and ret <= 0: px = c[j]; jx = j; break  # control: opposite
        if px is None: px = c[last]
        px *= (1 - SLIP / 100); pnl = (px - entry) / entry * 100
        return {"t": A["t"][i], "te": A["t"][jx], "pnl_pct": pnl, "R": pnl / (stop_k * atr / entry * 100), "held": jx - i}
    return sim

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); sp = lab.load_bars()["SPY"]; last = sp[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    cl = [b["c"] for b in sp]; r2 = rsi_wilder(cl, 2)
    SP = {sp[k]["t"][:10]: (r2[k] if r2[k] is not None else 50, (cl[k] / cl[k-1] - 1) * 100 if k else 0) for k in range(len(sp))}
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    B = lab_breadth.breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    V = ["LIVE ref", "hold_washout", "hold_washout20", "spy_bounce70", "spy_bounce80", "spy_up", "spy_dn_ok"]
    print("variants tried:", len(V))
    for n in V:
        PT.sim = make_sim(None if n == "LIVE ref" else n, SP); T0 = PT.gen(AS, ctx, challenger.ruleset())
        live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
                for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
        row(n, live, kw, cut)
