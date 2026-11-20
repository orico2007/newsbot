"""Lab run 48 (outside/key reversal day); derived from run 43 script. Source: https://www.pulse.bot/stock-trading/news/reversal-day-strategy-for-the-markets-1fbb2118-59a3-415b-8f16-28b75dbc8c47/
"""
"""Lab run 43 (2026-11-20): 3-bar linear-regression-slope 'hook' reversal sleeve (web idea). Backtest only.
Source: https://algomatictrading.substack.com/p/strategy-4-a-mean-reversion-strategy (index futures; rule: slope of 3-period linreg of typical price
turns up after a down slope, red candle, exit close>SMA5). Translated to daily stock bars, standalone and with the vol60 filter, plus combined with LIVE."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from sweep import sim, gate_ok
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def sig(AS, ctx, trend=True, vol=None, mode="outside", down3=False, cool=3):
    out = []
    for sym, A in AS.items():
        c, h, l, o = A["c"], A["h"], A["l"], A["o"]; cd = 0
        for i in range(205, len(c) - 2):
            if i < cd: continue
            if mode == "outside": ok = l[i] < l[i-1] and c[i] > h[i-1]          # bullish outside reversal day
            else: ok = l[i] < l[i-1] and c[i] > c[i-1] and c[i] > o[i]          # key reversal: new low, closes up
            if not ok: continue
            if down3 and not (c[i-1] < c[i-2] < c[i-3]): continue
            if trend and (not A["s200"][i] or c[i] <= A["s200"][i]): continue
            if not gate_ok(ctx, A["t"][i], "long", "spy200"): continue
            if not A["atr"][i] or A["atr"][i] / c[i] > .06: continue
            if vol is not None:
                v = challenger.vol60(A, i)
                if v is None or v < vol: continue
            out.append((sym, i)); cd = i + cool
    return out

def trades(AS, sg, stop=4.0, hold=7, ex="ma5"):
    out = []
    for sym, i in sg:
        r = sim(AS[sym], i, "long", stop, ex, hold)
        if r: r.update(sym=sym, t_exit=r["te"], score=50, side="long", rule="lr"); out.append(r)
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
    V = [("outside rev s200 ma5 h7", dict(), "ma5"),
         ("outside rev down3 s200 ma5", dict(down3=True), "ma5"),
         ("outside rev vol60>=1.75 ma5", dict(vol=1.75), "ma5"),
         ("outside rev vol60>=1.75 prevhl", dict(vol=1.75), "prevhl"),
         ("outside rev down3 vol60>=1.75 ma5", dict(vol=1.75, down3=True), "ma5"),
         ("key rev vol60>=1.75 ma5", dict(vol=1.75, mode="key"), "ma5")]
    print("variants tried:", len(V)); res = {}
    for nm, k, ex in V:
        T = trades(AS, sig(AS, ctx, **k), ex=ex); res[nm] = T; row(nm, T, kw, cut)
    for nm in list(res)[2:5]:
        row("  LIVE + " + nm, live + res[nm], kw, cut)
        row("  LIVE + " + nm + " (breadth>=10%)", live + [t for t in res[nm] if B.get(t["t"][:10], (0, 0))[0] >= .10], kw, cut)
