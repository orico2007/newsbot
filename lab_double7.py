"""Lab run 20 (web idea): Connors 'Double 7' - buy close at 7-day closing low above SMA200, exit at 7-day closing high. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from sweep import sim, gate_ok
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def sig(AS, ctx, n=7, trend="s200", gate="spy200", cool=3, lo=205):
    out = []
    for sym, A in AS.items():
        c = A["c"]; cd = 0
        for i in range(lo, len(c) - 2):
            if i < cd: continue
            if c[i] > min(c[i-n+1:i]) : continue          # not a new n-day closing low
            if not A["s200"][i] or c[i] <= A["s200"][i]: continue
            if trend == "s50_200" and not (A["s50"][i] and A["s50"][i] > A["s200"][i]): continue
            if not gate_ok(ctx, A["t"][i], "long", gate): continue
            if not A["atr"][i] or A["atr"][i] / c[i] > .06: continue
            out.append((sym, i)); cd = i + cool
    return out

def trades(AS, sg, stop, hold, exit_mode):
    out = []
    for sym, i in sg:
        A = AS[sym]; c = A["c"]
        if exit_mode == "hh7":      # exit when close >= 7-day closing high (custom loop on top of sim stop logic)
            r = sim(A, i, "long", stop, "none", hold)
            if not r: continue
            # re-scan for exit
            entry = c[i] * 1.0005; j_exit = None
            for j in range(i + 1, min(len(c) - 1, i + hold) + 1):
                if A["l"][j] <= entry - stop * A["atr"][i] or A["o"][j] <= entry - stop * A["atr"][i]: break
                if c[j] >= max(c[j-6:j+1]): j_exit = j; break
            if j_exit:
                px = c[j_exit] * .9995; pnl = (px - entry) / entry * 100
                r = {"t": A["t"][i], "te": A["t"][j_exit], "pnl_pct": pnl, "R": pnl / (stop * A["atr"][i] / entry * 100), "held": j_exit - i}
        else:
            r = sim(A, i, "long", stop, exit_mode, hold)
        if r: r.update(sym=sym, t_exit=r["te"], score=50, side="long", rule="d7"); out.append(r)
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    B = breadth_series(AS); F = feats(AS)
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        if B.get(t["t"][:10], (0, 0))[0] < .10: continue
        f = F.get((t["sym"], t["t"])); live.append(dict(t, score=-f["m3"]) if f else t)
    row("LIVE (breadth+rank)", live, kw, cut)
    V = [("D7 n7 s200 hh7 exit hold15", dict(n=7), 4.0, 15, "hh7"),
         ("D7 n7 s200 prevhl hold7", dict(n=7), 4.0, 7, "prevhl"),
         ("D7 n7 s50_200 hh7 hold15", dict(n=7, trend="s50_200"), 4.0, 15, "hh7"),
         ("D7 n5 s50_200 prevhl hold7", dict(n=5, trend="s50_200"), 4.0, 7, "prevhl"),
         ("D7 n10 s50_200 prevhl hold7", dict(n=10, trend="s50_200"), 4.0, 7, "prevhl")]
    print("variants tried:", len(V) + 3)
    res = {}
    for nm, k, st, h, em in V:
        T = trades(AS, sig(AS, ctx, **k), st, h, em); res[nm] = T; row(nm, T, kw, cut)
    for nm in list(res)[:3:2]:
        T = res[nm]; Tb = [t for t in T if B.get(t["t"][:10], (0, 0))[0] >= .10]
        row(nm + " + breadth>=10%", Tb, kw, cut)
        row("  LIVE + " + nm + " (breadth)", live + Tb, kw, cut)
    row("  LIVE + D7 n7 s200 hh7 (no breadth)", live + res[list(res)[0]], kw, cut)
