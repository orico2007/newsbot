"""Lab run 32 (2026-11-16): profit-lock exits (breakeven stop / ATR trailing stop after a gain) on the LIVE vol60>=1.75% setup. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from sweep import SLIP, rsi_wilder, sma_arr
from lab_52wh import row
import lab_breadth
from lab_sector import feats

def make_sim(mode=None):
    """Prior-high exit (live) + a profit-lock stop. mode=(kind, trigger_ATR, trail_ATR). kind 'be' = move stop to entry once close>=entry+trigger*ATR;
    'trail' = once armed, stop = highest close since entry - trail*ATR."""
    def sim(A, i, side, stop_k, exit_mode, hold):
        c, h, l, o = A["c"], A["h"], A["l"], A["o"]; n = len(c); atr = A["atr"][i]
        if not atr or side != "long" or mode is None: return sweep.sim(A, i, side, stop_k, exit_mode, hold)
        kind, trig, tr = mode
        entry = c[i] * (1 + SLIP / 100); stop = entry - stop_k * atr
        last = min(n - 1, i + hold)
        if last <= i: return None
        px, jx = None, last; hi = c[i]; armed = False
        for j in range(i + 1, last + 1):
            if o[j] <= stop: px = o[j]; jx = j; break
            if l[j] <= stop: px = stop; jx = j; break
            if c[j] > h[j-1]: px = c[j]; jx = j; break
            hi = max(hi, c[j])
            if not armed and c[j] >= entry + trig * atr: armed = True
            if armed:
                ns = entry if kind == "be" else max(entry, hi - tr * atr) if kind == "trailE" else hi - tr * atr
                stop = max(stop, ns)
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
    M = {"LIVE ref": None, "BE after +0.5ATR": ("be", .5, 0), "BE after +1ATR": ("be", 1, 0), "BE after +1.5ATR": ("be", 1.5, 0),
         "trail 1.5ATR after +1ATR": ("trailE", 1, 1.5), "trail 1ATR after +0.5ATR": ("trailE", .5, 1)}
    V = list(M)
    print("variants tried:", len(V))
    for n in V:
        PT.sim = make_sim(M[n]); T0 = PT.gen(AS, ctx, challenger.ruleset())
        live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
                for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
        row(n, live, kw, cut)
