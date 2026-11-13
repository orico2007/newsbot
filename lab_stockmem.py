"""Lab run 45 (2026-11-13): stock-specific reversion tendency as conditioner of the LIVE vol60>=1.75% setup:
(a) trailing 252d lag-1 autocorrelation of daily returns (negative = mean-reverting stock; Lo-MacKinlay style),
(b) the stock's own earlier closed signal trades (expanding-window mean pnl, needs >=3). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth

def ac1(c, i, n=252):
    if i < n + 1: return None
    r = [c[k] / c[k - 1] - 1 for k in range(i - n + 1, i + 1)]
    m = sum(r) / len(r); d = [x - m for x in r]
    den = sum(x * x for x in d)
    return sum(d[k] * d[k - 1] for k in range(1, len(d))) / den if den else None

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    B = lab_breadth.breadth_series(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    base = [t for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    print("base signals", len(base))
    # (a) autocorr
    for t in base: t["ac"] = ac1(AS[t["sym"]]["c"], IX[t["sym"]][t["t"][:10]])
    # (b) own history: all-universe signals (T0 incl. non-hv) for the same symbol, closed strictly before
    by = {}
    for t in T0: by.setdefault(t["sym"], []).append(t)
    def hist(t):
        p = [u["pnl_pct"] for u in by[t["sym"]] if u["t_exit"] < t["t"][:10]]
        return sum(p) / len(p) if len(p) >= 3 else None
    for t in base: t["mem"] = hist(t)
    row("LIVE ref (all)", base, kw, cut)
    A_ = [t for t in base if t["ac"] is not None]; M_ = [t for t in base if t["mem"] is not None]
    print("with ac:", len(A_), "with mem:", len(M_))
    row("LIVE ref (with ac)", A_, kw, cut); row("LIVE ref (with mem)", M_, kw, cut)
    srt = sorted(t["ac"] for t in A_); med = srt[len(srt) // 2]; t1, t2 = srt[len(srt) // 3], srt[2 * len(srt) // 3]
    print("ac median", round(med, 3), "tertiles", round(t1, 3), round(t2, 3))
    row("ac < median (mean-reverting stock)", [t for t in A_ if t["ac"] < med], kw, cut)
    row("ac >= median", [t for t in A_ if t["ac"] >= med], kw, cut)
    row("ac bottom tertile", [t for t in A_ if t["ac"] < t1], kw, cut)
    row("ac top tertile", [t for t in A_ if t["ac"] >= t2], kw, cut)
    row("rank by lowest ac", [dict(t, score=-t["ac"]) for t in A_], kw, cut)
    row("own-history mean pnl > 0", [t for t in M_ if t["mem"] > 0], kw, cut)
    row("own-history mean pnl <= 0", [t for t in M_ if t["mem"] <= 0], kw, cut)
    row("rank by own-history pnl", [dict(t, score=t["mem"]) for t in M_], kw, cut)
    print("variants tried: 8")
