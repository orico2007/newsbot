"""Lab run 9 (2026-11-09): follow-up of lab_beta*.py - sizing up the vol60>=1.75 live setup and vol-vs-beta disentangling. Backtest only."""
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
    def feat(t):
        A = AS[t["sym"]]; i = IX[t["sym"]].get(t["t"][:10])
        if i is None or i < 70: return None
        rs, rm = [], []
        for j in range(i - 59, i + 1):
            d, dp = A["t"][j], A["t"][j-1]
            if d not in sc or dp not in sc: return None
            rs.append(A["c"][j]/A["c"][j-1]-1); rm.append(sc[d]/sc[dp]-1)
        ms, mm = sum(rs)/60, sum(rm)/60
        cov = sum((a-ms)*(b-mm) for a, b in zip(rs, rm)); vm = sum((b-mm)**2 for b in rm); vs = sum((a-ms)**2 for a in rs)
        return dict(vol=math.sqrt(vs/59)*100, beta=cov/vm if vm else 1)
    live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            u = dict(t); u["score"] = -m3(t); u["_f"] = feat(t); live.append(u)
    live = [t for t in live if t["_f"]]
    hv = [t for t in live if t["_f"]["vol"] >= 1.75]
    row("LIVE ref (10x12)", live, kw, cut)
    row("vol>=1.75 10x12 (candidate)", hv, kw, cut)
    n = 2
    for sz, mp, pd in ((12, 10, 4), (15, 8, 4), (20, 6, 3), (15, 8, 3), (10, 12, 6), (8, 12, 6)):
        row(f"vol>=1.75 {sz}x{mp} {pd}/day", hv, dict(size_pct=sz, max_pos=mp, per_day=pd), cut); n += 1
    # vol vs beta
    for q in (1.0, 1.27):
        row(f"vol>=1.75 & beta<{q}", [t for t in hv if t["_f"]["beta"] < q], kw, cut)
        row(f"vol<1.75 & beta>={q}", [t for t in live if t["_f"]["vol"] < 1.75 and t["_f"]["beta"] >= q], kw, cut); n += 2
    # selection on early years, confirm later
    for lab_, f in (("early 2021-23", lambda t: t["t"][:4] <= "2023"), ("late 2024-26", lambda t: t["t"][:4] >= "2024")):
        for th in (0, 1.5, 1.75, 2.0):
            S = [t for t in live if t["_f"]["vol"] >= th and f(t)]
            row(f"{lab_} vol>={th}", S, kw, cut)
    print("variants tried this run:", n)
