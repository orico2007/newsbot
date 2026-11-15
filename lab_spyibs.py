"""Lab run 30: SPY signal-day close location (IBS) and SPY overnight-gap vs intraday split as conditioners of the vol60>=1.75% LIVE setup (own idea; web hint: capitulation/'close near low' market days precede rebounds, unverified). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
import lab_breadth, lab_sector
from lab_52wh import row

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = challenger.DEF_PORT
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    B = lab_breadth.breadth_series(AS); F = lab_sector.feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    S = {}
    for i in range(1, len(spy)):
        b = spy[i]; rng = b["h"] - b["l"]
        S[b["t"][:10]] = dict(ibs=(b["c"] - b["l"]) / rng if rng else .5,
                              gap=(b["o"] / spy[i-1]["c"] - 1) * 100, intra=(b["c"] / b["o"] - 1) * 100)
    g = lambda t, k: S.get(t["t"][:10], {}).get(k)
    row("LIVE vol175", live, kw, cut)
    V = [("SPY IBS<0.3", lambda t: (g(t,"ibs") or 9) < .3), ("SPY IBS>=0.3", lambda t: (g(t,"ibs") or 0) >= .3),
         ("SPY IBS<0.5", lambda t: (g(t,"ibs") or 9) < .5), ("SPY IBS>=0.5", lambda t: (g(t,"ibs") or 0) >= .5),
         ("SPY intraday<0", lambda t: (g(t,"intra") or 9) < 0), ("SPY intraday>=0", lambda t: (g(t,"intra") or -9) >= 0),
         ("SPY gap<-0.3%", lambda t: (g(t,"gap") or 9) < -.3), ("SPY gap>=-0.3%", lambda t: (g(t,"gap") or -9) >= -.3)]
    print("variants tried:", len(V))
    for n, f in V: row(n, [t for t in live if f(t)], kw, cut)
    # size tilt (PF size-weighted): scale pnl by hi when SPY IBS<thr else lo
    def tilt(T, thr, hi, lo):
        out = []
        for t in T:
            m = hi if (g(t, "ibs") if g(t, "ibs") is not None else 9) < thr else lo
            u = dict(t); u["pnl_pct"] = t["pnl_pct"] * m
            if "R" in u: u["R"] = t["R"] * m
            out.append(u)
        return out
    print("--- size tilts (3 more comparisons; total 11)")
    for thr, hi, lo in ((0.3, 1.25, .75), (0.3, 1.5, .5), (0.5, 1.25, .75)):
        row(f"tilt SPY IBS<{thr}: {hi}x else {lo}x", tilt(live, thr, hi, lo), kw, cut)
    print("--- early (<=2023) vs late (>=2024) for IBS<0.3 vs live")
    for nm, f in (("<=2023", lambda t: t["t"][:4] <= "2023"), (">=2024", lambda t: t["t"][:4] >= "2024")):
        row("live " + nm, [t for t in live if f(t)], kw, cut)
        row("IBS<0.3 " + nm, [t for t in live if f(t) and (g(t,"ibs") or 9) < .3], kw, cut)
