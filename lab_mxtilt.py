"""Lab run 53 (2026-11-21): size tilt on mx10 (share of 10d drop from the single largest down day), follow-up of run 51, on vol60>=1.75% LIVE setup. Own idea. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats
from lab_infodisc import idisc

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(spy) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2; B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(t["t"][:10]); v = challenger.vol60(AS[t["sym"]], i) if i else None
            if v is not None and v >= 1.75 and i >= 30:
                live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0), mx=idisc(AS[t["sym"]]["c"], i, 10)[1]))
    row("LIVE ref", live, kw, cut)
    q = sorted(t["mx"] for t in live); print("mx10 quartiles", [round(q[int(len(q)*p)], 3) for p in (.25,.5,.75)])
    med = q[len(q)//2]; p75 = q[int(len(q)*.75)]
    def tilt(T, thr, hi, lo):
        out = []
        for t in T:
            m = hi if t["mx"] >= thr else lo
            u = dict(t); u["pnl_pct"] = t["pnl_pct"]*m
            if "R" in u: u["R"] = t["R"]*m
            out.append(u)
        return out
    V = [(med, 1.25, .75), (med, 1.5, .5), (p75, 1.5, 1.0), (med, 1.0, .5)]
    for thr, hi, lo in V: row(f"tilt mx10>={thr:.2f}: {hi}x else {lo}x", tilt(live, thr, hi, lo), kw, cut)
    print("variants tried:", len(V))
    print("--- early(<=2023) vs late(>=2024), tilt 1.5/0.5 at median (median fixed from full sample)")
    for nm, f in (("<=2023", lambda t: t["t"][:4] <= "2023"), (">=2024", lambda t: t["t"][:4] >= "2024")):
        S = [t for t in live if f(t)]
        row("live " + nm, S, kw, cut); row("tilt " + nm, tilt(S, med, 1.5, .5), kw, cut)
