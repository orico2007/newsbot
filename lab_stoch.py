"""Lab idea 2026-11-09 (run 6): stochastic pullback sleeve (Quantified Strategies, daily-bar translation). Backtest only."""
import datetime
import lab, research, sweep, challenger
import portfolio_test as PT
from sweep import sim, trend_ok
from lab_52wh import row
from lab_gap import trades

def stoch(A, n=5):
    c, h, l = A["c"], A["h"], A["l"]; out = [None] * len(c)
    for i in range(n - 1, len(c)):
        hh, ll = max(h[i-n+1:i+1]), min(l[i-n+1:i+1])
        out[i] = 100 * (c[i] - ll) / (hh - ll) if hh > ll else 50
    return out

def signals(AS, ctx, n, k, smooth=1, cool=3):
    out = []
    for sym, A in AS.items():
        K = stoch(A, n); c = A["c"]; cd = 0
        for i in range(205, len(c) - 2):
            if i < cd: continue
            s = K[i] if smooth == 1 else sum(K[i-smooth+1:i+1]) / smooth
            if s is None or s >= k: continue
            if not trend_ok(A, i, "long", "s200") or not challenger.gate2(ctx, A["t"][i], "long", "spy200"): continue
            if not A["atr"][i] or A["atr"][i] / c[i] > 0.06: continue
            out.append((sym, i, 50 - s)); cd = i + cool
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); row("CHAMPION", champ, kw, cut)
    V = [("stoch5<10", 5, 10, 1), ("stoch5<5", 5, 5, 1), ("stoch5<20", 5, 20, 1), ("stoch14<10", 14, 10, 1), ("stoch5(3sm)<15", 5, 15, 3)]
    print("variants tried:", len(V))
    for name, n, k, sm in V:
        T = trades(AS, signals(AS, ctx, n, k, sm), 7, "prevhl")
        row(name, T, kw, cut); row("   + champion combined", champ + T, kw, cut)
