"""Lab run 49 (2026-11-20): structural stops (signal-day low / 5-day low minus k ATR) and weekend-avoidance exits (Friday close) on the
vol60>=1.75% LIVE setup (own idea; no earlier run tested a price-structure stop or a weekend exit). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from sweep import SLIP
from lab_52wh import row
import lab_breadth
from lab_sector import feats

def make_sim(mode=None):
    """mode=(kind, k). kind 'lowstop': stop = max(entry-4ATR, low[i]-k*ATR); 'low5': same with 5d low; 'fri': exit at Friday close (k=0 any Friday,
    k=1 only if in profit); live prior-high exit and 4 ATR stop stay."""
    def sim(A, i, side, stop_k, exit_mode, hold):
        if mode is None or side != "long": return sweep.sim(A, i, side, stop_k, exit_mode, hold)
        c, h, l, o = A["c"], A["h"], A["l"], A["o"]; n = len(c); atr = A["atr"][i]
        if not atr: return None
        kind, k = mode
        entry = c[i] * (1 + SLIP / 100); stop = entry - stop_k * atr
        if kind == "lowstop": stop = max(stop, l[i] - k * atr)
        if kind == "low5": stop = max(stop, min(l[i-4:i+1]) - k * atr)
        last = min(n - 1, i + hold)
        if last <= i: return None
        px, jx = None, last
        for j in range(i + 1, last + 1):
            if o[j] <= stop: px = o[j]; jx = j; break
            if l[j] <= stop: px = stop; jx = j; break
            if c[j] > h[j-1]: px = c[j]; jx = j; break
            if kind == "fri" and datetime.date.fromisoformat(A["t"][j][:10]).weekday() == 4 and j < last:
                if k == 0 or c[j] > entry: px = c[j]; jx = j; break
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
    M = {"LIVE ref": None, "stop = signal-day low - 0 ATR": ("lowstop", 0), "stop = signal-day low - 0.5 ATR": ("lowstop", .5),
         "stop = signal-day low - 1 ATR": ("lowstop", 1), "stop = 5d low - 0.5 ATR": ("low5", .5),
         "exit any Friday close": ("fri", 0), "exit Friday close only if in profit": ("fri", 1)}
    print("variants tried:", len(M) - 1)
    for n in M:
        PT.sim = make_sim(M[n]); T0 = PT.gen(AS, ctx, challenger.ruleset())
        live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
                for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
        row(n, live, kw, cut)
