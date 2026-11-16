"""Lab round 2026-11-16: size tilt by down-close streak length on the live vol60>=1.75% setup (follow-up of lab_streak.py). Backtest only."""
import datetime, math
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); bars = lab.load_bars(); spy = bars["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); B = breadth_series(AS); F = feats(AS)
    m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    sc = {b["t"][:10]: b["c"] for b in spy}
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    def vol60(t):
        A = AS[t["sym"]]; i = IX[t["sym"]].get(t["t"][:10])
        if i is None or i < 70: return None
        r = [A["c"][j]/A["c"][j-1]-1 for j in range(i-59, i+1)]; m = sum(r)/60
        return math.sqrt(sum((x-m)**2 for x in r)/59)*100
    def streak(t):
        A = AS[t["sym"]]; i = IX[t["sym"]].get(t["t"][:10]); n = 0
        while i - n > 0 and A["c"][i-n] < A["c"][i-n-1]: n += 1
        return n
    live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            v = vol60(t)
            if v and v >= 1.75:
                u = dict(t); u["score"] = -m3(t); u["_s"] = streak(t); live.append(u)
    def tilt(hi, lo, th=3):
        out = []
        for t in live:
            u = dict(t); m = hi if t["_s"] >= th else lo; u["pnl_pct"] = t["pnl_pct"]*m; out.append(u)
        return out
    row("LIVE vol60 (ref)", live, kw, cut)
    for hi, lo in ((1.25, 1.0), (1.25, 0.75), (1.5, 1.0)):
        row(f"streak>=3 x{hi}, else x{lo}", tilt(hi, lo), kw, cut)
    print("variants tried:", 3)
    for lab_, f in (("early 2021-23", lambda t: t["t"][:4] <= "2023"), ("late 2024-26", lambda t: t["t"][:4] >= "2024")):
        S = [t for t in live if f(t)]
        row(f"{lab_} ref", S, kw, cut)
        row(f"{lab_} 1.25/0.75", [u for u in tilt(1.25, .75) if f(u)], kw, cut)
