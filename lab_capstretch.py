"""Lab run 69 (2026-11-22): 'Capitulation Stretch Reversion' sleeve (web idea). Backtest only.
Source: https://in.tradingview.com/script/WWuTjyDx-Capitulation-Stretch-Reversion-Jayadev-Rana/ (fetched; rules: close>EMA200, close >= k ATR below EMA5 and
N consecutive lower closes arm the setup, enter on the first up-close (reversal bar), exit close>=EMA5 / stop 3 ATR / 10 bars; claimed SPY PF 1.67 in-sample, unverified).
Translated to daily stock bars: arm on bar i-1, enter at close of bar i if c[i]>c[i-1]. Exit ma5 (SMA5 proxy for EMA5), stop 3 ATR, hold 10."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from sweep import sim, gate_ok
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def ema(c, n):
    k = 2 / (n + 1); out = [c[0]]
    for x in c[1:]: out.append(out[-1] + k * (x - out[-1]))
    return out

def sig(AS, ctx, k=0.5, nd=2, vol=None, cool=3):
    out = []
    for sym, A in AS.items():
        c = A["c"]; e5 = ema(c, 5); cd = 0
        for i in range(205, len(c) - 2):
            if i < cd or not A["atr"][i-1] or not A["s200"][i]: continue
            j = i - 1
            if c[i] <= A["s200"][i] or c[i] <= c[j]: continue
            if not all(c[j-m] < c[j-m-1] for m in range(nd)): continue
            if c[j] > e5[j] - k * A["atr"][j]: continue
            if not gate_ok(ctx, A["t"][i], "long", "spy200"): continue
            if A["atr"][i] / c[i] > .06: continue
            if vol is not None:
                v = challenger.vol60(A, i)
                if v is None or v < vol: continue
            out.append((sym, i)); cd = i + cool
    return out

def trades(AS, sg, stop=3.0, hold=10, ex="ma5"):
    out = []
    for sym, i in sg:
        r = sim(AS[sym], i, "long", stop, ex, hold)
        if r: r.update(sym=sym, t_exit=r["te"], score=50, side="long", rule="cs"); out.append(r)
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        if B.get(t["t"][:10], (0, 0))[0] < .10: continue
        v = challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10]))
        if v is not None and v >= 1.75:
            f = F.get((t["sym"], t["t"])); live.append(dict(t, score=-f["m3"]) if f else dict(t))
    row("LIVE ref", live, kw, cut)
    V = [("default k0.5 nd2 s200", dict(), "ma5", 3.0, 10),
         ("k1.0 nd2", dict(k=1.0), "ma5", 3.0, 10),
         ("k1.5 nd3", dict(k=1.5, nd=3), "ma5", 3.0, 10),
         ("k1.0 nd2 vol60>=1.75", dict(k=1.0, vol=1.75), "ma5", 3.0, 10),
         ("k1.0 nd2 vol60>=1.75 prevhl hold7 stop4", dict(k=1.0, vol=1.75), "prevhl", 4.0, 7),
         ("k1.5 nd3 vol60>=1.75 prevhl hold7 stop4", dict(k=1.5, nd=3, vol=1.75), "prevhl", 4.0, 7)]
    print("variants tried:", len(V)); res = {}
    for nm, k, ex, st, h in V:
        T = trades(AS, sig(AS, ctx, **k), stop=st, hold=h, ex=ex); res[nm] = T; row(nm, T, kw, cut)
        Tb = [t for t in T if B.get(t["t"][:10], (0, 0))[0] >= .10]
        row("   +breadth>=10%", Tb, kw, cut)
        row("   LIVE + this (breadth>=10%)", live + Tb, kw, cut)
