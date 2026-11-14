"""Lab run 21 (2026-11-14, web-seeded: equity-curve throttling, luxalgo.com/library/concept/equity-curve-based-throttling ; unverified).
Strategy-level momentum/reversal: condition each LIVE-setup entry on the result of the strategy's last N CLOSED trades (known on the entry date).
Shadow curve = trades of the unfiltered LIVE portfolio (exit date < entry date). Backtest only."""
import datetime, bisect
import lab, sweep, challenger
import portfolio_test as PT
import lab_breadth, lab_sector
from lab_52wh import row

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = challenger.DEF_PORT
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    B = lab_breadth.breadth_series(AS); F = lab_sector.feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    base = lab.portfolio(live, **kw)
    sh = sorted(base["trades"], key=lambda t: t["t_exit"]); ex = [t["t_exit"] for t in sh]
    def trail(d, N):
        k = bisect.bisect_left(ex, d)   # exits strictly before d
        w = sh[max(0, k - N):k]
        return (len(w), sum(t["pnl_pct"] for t in w) / len(w), sum(t["pnl_pct"] > 0 for t in w) / len(w)) if w else (0, 0, 0)
    row("LIVE (vol175)", live, kw, cut)
    V = []
    for N in (10, 20, 30):
        V.append((f"skip if last{N} mean pnl<0", lambda t, N=N: (lambda r: r[0] < N or r[1] >= 0)(trail(t["t"], N))))
        V.append((f"CONTRA skip if last{N} mean pnl>0", lambda t, N=N: (lambda r: r[0] < N or r[1] <= 0)(trail(t["t"], N))))
    V.append(("skip if last20 win%<60", lambda t: (lambda r: r[0] < 20 or r[2] >= .60)(trail(t["t"], 20))))
    V.append(("skip if last10 win%<50", lambda t: (lambda r: r[0] < 10 or r[2] >= .50)(trail(t["t"], 10))))
    print("variants tried:", len(V))
    for n, f in V:
        row(n, [t for t in live if f(t)], kw, cut)
