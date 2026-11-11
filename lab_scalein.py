"""Lab run 22 (2026-11-11): scaling in (half at signal close, add half next close only if it closed lower) on the LIVE vol60>=1.75% setup.
Web hint: quantifiedstrategies.substack.com/p/market-timing-scaling-in-and-the (no exact rules given; rules here are my own). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from sweep import SLIP
from lab_52wh import row
import lab_breadth
from lab_sector import feats

def scale(t, A, i, mode):
    """returns modified trade; pnl_pct is on full-size notional (leg weights sum to 1)."""
    e1 = A["c"][i] * (1 + SLIP / 100); pxe = e1 * (1 + t["pnl_pct"] / 100)  # effective exit incl slip
    held = t["held"]
    if held < 2: return dict(t, pnl_pct=0.5 * t["pnl_pct"]) if mode != "delay" else None
    c1 = A["c"][i + 1]; lower = c1 < A["c"][i]
    e2 = c1 * (1 + SLIP / 100); p2 = (pxe - e2) / e2 * 100
    if mode == "scale_lower": return dict(t, pnl_pct=0.5 * t["pnl_pct"] + (0.5 * p2 if lower else 0))
    if mode == "scale_always": return dict(t, pnl_pct=0.5 * t["pnl_pct"] + 0.5 * p2)
    if mode == "delay": return dict(t, pnl_pct=p2) if lower else None
    if mode == "scale_lower_125": return dict(t, pnl_pct=0.5 * t["pnl_pct"] + (0.75 * p2 if lower else 0))

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); bars = lab.load_bars(); spy = bars["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = challenger.DEF_PORT
    T0 = PT.gen(AS, ctx, challenger.ruleset()); B = lab_breadth.breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    row("LIVE (vol175) ref", live, kw, cut)
    V = ["scale_lower", "scale_always", "delay", "scale_lower_125"]
    print("variants tried:", len(V))
    for m in V:
        T = []
        for t in live:
            i = IX[t["sym"]][t["t"][:10]]; u = scale(t, AS[t["sym"]], i, m)
            if u: T.append(u)
        row(m, T, kw, cut)
