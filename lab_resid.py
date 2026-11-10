"""Lab idea 2026-11-10 (run 6): idiosyncratic vs market-wide oversold reversion (short-term reversal literature: residual/industry-adjusted reversal).
Is the RSI2 reversion edge stronger when the drop is stock-specific (3d return minus SPY 3d return very negative, SPY flat) or market-wide? Backtest only."""
import datetime
import lab, research, sweep, challenger
import portfolio_test as PT
from sweep import sim, trend_ok
from lab_52wh import row

def signals(AS, ctx, spyret, kind, cool=3):
    out = []
    for sym, A in AS.items():
        c, n, r2 = A["c"], len(A["c"]), A["r2"]; cd = 0
        for i in range(205, n - 2):
            if i < cd: continue
            if r2[i] is None or r2[i] >= 10: continue
            if not trend_ok(A, i, "long", "s200") or not challenger.gate2(ctx, A["t"][i], "long", "spy200"): continue
            if not A["atr"][i] or A["atr"][i] / c[i] > 0.06: continue
            s3 = spyret.get(A["t"][i]);
            if s3 is None: continue
            rel = A["ret3"][i] - s3
            ok = {"base": True, "idio5": rel < -5 and s3 > -1, "idio3": rel < -3 and s3 > -1,
                  "idio8": rel < -8 and s3 > -1, "sys": s3 < -2, "notidio": not (rel < -5 and s3 > -1)}[kind]
            if ok: out.append((sym, i, -rel)); cd = i + cool
    return out

def trades(AS, sg):
    out = []
    for sym, i, sc in sg:
        r = sim(AS[sym], i, "long", 4.0, "prevhl", 7)
        if r: r.update(sym=sym, t_exit=r["te"], score=sc, side="long", rule="resid"); out.append(r)
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); sp = lab.load_bars()["SPY"]; last = sp[-1]["t"][:10]
    spyret = {sp[i]["t"][:10]: (sp[i]["c"] / sp[i-3]["c"] - 1) * 100 for i in range(3, len(sp))}
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); row("CHAMPION", champ, kw, cut)
    ks = ["base", "idio3", "idio5", "idio8", "sys", "notidio"]
    print("variants tried:", len(ks), "data through", last)
    for k in ks:
        T = trades(AS, signals(AS, ctx, spyret, k)); row("rsi2<10 " + k, T, kw, cut)
        if k in ("idio5", "idio3"): row("   + champion combined", champ + T, kw, cut)
