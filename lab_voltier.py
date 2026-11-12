"""Lab run 31 (2026-11-12): vol60 two-tier sizing. Full size for vol60>=1.75 (live), reduced size for lower-vol signals that the live filter discards.
Reduced size emulated by scaling pnl_pct (PF/return size-weighted; slots still count as 1 each, so exposure is not free). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    base = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10]
    def v(t):
        x = challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])); return -1 if x is None else x
    def tier(lo, k, hi=1.75):
        out = []
        for t in base:
            x = v(t); u = dict(t)
            if x >= hi: out.append(u)
            elif x >= lo:
                u["pnl_pct"] = t["pnl_pct"]*k
                if isinstance(u.get("r"), (int, float)): u["r"] = u["r"]*k
                u["score"] = -1e9 + (u.get("score") or 0)   # low tier fills only after full-size signals
                out.append(u)
        return out
    live = [t for t in base if v(t) >= 1.75]
    row("LIVE ref (vol>=1.75)", live, kw, cut)
    row("no vol filter (base)", base, kw, cut)
    for lo, k in [(1.25, .5), (1.0, .5), (0, .5), (1.25, .33), (0, .33)]:
        row(f"tier: vol>={lo} at {k}x, rest after live", tier(lo, k), kw, cut)
    print("variants tried: 7")
