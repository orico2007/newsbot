"""Lab run 28 (2026-11-08): profit-target and trailing/breakeven stop exits layered on the LIVE exit (close > prior high). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from sweep import SLIP
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def make_sim(target=None, be=None, trail=None):
    """target: exit at entry+target*ATR if intraday high reaches it (gap-up opens fill at open).
    be: after any close >= entry+be*ATR, stop moves to entry. trail: stop = max(stop, highest close - trail*ATR) from the next day."""
    def sim(A, i, side, stop_k, exit_mode, hold):
        c, h, l, o = A["c"], A["h"], A["l"], A["o"]; n = len(c); atr = A["atr"][i]
        if not atr or side != "long": return sweep.sim(A, i, side, stop_k, exit_mode, hold)
        entry = c[i] * (1 + SLIP / 100); stop = entry - stop_k * atr
        tgt = entry + target * atr if target else None
        last = min(n - 1, i + hold)
        if last <= i: return None
        px, jx, hc = None, last, c[i]
        for j in range(i + 1, last + 1):
            if o[j] <= stop: px = o[j]; jx = j; break
            if l[j] <= stop: px = stop; jx = j; break
            if tgt and o[j] >= tgt: px = o[j]; jx = j; break
            if tgt and h[j] >= tgt: px = tgt; jx = j; break
            if exit_mode == "prevhl" and c[j] > h[j-1]: px = c[j]; jx = j; break
            hc = max(hc, c[j])
            if be is not None and hc >= entry + be * atr: stop = max(stop, entry)
            if trail: stop = max(stop, hc - trail * atr)
        if px is None: px = c[last]
        px *= (1 - SLIP / 100); pnl = (px - entry) / entry * 100
        return {"t": A["t"][i], "te": A["t"][jx], "pnl_pct": pnl, "R": pnl / (stop_k * atr / entry * 100), "held": jx - i}
    return sim

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    B = breadth_series(AS); F = feats(AS)
    m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    V = [("LIVE ref", {}), ("target 1.0 ATR", dict(target=1.0)), ("target 1.5 ATR", dict(target=1.5)), ("target 2.5 ATR", dict(target=2.5)),
         ("breakeven after +1 ATR close", dict(be=1.0)), ("trail 2 ATR from highest close", dict(trail=2.0)), ("trail 3 ATR", dict(trail=3.0))]
    print("variants tried:", len(V))
    for n, k in V:
        PT.sim = make_sim(**k); champ = PT.gen(AS, ctx, challenger.ruleset()); live = []
        for t in champ:
            if B.get(t["t"][:10], (0, 0))[0] >= .10:
                u = dict(t); u["score"] = -m3(t); live.append(u)
        row(n, live, kw, cut)
