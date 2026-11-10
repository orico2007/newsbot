"""Lab run 13 (2026-11-10, web idea): Campbell-Grossman-Wang volume-conditioned reversal. Condition LIVE-setup signals on signal-day relative volume (v/vavg) and 3-day volume trend. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row as _row
from lab_breadth import breadth_series
from lab_sector import feats
def row(nm, T, kw, cut):
    if len(T) < 5: print(f'{nm:42} n={len(T)} (too few)'); return None
    return _row(nm, T, kw, cut)
if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); B = breadth_series(AS); F = feats(AS)
    m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    def feat(t):
        A = AS[t["sym"]]; i = IX[t["sym"]].get(t["t"][:10])
        if i is None or i < 70 or not A["vavg"][i]: return None
        r1 = A["v"][i]/A["vavg"][i]
        v3 = sum(A["v"][i-2:i+1])/3/A["vavg"][i]
        return dict(r1=r1, v3=v3)
    live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            u = dict(t); u["score"] = -m3(t); u["_f"] = feat(t); live.append(u)
    live = [t for t in live if t["_f"]]
    row("LIVE ref", live, kw, cut)
    for k in ("r1", "v3"):
        s = sorted(t["_f"][k] for t in live); q = lambda p: s[int(p*(len(s)-1))]
        print(k, "terciles", round(q(1/3),2), round(q(2/3),2))
        for lo, hi, nm in ((0, q(1/3), "low"), (q(1/3), q(2/3), "mid"), (q(2/3), 99, "high")):
            row(f"{k} {nm} tercile", [t for t in live if lo <= t["_f"][k] < hi], kw, cut)
    for th in (0.8, 1.0, 1.5, 2.0):
        row(f"r1<{th} (low vol)", [t for t in live if t["_f"]["r1"] < th], kw, cut)
        row(f"r1>={th} (high vol)", [t for t in live if t["_f"]["r1"] >= th], kw, cut)
    print("variants: ~ 22")
