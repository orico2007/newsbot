"""Lab run 7 (2026-11-10): down-close streak length and trend context (close vs SMA50) inside the LIVE setup. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); B = breadth_series(AS)
    from lab_sector import feats
    F = feats(AS); m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            u = dict(t); u["score"] = -m3(t); live.append(u)
    ix = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    def streak(t):
        A = AS[t["sym"]]; i = ix[t["sym"]].get(t["t"])
        if i is None: return None
        n = 0
        while i - n > 0 and A["c"][i-n] < A["c"][i-n-1]: n += 1
        return n
    def a50(t):
        A = AS[t["sym"]]; i = ix[t["sym"]].get(t["t"])
        return None if i is None or not A["s50"][i] else A["c"][i] > A["s50"][i]
    row("LIVE", live, kw, cut)
    V = [("streak>=2", lambda t: (streak(t) or 0) >= 2), ("streak>=3", lambda t: (streak(t) or 0) >= 3),
         ("streak<=2", lambda t: (streak(t) or 0) <= 2), ("close>SMA50", lambda t: a50(t) is True)]
    print("variants tried:", len(V))
    for n, f in V: row(n, [t for t in live if f(t)], kw, cut)
