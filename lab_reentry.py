"""Lab run 23 (2026-11-07): same-symbol re-entry memory on the LIVE setup (skip/favour a signal if the stock's previous signal-trade lost recently). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def days(a, b): return (datetime.date.fromisoformat(b[:10]) - datetime.date.fromisoformat(a[:10])).days

def filt(live, mode, N):
    """History = the unfiltered live signal-trade list (path-independent approximation). mode: 'skip_loss', 'skip_any', 'only_loss', 'only_win'."""
    by = {}
    for t in sorted(live, key=lambda x: x["t"]): by.setdefault(t["sym"], []).append(t)
    out = []
    for sym, L in by.items():
        for k, t in enumerate(L):
            prev = [p for p in L[:k] if p["t_exit"][:10] < t["t"][:10] and days(p["t_exit"], t["t"]) <= N]
            p = prev[-1] if prev else None
            if mode == "skip_loss" and p and p["pnl_pct"] < 0: continue
            if mode == "skip_any" and p: continue
            if mode == "only_loss" and not (p and p["pnl_pct"] < 0): continue
            if mode == "only_win" and not (p and p["pnl_pct"] > 0): continue
            out.append(t)
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); B = breadth_series(AS); F = feats(AS)
    m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            u = dict(t); u["score"] = -m3(t); live.append(u)
    row("LIVE ref", live, kw, cut)
    V = [("skip if prev trade lost <=20d", "skip_loss", 20), ("skip if prev trade lost <=60d", "skip_loss", 60),
         ("skip any re-entry <=20d", "skip_any", 20), ("only re-entry after loss <=20d", "only_loss", 20),
         ("only re-entry after win <=20d", "only_win", 20)]
    print("variants tried:", len(V))
    for name, mode, N in V:
        T = filt(live, mode, N); print("  signals", len(T), "of", len(live)); row(name, T, kw, cut)
