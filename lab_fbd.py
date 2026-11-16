"""Lab run 21 (2026-11-16): failed-breakdown / Turtle-Soup reversal sleeve (undercut N-day low intraday, close back above it) on top of LIVE setup. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from sweep import sim, trend_ok
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def signals(AS, ctx, N, ibs_min, hv, cool=3):
    out = []
    for sym, A in AS.items():
        c, l, n = A["c"], A["l"], len(A["c"]); cd = 0
        for i in range(205, n - 2):
            if i < cd: continue
            if not trend_ok(A, i, "long", "s200") or not challenger.gate2(ctx, A["t"][i], "long", "spy200"): continue
            if not A["atr"][i] or A["atr"][i] / c[i] > 0.06: continue
            pl = min(l[i - N:i])
            if not (l[i] < pl and c[i] > pl and A["ibs"][i] >= ibs_min): continue
            if hv:
                v = challenger.vol60(A, i)
                if v is None or v < 1.75: continue
            out.append((sym, i)); cd = i + cool
    return out

def trades(AS, sg):
    out = []
    for sym, i in sg:
        r = sim(AS[sym], i, "long", 4.0, "prevhl", 7)
        if r: r.update(sym=sym, t_exit=r["te"], score=0, side="long", rule="fbd"); out.append(r)
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    okb = lambda t: B.get(t["t"][:10], (0, 0))[0] >= .10
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [dict(t, score=-m3(t)) for t in PT.gen(AS, ctx, challenger.ruleset()) if okb(t) and hv(t)]
    row("LIVE (vol175)", live, kw, cut)
    V = [(N, ib, h) for N in (10, 20) for ib in (0, 0.5) for h in (False, True)]
    print("variants tried:", len(V))
    for N, ib, h in V:
        S = [dict(t, score=-m3(t) - 1000) for t in trades(AS, signals(AS, ctx, N, ib, h)) if okb(t)]
        nm = f"fbd N={N} ibs>={ib} hv={h}"
        row(nm, S, kw, cut); row("   + live", live + S, kw, cut)
