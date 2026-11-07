"""Lab run 16 (own idea): can the breadth>=10% filter replace/loosen the SPY>200d gate on the NEW live setup? Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def spy_feats(spy):
    c = [b["c"] for b in spy]; out = {}
    for i, b in enumerate(spy):
        d = b["t"][:10]
        if i < 200: continue
        s50 = sum(c[i-49:i+1]) / 50; s200 = sum(c[i-199:i+1]) / 200; s200p = sum(c[i-219:i-19]) / 200 if i >= 220 else s200
        hi = max(c[max(0, i-251):i+1])
        out[d] = dict(a50=c[i] > s50, a200=c[i] > s200, dd=c[i] / hi - 1, slope=s200 > s200p)
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    B = breadth_series(AS); F = feats(AS); S = spy_feats(spy)
    def live(gate, cond=None):
        T = PT.gen(AS, ctx, challenger.ruleset(gate=gate)); out = []
        for t in T:
            d = t["t"][:10]; br = B.get(d, (0, 0))[0]
            if br < .10: continue
            if cond and not cond(S.get(d), br): continue
            f = F.get((t["sym"], t["t"]))
            out.append(dict(t, score=-f["m3"]) if f else t)
        return out
    V = [("LIVE SPY>200d + breadth>=10% (ref)", "spy200", None),
         ("no SPY gate + breadth>=10%", "none", None),
         ("not-bear regime + breadth>=10%", "notbear", None),
         ("SPY>50d + breadth>=10%", "none", lambda s, b: s and s["a50"]),
         ("SPY dd from 252d high > -10%", "none", lambda s, b: s and s["dd"] > -.10),
         ("SPY dd > -15%", "none", lambda s, b: s and s["dd"] > -.15),
         ("SPY>200d OR breadth>=25%", "none", lambda s, b: s and (s["a200"] or b >= .25)),
         ("SPY>200d AND 200d slope up", "none", lambda s, b: s and s["a200"] and s["slope"])]
    print("variants tried:", len(V))
    for nm, g, c in V: row(nm, live(g, c), kw, cut)
