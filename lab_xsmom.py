"""Lab run 25: cross-sectional stock 12-1m momentum monthly sleeve (Quantpedia momentum factor), +/- vol60 tilt, combined with champion. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
import lab_breadth, lab_sector, lab_rotation as R
from lab_52wh import row

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); bars = lab.load_bars(); spy = bars["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = challenger.DEF_PORT
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    B = lab_breadth.breadth_series(AS); F = lab_sector.feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    row("LIVE vol175 (champion)", live, kw, cut)
    syms = [s for s in AS if s != "SPY"]
    def volf(T): return [t for t in T if hv(t)]
    V = [("xsmom 12-1 top5 hold21 gate", dict(topn=5, gate=True), False),
         ("xsmom 12-1 top10 hold21 gate", dict(topn=10, gate=True), False),
         ("xsmom 12-1 top10 hold21 nogate", dict(topn=10, gate=False), False),
         ("xsmom 12-1 top10 gate, vol60>=1.75 only", dict(topn=10, gate=True), True),
         ("xsmom 6-1 top10 gate", dict(topn=10, gate=True, lb=126), False),
         ("xsmom 12-1 top20 gate (control, diluted)", dict(topn=20, gate=True), False)]
    print("variants tried:", len(V))
    for name, k, vf in V:
        lb = k.pop("lb", 252); topn = k.pop("topn")
        T = R.rotation(bars, syms, lb, 21, topn, k["gate"], 21, ctx)
        if vf: T = volf(T)
        row(name, T, kw, cut)
        row("   + champion combined", live + T, kw, cut)
