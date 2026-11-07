"""Lab run 18 (web idea): intraday-vs-overnight decomposition of the recent decline (Quantpedia 'Short-Term Return Reversals and
Intraday Transactions': intraday returns reverse next week, overnight do not). Applied as filter/rank on the NEW live setup's trades. Backtest only."""
import datetime, math
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def decomp(AS, n):
    out = {}
    for s, A in AS.items():
        o, c = A["o"], A["c"]
        for i in range(n + 1, len(c)):
            intr = sum(math.log(c[k] / o[k]) for k in range(i - n + 1, i + 1) if o[k] > 0) * 100
            ovn = sum(math.log(o[k] / c[k-1]) for k in range(i - n + 1, i + 1) if o[k] > 0) * 100
            out[(s, A["t"][i])] = (intr, ovn)
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    B = breadth_series(AS); F = feats(AS); D3 = decomp(AS, 3); D5 = decomp(AS, 5)
    base = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        if B.get(t["t"][:10], (0, 0))[0] < .10: continue
        f = F.get((t["sym"], t["t"])); base.append(dict(t, score=-f["m3"]) if f else t)
    def sel(fn, rank=None):
        out = []
        for t in base:
            k = (t["sym"], t["t"]); i3 = D3.get(k); i5 = D5.get(k)
            if not i3 or not i5 or not fn(i3, i5): continue
            out.append(dict(t, score=rank(i3, i5)) if rank else t)
        return out
    V = [("LIVE ref", lambda a, b: True, None),
         ("intraday3 < ovn3 (decline mostly intraday)", lambda a, b: a[0] < a[1], None),
         ("intraday3 < -2%", lambda a, b: a[0] < -2, None),
         ("overnight3 > -1% (no gap-down driven)", lambda a, b: a[1] > -1, None),
         ("intraday5 < 0 and ovn5 > intraday5", lambda a, b: b[0] < 0 and b[1] > b[0], None),
         ("rank by most-negative intraday3 (replaces peer rank)", lambda a, b: True, lambda a, b: -a[0]),
         ("rank by intraday3 - ovn3 gap", lambda a, b: True, lambda a, b: a[1] - a[0]),
         ("EXCLUDE intraday3 < ovn3 (opposite check)", lambda a, b: a[0] >= a[1], None)]
    print("variants tried:", len(V))
    for nm, fn, rk in V: row(nm, sel(fn, rk), kw, cut)
