"""Lab run 48 (2026-11-13): overbought-fade SHORT sleeve in confirmed bear regimes (Connors-style RSI2 short; web-seeded, own rules). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from sweep import sim, trend_ok, gate_ok
from lab_52wh import row
import lab_breadth

def signals(AS, ctx, r2=95, gate="spy200", trend="s200", lo=205, cool=5, ext=0):
    out = []
    for sym, A in AS.items():
        c, n = A["c"], len(A["c"]); cd = 0
        for i in range(lo, n - 2):
            if i < cd or A["r2"][i] is None or A["r2"][i] <= r2: continue
            if not A["atr"][i] or A["s10"][i] is None if "s10" in A else False: continue
            if not trend_ok(A, i, "short", trend) or not gate_ok(ctx, A["t"][i], "short", gate): continue
            if ext and (A["s20"][i] is None or c[i] < A["s20"][i] + ext * A["atr"][i]): continue
            out.append((sym, i, A["r2"][i])); cd = i + cool
    return out

def trades(AS, sg, hold, stop, ex="none"):
    out = []
    for sym, i, sc in sg:
        r = sim(AS[sym], i, "short", stop, ex, hold)
        if r: r.update(sym=sym, t_exit=r["te"], score=sc, side="short", rule="short"); out.append(r)
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    B = lab_breadth.breadth_series(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    base = [t for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    row("LIVE ref", base, kw, cut)
    V = [("short rsi2>95, SPY<200d, stock<200d, hold5", dict(), 5, 4.0),
         ("short rsi2>98, SPY<200d, stock<200d, hold5", dict(r2=98), 5, 4.0),
         ("short rsi2>95, bear regime gate, hold5", dict(gate="bear"), 5, 4.0),
         ("short rsi2>95, no gate, stock<200d, hold5", dict(gate="none"), 5, 4.0),
         ("short rsi2>95, SPY<200d, stock>200d-any (trend none), hold5", dict(trend="none"), 5, 4.0),
         ("short rsi2>95, SPY<200d, stock<200d, hold3", dict(), 3, 4.0)]
    print("variants tried:", len(V))
    for name, kk, hold, stop in V:
        T = trades(AS, signals(AS, ctx, **kk), hold, stop)
        row(name, T, kw, cut)
        row("   + LIVE combined", base + T, kw, cut)
