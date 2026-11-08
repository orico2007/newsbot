"""Lab run 24 (2026-11-08): 52-week-high proximity conditioning of the LIVE setup (web idea: cxoadvisory 'proximity to 52-week high and short-term reversal'). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def prox(AS, t):
    A = AS[t["sym"]]
    try: i = A["t"].index(t["t"])
    except ValueError: return None
    if i < 252: return None
    return A["c"][i] / max(A["c"][i-252:i+1])

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); B = breadth_series(AS); F = feats(AS)
    m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            u = dict(t); u["score"] = -m3(t); u["px"] = prox(AS, t); live.append(u)
    row("LIVE ref", live, kw, cut)
    ok = [t for t in live if t["px"] is not None]; print("with prox:", len(ok), "of", len(live))
    V = [("within 10% of 252d high", lambda p: p >= .90), ("within 20%", lambda p: p >= .80),
         ("more than 10% below high", lambda p: p < .90), ("more than 20% below", lambda p: p < .80),
         ("more than 30% below", lambda p: p < .70)]
    print("variants tried:", len(V))
    for n, fn in V: row(n, [t for t in ok if fn(t["px"])], kw, cut)
    for lab_, sgn in (("rank nearest-high first", -1), ("rank farthest-from-high first", 1)):
        T = []
        for t in ok:
            u = dict(t); u["score"] = sgn * t["px"] + 0; T.append(u)
        row(lab_, T, kw, cut)
