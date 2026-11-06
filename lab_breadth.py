"""Lab run 12: market-breadth washout filter on champion entries (share of universe with RSI2<10 or at 5-day low on the signal day). Backtest only."""
import datetime
from collections import defaultdict
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row

def breadth_series(AS):
    """date -> (frac with rsi2<10, frac closing at 5-day low) over stocks that have data that day."""
    n = defaultdict(int); a = defaultdict(int); b = defaultdict(int)
    for A in AS.values():
        for i, d in enumerate(A["t"]):
            if i < 6 or A["r2"][i] is None: continue
            n[d] += 1
            if A["r2"][i] < 10: a[d] += 1
            if A["c"][i] <= min(A["c"][i-4:i+1]): b[d] += 1
    return {d: (a[d] / n[d], b[d] / n[d]) for d in n if n[d] > 30}

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); row("CHAMPION", champ, kw, cut)
    B = breadth_series(AS)
    r = lambda t: B.get(t["t"][:10], (0, 0))[0]; l = lambda t: B.get(t["t"][:10], (0, 0))[1]
    import statistics
    print("median rsi2<10 frac on entries:", statistics.median(r(t) for t in champ), " 5d-low frac:", statistics.median(l(t) for t in champ))
    V = [("rsi2<10 breadth < 10%", lambda t: r(t) < .10), ("rsi2<10 breadth >= 10%", lambda t: r(t) >= .10),
         ("rsi2<10 breadth >= 20%", lambda t: r(t) >= .20), ("rsi2<10 breadth >= 30%", lambda t: r(t) >= .30),
         ("5d-low breadth < 25%", lambda t: l(t) < .25), ("5d-low breadth >= 25%", lambda t: l(t) >= .25),
         ("5d-low breadth >= 40%", lambda t: l(t) >= .40), ("5d-low breadth >= 60%", lambda t: l(t) >= .60)]
    print("variants tried:", len(V))
    for n, f in V: row(n, [t for t in champ if f(t)], kw, cut)
    print("-- split by 2021-23 / 2024-26 for >=10% and <10%")
    for n, f in V[:2]:
        for nm, g in (("<=2023", lambda t: t["t"][:4] <= "2023"), (">=2024", lambda t: t["t"][:4] >= "2024")):
            row(n + " " + nm, [t for t in champ if f(t) and g(t)], kw, cut)
