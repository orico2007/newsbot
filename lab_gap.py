"""Lab idea 2026-11-05 (run 5): gap-down fade and overnight-hold reversion sleeves (web/own idea). Backtest only."""
import datetime
import lab, research, sweep, challenger
import portfolio_test as PT
from sweep import sim, trend_ok, SLIP
from lab_52wh import row

def signals(AS, ctx, kind, cool=3):
    out = []
    for sym, A in AS.items():
        c, o, n, r2 = A["c"], A["o"], len(A["c"]), A["r2"]; cd = 0
        for i in range(205, n - 2):
            if i < cd: continue
            if not trend_ok(A, i, "long", "s200") or not challenger.gate2(ctx, A["t"][i], "long", "spy200"): continue
            if not A["atr"][i] or A["atr"][i] / c[i] > 0.06: continue
            gap = (o[i] / c[i-1] - 1) * 100; ok = False
            if kind == "gap2_recover": ok = gap < -2 and c[i] > o[i]
            elif kind == "gap3_close_low": ok = gap < -3 and A["ibs"][i] < 0.3
            elif kind == "gap1_recover": ok = gap < -1 and c[i] > o[i]
            elif kind == "gap3_recover": ok = gap < -3 and c[i] > o[i]
            elif kind == "gap2_recover_hi": ok = gap < -2 and c[i] > o[i] and A["ibs"][i] > 0.6
            elif kind == "gap2_r2": ok = gap < -2 and r2[i] is not None and r2[i] < 15
            elif kind == "r2_5": ok = r2[i] is not None and r2[i] < 5
            elif kind == "r2_5_ibs": ok = r2[i] is not None and r2[i] < 10 and A["ibs"][i] < 0.15
            if ok: out.append((sym, i, 50 - (r2[i] or 50))); cd = i + cool
    return out

def trades(AS, sg, hold, exit_, stop=4.0, overnight=False):
    out = []
    for sym, i, sc in sg:
        A = AS[sym]
        if overnight:  # buy close, sell next open
            e = A["c"][i] * (1 + SLIP/100); x = A["o"][i+1] * (1 - SLIP/100); pnl = (x/e - 1) * 100
            r = {"t": A["t"][i], "te": A["t"][i+1], "pnl_pct": pnl, "R": pnl / (stop * A["atr"][i] / e * 100), "held": 1}
        else:
            r = sim(A, i, "long", stop, exit_, hold)
        if r: r.update(sym=sym, t_exit=r["te"], score=sc, side="long", rule="gap"); out.append(r)
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); row("CHAMPION", champ, kw, cut)
    V = [("gap<-2% & closed>open, prevhl h7", "gap2_recover", "prevhl", 7, False),
         ("gap<-3% & IBS<.3, prevhl h7", "gap3_close_low", "prevhl", 7, False),
         ("gap<-2% & rsi2<15, prevhl h7", "gap2_r2", "prevhl", 7, False),
         ("rsi2<5 OVERNIGHT (close->next open)", "r2_5", None, 1, True),
         ("rsi2<10&ibs<.15 OVERNIGHT", "r2_5_ibs", None, 1, True),
         ("rsi2<5 prevhl h7", "r2_5", "prevhl", 7, False)]
    print("variants tried:", len(V))
    for name, k, ex, h, on in V:
        T = trades(AS, signals(AS, ctx, k), h, ex, overnight=on)
        row(name, T, kw, cut)
        row("   + champion combined", champ + T, kw, cut)
