"""Lab run 47 (2026-11-18): exit-at-the-open variants on the vol60>=1.75% LIVE setup (own idea). Backtest only.
Live exit = close > prior high (exit at that close). Variants: exit at that day's OPEN when the open already gaps above the prior high;
exit at the open of the day AFTER the prior-high close; open-exit only if gap >= x ATR."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats
from sweep import SLIP

def resim(A, i, mode, stop_k=4.0, hold=7, gap_atr=0.0):
    c, h, l, o = A["c"], A["h"], A["l"], A["o"]; n = len(c); atr = A["atr"][i]
    entry = c[i] * (1 + SLIP / 100); stop = entry - stop_k * atr; last = min(n - 1, i + hold)
    px, jx = None, last
    for j in range(i + 1, last + 1):
        if o[j] <= stop: px = o[j]; jx = j; break
        if l[j] <= stop: px = stop; jx = j; break
        if mode in ("open_gap", "open_gap_atr") and o[j] > h[j-1] and (o[j] - h[j-1]) >= gap_atr * atr:
            px = o[j]; jx = j; break
        if c[j] > h[j-1]:
            if mode == "next_open" and j + 1 <= last + 1 and j + 1 < n:
                px = o[j+1]; jx = j + 1
            else: px = c[j]; jx = j
            break
    if px is None: px = c[last]
    px *= (1 - SLIP / 100)
    pnl = (px - entry) / entry * 100
    return pnl, jx - i

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    champ = PT.gen(AS, ctx, challenger.ruleset()); live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(t["t"][:10]); v = challenger.vol60(AS[t["sym"]], i)
            if v is not None and v >= 1.75:
                live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0), i=i))
    row("LIVE ref", live, kw, cut)
    chk = [abs(resim(AS[t["sym"]], t["i"], "close")[0] - t["pnl_pct"]) for t in live]
    print("resim max abs diff vs live pnl:", round(max(chk), 4))
    V = [("close (re-sim check)", "close", 0), ("open if gap above prior high", "open_gap", 0),
         ("open if gap >= 0.25 ATR above", "open_gap_atr", .25), ("open if gap >= 0.5 ATR above", "open_gap_atr", .5),
         ("next-day open after trigger close", "next_open", 0)]
    print("variants tried:", len(V) - 1)
    for name, mode, g in V:
        T = []
        for t in live:
            u = dict(t); p, held = resim(AS[t["sym"]], t["i"], mode, gap_atr=g)
            u["pnl_pct"] = p
            if "R" in t: u["R"] = p / (4.0 * AS[t["sym"]]["atr"][t["i"]] / AS[t["sym"]]["c"][t["i"]] * 100)
            j = min(t["i"] + held, len(AS[t["sym"]]["t"]) - 1)
            u["te"] = u["t_exit"] = AS[t["sym"]]["t"][j]
            T.append(u)
        row(name, T, kw, cut)
