"""Lab run 74 (2026-11-23): news-driven decline flag (volume>=2.5x + gap/drop spike in the prior N sessions, i.e. a probable earnings/news day inside the decline) as filter/size tilt of the live vol60+zreg setup. Own idea; backward-looking only. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row as _row

def row(name, T, kw, cut):
    if len(T) < 3:
        print(f'{name:42} n={len(T)} (too few)'); return
    try: _row(name, T, kw, cut)
    except TypeError: print(f'{name:42} n={len(T)} (no L12 trades)')
from lab_breadth import breadth_series
from lab_sector import feats
from lab_zscore import zreg

def spike_down(A, i, n):
    c, o, v, va = A["c"], A["o"], A["v"], A["vavg"]
    for j in range(max(21, i - n + 1), i + 1):
        if va[j - 1] and v[j] >= 2.5 * va[j - 1] and (o[j] / c[j - 1] - 1 <= -0.03 or c[j] / c[j - 1] - 1 <= -0.05):
            return True
    return False

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(spy) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2; B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(t["t"][:10]); v = challenger.vol60(AS[t["sym"]], i)
            if v is not None and v >= 1.75 and i is not None and i >= 25 and zreg(AS[t["sym"]], i, 20) < -1.5:
                A = AS[t["sym"]]
                live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0), _f5=spike_down(A, i, 5), _f10=spike_down(A, i, 10), _f20=spike_down(A, i, 20)))
    row("LIVE ref", live, kw, cut)
    for n in ("_f5", "_f10", "_f20"):
        row("flag " + n + " only", [t for t in live if t[n]], kw, cut)
        row("skip " + n, [t for t in live if not t[n]], kw, cut)
    for n in ("_f10",):
        for nm, up, dn in (("tilt 1.25/0.75 favour flag", 1.25, .75), ("tilt 1.25/0.75 favour no-flag", .75, 1.25)):
            T = []
            for t in live:
                m = up if t[n] else dn
                T.append(dict(t, size_mult=m, mult=m))
            row(nm, T, kw, cut)
    print("variants tried: 3 flags x2 + 2 tilts = 8")
    for nm, f in (("early<=2023", lambda t: t["t"][:4] <= "2023"), ("late>=2024", lambda t: t["t"][:4] >= "2024")):
        row(nm + " flag10", [t for t in live if f(t) and t["_f10"]], kw, cut)
        row(nm + " noflag10", [t for t in live if f(t) and not t["_f10"]], kw, cut)
