"""Lab run 23 (2026-11-16): SPY-hedge overlay on the LIVE vol60>=1.75% setup (own idea, untested: beta-neutralising each trade by shorting SPY
for the same holding period; pnl_pct -= h * SPY return entry->exit). Also vol-scaled hedge (beta60 estimated per stock). Backtest only; no costs on hedge."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_retune import live
from lab_breadth import breadth_series
from lab_sector import feats

def beta(A, i, spy_ret, win=60):
    c = A["c"]; d = A["t"]
    xs, ys = [], []
    for k in range(i - win + 1, i + 1):
        s = spy_ret.get(d[k][:10])
        if s is None or k < 1: continue
        xs.append(s); ys.append(c[k] / c[k - 1] - 1)
    if len(xs) < 40: return 1.0
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    v = sum((x - mx) ** 2 for x in xs)
    return max(0.0, min(3.0, sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / v)) if v else 1.0

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    B = breadth_series(AS); Fs = feats(AS); IX = {s: {d: i for i, d in enumerate(a["t"])} for s, a in AS.items()}
    rules = [challenger.R(**x) for x in (challenger.A, challenger.E, challenger.F)]
    T0 = live(AS, ctx, rules, B, Fs, IX)
    sd = [x["t"][:10] for x in spy]; sc = {d: x["c"] for d, x in zip(sd, spy)}
    sret = {sd[k]: spy[k]["c"] / spy[k - 1]["c"] - 1 for k in range(1, len(spy))}
    sma50 = {}
    for k in range(50, len(spy)): sma50[sd[k]] = sum(x["c"] for x in spy[k - 50:k]) / 50
    def mk(h, mode="const"):
        out = []
        for t in T0:
            a, b = t["t"][:10], t["t_exit"][:10]
            if a not in sc or b not in sc: out.append(t); continue
            sr = (sc[b] / sc[a] - 1) * 100
            if mode == "beta": hh = h * beta(AS[t["sym"]], IX[t["sym"]][a], sret)
            elif mode == "weak": hh = h if sc[a] < sma50.get(a, 0) else 0.0
            else: hh = h
            out.append(dict(t, pnl_pct=t["pnl_pct"] - hh * sr))
        return out
    V = [("LIVE (vol175) unhedged", T0), ("hedge 0.25 x SPY", mk(.25)), ("hedge 0.5 x SPY", mk(.5)), ("hedge 1.0 x SPY", mk(1.0)),
         ("hedge 1.0 x beta60 x SPY", mk(1.0, "beta")), ("hedge 0.5 x beta60 x SPY", mk(.5, "beta")), ("hedge 1.0 only if SPY<SMA50", mk(1.0, "weak"))]
    print("variants tried:", len(V), "data through", last)
    for n, T in V: row(n, T, kw, cut)
