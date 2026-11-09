"""Lab run 33 (2026-11-09): volatility-expansion conditioning of the LIVE setup (short-term range/ATR ratio at signal). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def mean(x): return sum(x) / len(x)

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
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    def feat(t):
        A = AS[t["sym"]]; i = IX[t["sym"]].get(t["t"][:10])
        if i is None or i < 60 or not A["atr"][i]: return None
        rng = [A["h"][j] - A["l"][j] for j in range(i - 4, i + 1)]
        r50 = [A["h"][j] - A["l"][j] for j in range(i - 49, i + 1)]
        return dict(r5_50=mean(rng) / mean(r50), today=(A["h"][i] - A["l"][i]) / A["atr"][i],
                    gap=(A["o"][i] / A["c"][i-1] - 1) * 100)
    for t in live: t["_f"] = feat(t)
    ok = [t for t in live if t["_f"]]
    print("with feats", len(ok), "of", len(live))
    row("LIVE ref", live, kw, cut)
    V = [("5d range / 50d range >= 1.2 (expansion)", lambda f: f["r5_50"] >= 1.2),
         ("5d range / 50d range < 1.2", lambda f: f["r5_50"] < 1.2),
         ("5d range / 50d range >= 1.0", lambda f: f["r5_50"] >= 1.0),
         ("5d range / 50d range < 1.0 (contraction)", lambda f: f["r5_50"] < 1.0),
         ("signal-day range >= 1.5 ATR", lambda f: f["today"] >= 1.5),
         ("signal-day range < 1.5 ATR", lambda f: f["today"] < 1.5),
         ("signal-day range < 1.0 ATR", lambda f: f["today"] < 1.0)]
    print("variants tried:", len(V) + 1)
    for n, fn in V:
        S = [t for t in ok if fn(t["_f"])]
        row(n, S, kw, cut)
        h = [t for t in S if t["t"][:4] <= "2023"]; l = [t for t in S if t["t"][:4] >= "2024"]
        print("   split <=2023 n=%d | >=2024 n=%d" % (len(h), len(l)))
