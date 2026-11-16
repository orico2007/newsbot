"""Lab run 21 (2026-11-16): exit overlays on the LIVE setup trades (early cut of non-working trades, profit lock, breakeven stop).
Web hint: short holds / fast exits improve pullback Sharpe (https://quantpedia.com/testing-an-ai-assisted-research-workflow-for-multi-asset-pullback-strategy-discovery/ , unverified). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
import lab_breadth, lab_sector
from lab_52wh import row
SLIP = sweep.SLIP

def resim(A, i, stop_k=4.0, hold=7, cut_day=None, cut_thr=0.0, lock_atr=None, be_atr=None):
    c, h, l, o = A["c"], A["h"], A["l"], A["o"]; n = len(c); atr = A["atr"][i]
    entry = c[i] * (1 + SLIP / 100); stop = entry - stop_k * atr; last = min(n - 1, i + hold)
    px, j_exit = None, last; be = False
    for j in range(i + 1, last + 1):
        if o[j] <= stop: px = o[j]; j_exit = j; break
        if l[j] <= stop: px = stop; j_exit = j; break
        if c[j] > h[j - 1]: px = c[j]; j_exit = j; break
        if lock_atr and c[j] >= entry + lock_atr * atr: px = c[j]; j_exit = j; break
        if cut_day and j - i == cut_day and c[j] < entry * (1 + cut_thr): px = c[j]; j_exit = j; break
        if be_atr:
            if be and l[j] <= entry: px = max(entry, min(o[j], entry)) if o[j] > entry else o[j]; j_exit = j; break
            if c[j] >= entry + be_atr * atr: be = True
    if px is None: px = c[last]
    px *= (1 - SLIP / 100)
    return (px - entry) / entry * 100, A["t"][j_exit]

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
    def variant(**k):
        out = []
        for t in live:
            i = IX[t["sym"]][t["t"][:10]]; p, te = resim(AS[t["sym"]], i, **k)
            u = dict(t); u["pnl_pct"] = p; u["t_exit"] = te; u["te"] = te
            if "R" in u: u["R"] = p / (4.0 * AS[t["sym"]]["atr"][i] / AS[t["sym"]]["c"][i] * 100)
            out.append(u)
        return out
    row("LIVE ref (vol175)", live, kw, cut)
    row("resim base (check)", variant(), kw, cut)
    V = [("cut day3 if below entry", dict(cut_day=3)), ("cut day2 if below entry", dict(cut_day=2)),
         ("cut day4 if below entry-1%", dict(cut_day=4, cut_thr=-0.01)),
         ("cut day5 if below entry", dict(cut_day=5)),
         ("profit lock +1.5 ATR close", dict(lock_atr=1.5)), ("profit lock +1.0 ATR close", dict(lock_atr=1.0)),
         ("breakeven stop after +1 ATR close", dict(be_atr=1.0)), ("hold 5 (control)", dict(hold=5)), ("hold 10 (control)", dict(hold=10))]
    print("variants tried:", len(V) + 1)
    for n, k in V: row(n, variant(**k), kw, cut)
