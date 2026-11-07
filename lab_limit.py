"""Lab run 22 (2026-11-07): limit-order pullback entry (buy next day at close - k*ATR) and next-open entry on the LIVE setup. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from sweep import SLIP
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def sim_limit(A, i, k, stop_k=4.0, hold=7, mode="limit"):
    """Signal at close of bar i. mode 'limit': buy limit close-k*ATR on bar i+1 (fills at min(open,limit) if low<=limit, else no trade).
    mode 'open': buy at next open. Exits as live: stop stop_k*ATR below fill, close>prev high, max hold i+hold."""
    c, h, l, o, atr = A["c"], A["h"], A["l"], A["o"], A["atr"][i]; n = len(c)
    if not atr or i + 1 >= n: return None
    j0 = i + 1
    if mode == "open": fill = o[j0]
    else:
        lim = c[i] - k * atr
        if o[j0] <= lim: fill = o[j0]
        elif l[j0] <= lim: fill = lim
        else: return None
    entry = fill * (1 + SLIP / 100); stop = entry - stop_k * atr
    last = min(n - 1, i + hold); px = None; je = last
    # same-day exits after fill: only stop (close>prev high would be a same-bar exit; allow from the fill day close too)
    for j in range(j0, last + 1):
        if l[j] <= stop and (j > j0 or fill > stop): px = stop if o[j] > stop else o[j]; je = j; break
        if j > j0 and c[j] > h[j - 1]: px = c[j]; je = j; break
    if px is None: px = c[last]
    px *= (1 - SLIP / 100)
    pnl = (px - entry) / entry * 100
    return {"t": A["t"][j0], "te": A["t"][je], "pnl_pct": pnl, "R": pnl / (stop_k * atr / entry * 100), "held": je - j0}

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); B = breadth_series(AS); F = feats(AS)
    m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            u = dict(t); u["score"] = -m3(t); live.append(u)
    ix = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    row("LIVE ref (enter at signal close)", live, kw, cut)
    V = [("next-open entry", "open", 0), ("limit close-0.25ATR", "limit", .25), ("limit close-0.5ATR", "limit", .5),
         ("limit close-1.0ATR", "limit", 1.0), ("limit close-1.5ATR", "limit", 1.5)]
    print("variants tried:", len(V))
    for name, mode, k in V:
        T = []
        for t in live:
            i = ix[t["sym"]][t["t"]]; r = sim_limit(AS[t["sym"]], i, k, mode=mode)
            if r: u = dict(t); u.update(r); u["t_exit"] = r["te"]; T.append(u)
        print(f"  fill rate {len(T)}/{len(live)}")
        row(name, T, kw, cut)
