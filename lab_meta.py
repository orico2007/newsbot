"""Lab run 44 (2026-11-13): strategy self-timing (meta filter) - skip / favour new entries depending on the LIVE setup's own last K closed trades. Own idea. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth

def hist_gate(ref, K, fn):
    """ref: taken trades of LIVE ref. Returns f(date)->bool using the last K trades closed strictly before date."""
    ex = sorted(ref, key=lambda t: t["t_exit"])
    def f(d):
        prev = [t for t in ex if t["t_exit"] < d][-K:]
        if len(prev) < K: return True
        return fn(prev)
    return f

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    B = lab_breadth.breadth_series(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    base = [t for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    ref = row("LIVE ref", base, kw, cut)["trades"]
    win = lambda p: sum(1 for t in p if t["pnl_pct"] > 0) / len(p)
    mean = lambda p: sum(t["pnl_pct"] for t in p) / len(p)
    V = [("skip if last10 win%<50", 10, lambda p: win(p) >= .5),
         ("skip if last10 mean pnl<0", 10, lambda p: mean(p) >= 0),
         ("skip if last20 mean pnl<0", 20, lambda p: mean(p) >= 0),
         ("only if last10 win%<=70 (after weak stretch)", 10, lambda p: win(p) <= .7),
         ("only if last10 mean pnl<=1% (after cool stretch)", 10, lambda p: mean(p) <= 1.0),
         ("skip if last5 has >=2 stop-outs (pnl<-3%)", 5, lambda p: sum(1 for t in p if t["pnl_pct"] < -3) < 2)]
    print("variants tried:", len(V))
    for n, K, fn in V:
        g = hist_gate(ref, K, fn); cache = {}
        row(n, [t for t in base if cache.setdefault(t["t"][:10], g(t["t"][:10]))], kw, cut)
