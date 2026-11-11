"""Lab run 26 (2026-11-11): follow-up to run 25. Skip ADX<20 tail, ADX-tiered sizing (size emulated by scaling pnl_pct), ADX as ranking score. LIVE vol60>=1.75% setup. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth
from lab_sector import feats
from lab_adx import adx_series

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    B = lab_breadth.breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    AD = {s: adx_series(A) for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    base = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10]
    live = [t for t in base if hv(t)]
    def ad(t):
        i = IX[t["sym"]].get(t["t"][:10]); a = None if i is None else AD[t["sym"]][i]
        return 25 if a is None else a
    def scale(f, keep=lambda t: True):
        out = []
        for t in live:
            if not keep(t): continue
            k = f(ad(t)); u = dict(t); u["pnl_pct"] = t["pnl_pct"] * k
            if "r" in u and isinstance(u["r"], (int, float)): u["r"] = u["r"] * k
            out.append(u)
        return out
    row("LIVE (vol175)", live, kw, cut)
    row("skip ADX<20", scale(lambda a: 1, lambda t: ad(t) >= 20), kw, cut)
    row("ADX>=25 at 1.5x, else 1x", scale(lambda a: 1.5 if a >= 25 else 1), kw, cut)
    row("ADX>=25 1.5x, 20-25 1x, <20 0.5x", scale(lambda a: 1.5 if a >= 25 else (1 if a >= 20 else .5)), kw, cut)
    row("skip<20 + ADX>=25 at 1.5x", scale(lambda a: 1.5 if a >= 25 else 1, lambda t: ad(t) >= 20), kw, cut)
    r = [dict(t, score=ad(t)) for t in live]
    row("rank by highest ADX first", r, kw, cut)
    print("variants tried: 5")
