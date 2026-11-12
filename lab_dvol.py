"""Lab run 36 (2026-11-12): liquidity tier (20d avg dollar volume, cross-sectional percentile) as conditioner of the LIVE vol60>=1.75% setup.
Web-seeded (Medhat & Novy-Marx short-run reversal: stronger in less liquid stocks). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth

def dv_table(raw, AS):
    """date -> {sym: 20d average dollar volume} for symbols in AS."""
    DV = {}
    for s, bars in raw.items():
        if s not in AS: continue
        for i in range(20, len(bars)):
            DV.setdefault(bars[i]["t"][:10], {})[s] = sum(b["c"] * b["v"] for b in bars[i-19:i+1]) / 20
    return DV

def dv_pct(DV, s, d):
    m = DV.get(d, {})
    if s not in m or len(m) < 20: return None
    return sum(1 for x in m.values() if x < m[s]) / len(m)

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    B = lab_breadth.breadth_series(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    raw = lab.load_bars(); DV = {}
    for s, bars in raw.items():
        if s not in AS: continue
        for i in range(20, len(bars)):
            DV.setdefault(bars[i]["t"][:10], {})[s] = sum(b["c"] * b["v"] for b in bars[i-19:i+1]) / 20
    def pct(s, d):
        m = DV.get(d, {}); 
        if s not in m or len(m) < 20: return None
        return sum(1 for x in m.values() if x < m[s]) / len(m)
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    base = [t for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    for t in base: t["_p"] = pct(t["sym"], t["t"][:10])
    V = [("LIVE ref", lambda p: True), ("low liquidity half (p<0.5)", lambda p: p is not None and p < .5),
         ("high liquidity half (p>=0.5)", lambda p: p is not None and p >= .5),
         ("bottom third", lambda p: p is not None and p < 1/3), ("top third", lambda p: p is not None and p >= 2/3)]
    print("variants tried:", len(V) - 1)
    for n, f in V: row(n, [t for t in base if f(t["_p"])], kw, cut)
    print("--- follow-ups (3 more variants; total 7)")
    row("skip bottom third", [t for t in base if t["_p"] is not None and t["_p"] >= 1/3], kw, cut)
    row("rank by liquidity pct (high first)", [dict(t, score=t["_p"] or 0) for t in base], kw, cut)
    row("size 1.5x top half / 0.5x low half", [dict(t, pnl_pct=t["pnl_pct"] * (1.5 if (t["_p"] or 0) >= .5 else .5), **({"R": t["R"] * (1.5 if (t["_p"] or 0) >= .5 else .5)} if "R" in t else {})) for t in base], kw, cut)
