"""Lab idea 2026-11-05 (run 3): stock-selection ranking of same-day champion signals (RS vs SPY, low vol, liquidity, dip depth). Backtest only."""
import datetime, copy
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row

def feats(AS):
    spy = AS.get("SPY") or None
    bars = lab.load_bars()["SPY"]; sidx = {b["t"][:10]: i for i, b in enumerate(bars)}
    F = {}
    for sym, A in AS.items():
        for i in range(64, len(A["c"])):
            d = A["t"][i]; si = sidx.get(d[:10])
            if si is None or si < 64: continue
            rs = (A["c"][i] / A["c"][i-63] - 1) - (bars[si]["c"] / bars[si-63]["c"] - 1)
            atrp = (A["atr"][i] or 0) / A["c"][i]
            dv = sum(A["c"][k] * A["v"][k] for k in range(i-19, i+1)) / 20
            F[(sym, d)] = dict(rs=rs, atrp=atrp, dv=dv, r2=A["r2"][i] if A["r2"][i] is not None else 50, ibs=A["ibs"][i] if A["ibs"][i] is not None else .5, ret3=A["ret3"][i] or 0)
    return F

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); F = feats(AS)
    row("CHAMPION (rule score order)", champ, kw, cut)
    V = [("rank: high RS63 vs SPY", lambda f: f["rs"]),
         ("rank: low RS63 (weakest first)", lambda f: -f["rs"]),
         ("rank: low ATR% (calm first)", lambda f: -f["atrp"]),
         ("rank: high ATR% (volatile first)", lambda f: f["atrp"]),
         ("rank: high dollar volume", lambda f: f["dv"]),
         ("rank: deepest dip (lowest RSI2)", lambda f: -f["r2"]),
         ("rank: lowest IBS", lambda f: -f["ibs"]),
         ("rank: worst 3d return", lambda f: -f["ret3"])]
    print("variants tried:", len(V))
    for name, fn in V:
        T = []
        for t in champ:
            f = F.get((t["sym"], t["t"]))
            if not f: continue
            u = dict(t); u["score"] = fn(f); T.append(u)
        row(name, T, kw, cut)
        # within rule-tier: tier score dominates
        T2 = []
        for t in champ:
            f = F.get((t["sym"], t["t"]))
            if not f: continue
            u = dict(t); u["score"] = t["score"] * 1e6 + fn(f) * (1e3 if abs(fn(f)) < 1e3 else 1e-3); T2.append(u)
        row("   within rule tier", T2, kw, cut)
