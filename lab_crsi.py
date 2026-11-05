"""Lab idea 2026-11-05 (run 4): Connors cumulative RSI(2), N-day-low and NR7 sleeves (web idea). Backtest only."""
import datetime
import lab, research, sweep, challenger
import portfolio_test as PT
from sweep import sim, trend_ok
from lab_52wh import row

def signals(AS, ctx, kind, cool=3):
    out = []
    for sym, A in AS.items():
        c, n, r2 = A["c"], len(A["c"]), A["r2"]; cd = 0
        for i in range(205, n - 2):
            if i < cd: continue
            if not trend_ok(A, i, "long", "s200") or not challenger.gate2(ctx, A["t"][i], "long", "spy200"): continue
            if not A["atr"][i] or A["atr"][i] / c[i] > 0.06: continue
            ok = False
            if kind == "crsi35": ok = r2[i] is not None and r2[i-1] is not None and r2[i] + r2[i-1] < 35
            elif kind == "crsi10": ok = r2[i] is not None and r2[i-1] is not None and r2[i] + r2[i-1] < 10
            elif kind == "low10": ok = c[i] <= min(c[i-9:i+1]) and c[i] < A["s5"][i] * 0.97
            elif kind == "low5down": ok = all(c[i-k] < c[i-k-1] for k in range(3)) and c[i] <= min(c[i-6:i+1]) and r2[i] is not None and r2[i] < 20
            elif kind == "nr7_dn":  # narrowest range of 7 and close below prior low (contraction then flush)
                rg = [A["h"][j] - A["l"][j] for j in range(i-6, i+1)]
                ok = rg[-1] == min(rg) and c[i] < c[i-1] and A["ibs"][i] < 0.3
            if ok: out.append((sym, i, 50 - (r2[i] or 50))); cd = i + cool
    return out

def trades(AS, sg, hold, exit_, stop=4.0):
    out = []
    for sym, i, sc in sg:
        r = sim(AS[sym], i, "long", stop, exit_, hold)
        if r: r.update(sym=sym, t_exit=r["te"], score=sc, side="long", rule="crsi"); out.append(r)
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); row("CHAMPION", champ, kw, cut)
    V = [("crsi<35 (2d sum), ma5 exit, hold7", "crsi35", "ma5", 7),
         ("crsi<10, ma5 exit, hold7", "crsi10", "ma5", 7),
         ("crsi<10, prevhl exit, hold7", "crsi10", "prevhl", 7),
         ("10d low & 3% under MA5, ma5 hold7", "low10", "ma5", 7),
         ("3 down days+6d low+rsi2<20, prevhl", "low5down", "prevhl", 7),
         ("NR7 + weak close, prevhl hold7", "nr7_dn", "prevhl", 7)]
    print("variants tried:", len(V))
    for name, k, ex, h in V:
        T = trades(AS, signals(AS, ctx, k), h, ex)
        row(name, T, kw, cut)
        row("   + champion combined", champ + T, kw, cut)
