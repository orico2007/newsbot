"""Lab run 45 (2026-11-20): depth tilt inside the zreg20<-1.5 live setup: does a deeper residual z (more washed out) earn more, and does a size tilt on it help? Own idea. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats
from lab_zscore import zreg
if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(spy) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2; B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(t["t"][:10]); v = challenger.vol60(AS[t["sym"]], i)
            if v is not None and v >= 1.75 and i is not None and i >= 20:
                z = zreg(AS[t["sym"]], i, 20)
                if z < -1.5: live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0), _z=z))
    row("LIVE (zreg<-1.5)", live, kw, cut)
    for lo, hi in ((-1.5, -2.0), (-2.0, -2.5), (-2.5, -9)):
        row(f"z in [{hi},{lo})", [t for t in live if hi <= t["_z"] < lo], kw, cut)
    def tilt(hi, lo, th):
        return [dict(t, pnl_pct=t["pnl_pct"] * (hi if t["_z"] < th else lo)) for t in live]
    V = [(1.25, 1.0, -2.0), (1.5, 1.0, -2.0), (1.25, 0.75, -2.0)]
    for hi, lo, th in V: row(f"size x{hi} if z<{th} else x{lo}", tilt(hi, lo, th), kw, cut)
    print("variants tried:", len(V) + 3)
    for nm, f in (("early 2021-23", lambda t: t["t"][:4] <= "2023"), ("late 2024-26", lambda t: t["t"][:4] >= "2024")):
        row(nm + " ref", [t for t in live if f(t)], kw, cut)
        row(nm + " z<-2", [t for t in live if f(t) and t["_z"] < -2], kw, cut)
        row(nm + " tilt 1.25/1", [u for u in tilt(1.25, 1.0, -2.0) if f(u)], kw, cut)
