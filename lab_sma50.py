"""Lab run 42 (2026-11-18): stock-level medium-trend conditioner (close vs SMA50, SMA50 vs SMA200) on the vol60>=1.75% LIVE setup. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    champ = PT.gen(AS, ctx, challenger.ruleset()); live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            v = challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10]))
            if v is not None and v >= 1.75: live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0)))
    def sma(A, i, n): return sum(A["c"][i-n+1:i+1]) / n
    def ok(t, kind):
        A = AS[t["sym"]]; i = IX[t["sym"]].get(t["t"][:10])
        if i is None or i < 205: return False
        c = A["c"][i]; s50 = sma(A, i, 50); s200 = sma(A, i, 200)
        return {"above50": c > s50, "below50": c < s50, "50>200": s50 > s200, "50<200": s50 < s200}[kind]
    row("LIVE ref", live, kw, cut)
    # above50 keeps all 308 trades and below50 is empty: the live rules already require close>SMA50
    for k in ("50>200", "50<200"):
        sub = [t for t in live if ok(t, k)]
        print(k, "n =", len(sub))
        if len(sub) > 10: row("stock " + k, sub, kw, cut)
    print("variants tried: 4 (2 degenerate)")
