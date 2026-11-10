"""Lab run 6 (2026-11-10): SPY-dip regime as size-up / priority signal on champion entries. Backtest only.
Idea source: follow-up of the 2026-11-05 fear-filter result (champion edge is richest after SPY dips)."""
import datetime, copy
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_fear import spy_feats

def scaled(champ, F, fn):
    out = []
    for t in champ:
        f = F.get(t["t"][:10]); m = fn(f) if f else 1.0
        u = dict(t); u["pnl_pct"] = t["pnl_pct"] * m
        if "R" in u: u["R"] = t["R"] * m
        out.append(u)
    return out

def prio(champ, F, fn):
    out = []
    for t in champ:
        f = F.get(t["t"][:10]); u = dict(t); u["score"] = fn(f, t) if f else -99; out.append(u)
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); F = spy_feats()
    row("CHAMPION", champ, kw, cut)
    S = [("1.5x size if SPY 3d < -1%", lambda f: 1.5 if f[1] < -1 else 1.0),
         ("1.5x if 3d<-1%, 0.5x otherwise", lambda f: 1.5 if f[1] < -1 else 0.5),
         ("2x if SPY 3d < -2%", lambda f: 2.0 if f[1] < -2 else 1.0),
         ("1.25x if 3d<-1%, 0.75x else", lambda f: 1.25 if f[1] < -1 else 0.75)]
    print("variants tried:", len(S) + 2)
    for n, fn in S: row(n, scaled(champ, F, fn), kw, cut)
    row("priority: deepest SPY 3d dip first", prio(champ, F, lambda f, t: -f[1]), kw, cut)
    row("priority: lowest stock score first (ctrl)", prio(champ, F, lambda f, t: -t.get("score", 0)), kw, cut)
