"""Lab run 27 (2026-11-11): SPY regime conditioners (drawdown from 252d high, 20d realized vol, distance over SMA200, SPY>SMA50) on the LIVE vol60>=1.75% setup. Backtest only."""
import datetime, math
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth
from lab_sector import feats

def spy_feats(spy):
    c = [b["c"] for b in spy]; out = {}
    for i in range(200, len(c)):
        r = [c[j] / c[j-1] - 1 for j in range(i-19, i+1)]; m = sum(r) / 20
        vol = math.sqrt(sum((x-m)**2 for x in r) / 19) * math.sqrt(252) * 100
        out[spy[i]["t"][:10]] = dict(dd=c[i] / max(c[max(0, i-251):i+1]) - 1, vol=vol,
                                     d200=c[i] / (sum(c[i-199:i+1]) / 200) - 1, a50=c[i] > sum(c[i-49:i+1]) / 50)
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    B = lab_breadth.breadth_series(AS); F = feats(AS); S = spy_feats(spy)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10]
    live = [t for t in live if hv(t)]
    f = lambda t: S.get(t["t"][:10])
    V = [("LIVE (vol175)", lambda t: True),
         ("SPY dd from 252d high < 3%", lambda t: f(t) and f(t)["dd"] > -.03),
         ("SPY dd 3-10%", lambda t: f(t) and -.10 < f(t)["dd"] <= -.03),
         ("SPY dd >= 3% (any)", lambda t: f(t) and f(t)["dd"] <= -.03),
         ("SPY 20d vol < 15", lambda t: f(t) and f(t)["vol"] < 15),
         ("SPY 20d vol >= 15", lambda t: f(t) and f(t)["vol"] >= 15),
         ("SPY > SMA50", lambda t: f(t) and f(t)["a50"]),
         ("SPY < SMA50 (still >200d)", lambda t: f(t) and not f(t)["a50"]),
         ("SPY within 5% of SMA200", lambda t: f(t) and f(t)["d200"] < .05)]
    for n, k in V: row(n, [t for t in live if k(t)], kw, cut)
    print("variants tried:", len(V) - 1)
