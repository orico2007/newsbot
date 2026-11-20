"""Lab run 46 (2026-11-20): CCI(14) / Williams %R(14) / Keltner depth conditioners of the vol60>=1.75% LIVE setup. Web-seeded (QuantifiedStrategies Williams %R pages, https://www.quantifiedstrategies.com/williams-r-trading-strategy/ , https://quantifiedstrategies.substack.com/p/we-tested-williams-r-on-all-nasdaq ; claims unverified). Backtest only."""
import datetime, statistics as S
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def cci(A, i, n=14):
    tp = [(A["h"][k]+A["l"][k]+A["c"][k])/3 for k in range(i-n+1, i+1)]; m = sum(tp)/n
    md = sum(abs(x-m) for x in tp)/n
    return (tp[-1]-m)/(0.015*md) if md else 0
def wr(A, i, n=14):
    h = max(A["h"][i-n+1:i+1]); l = min(A["l"][i-n+1:i+1])
    return -100*(h-A["c"][i])/(h-l) if h > l else -50
def kelt(A, i, n=20):
    m = sum(A["c"][i-n+1:i+1])/n
    tr = [max(A["h"][k]-A["l"][k], abs(A["h"][k]-A["c"][k-1]), abs(A["l"][k]-A["c"][k-1])) for k in range(i-n+1, i+1)]
    return (m-A["c"][i])/(sum(tr)/n)

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(spy) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2; B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(t["t"][:10]); v = challenger.vol60(AS[t["sym"]], i) if i else None
            if v is not None and v >= 1.75 and i >= 20:
                A = AS[t["sym"]]
                live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0), _cci=cci(A, i), _wr=wr(A, i), _k=kelt(A, i)))
    row("LIVE ref", live, kw, cut)
    for k in ("_cci", "_wr", "_k"):
        q = sorted(t[k] for t in live); print(k, "quartiles", [round(q[int(len(q)*p)], 2) for p in (.25, .5, .75)])
    V = [("CCI14 < -100", lambda t: t["_cci"] < -100), ("CCI14 < -150", lambda t: t["_cci"] < -150), ("CCI14 >= -100", lambda t: t["_cci"] >= -100),
         ("WR14 < -90", lambda t: t["_wr"] < -90), ("WR14 < -97", lambda t: t["_wr"] < -97), ("WR14 >= -90", lambda t: t["_wr"] >= -90),
         ("Keltner depth >= 1.5 ATR", lambda t: t["_k"] >= 1.5), ("Keltner depth >= 2.5 ATR", lambda t: t["_k"] >= 2.5), ("Keltner depth < 2.5", lambda t: t["_k"] < 2.5)]
    for nm, f in V:
        sub = [t for t in live if f(t)]
        if len(sub) > 15: row(nm, sub, kw, cut)
        else: print(nm, "n=", len(sub))
    print("variants tried:", len(V))
