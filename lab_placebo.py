"""Lab run 39 (2026-11-17): PLACEBO / null-model audit of the LIVE setup. Does the RSI(2) pullback trigger add anything beyond
'buy a high-vol60 uptrend stock on a breadth-washout day in a SPY>200d regime' (same exits/sizing)? Own idea. Backtest only."""
import datetime, random
import lab, sweep, challenger, research
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def placebo(AS, ctx, B, cond, seed, rank=None, F=None):
    rnd = random.Random(seed); out = []
    for sym, A in AS.items():
        n = len(A["c"]); cd = 0
        for i in range(205, n - 2):
            if i < cd: continue
            d = A["t"][i]
            if B.get(d, (0, 0))[0] < .10: continue
            if not (PT.trend_ok(A, i, "long", "s50_200") and PT.gate_ok(ctx, d, "long", "spy200")): continue
            v = challenger.vol60(A, i)
            if v is None or v < 1.75 or not cond(A, i): continue
            r = PT.sim(A, i, "long", 4.0, "prevhl", 7)
            if r:
                r.update(sym=sym, t_exit=r["te"], side="long", rule="placebo")
                r["score"] = rnd.random()
                if rank == "peer": r["score"] = -(F.get((sym, d), {}).get("m3", 0))
                out.append(r); cd = i + 3
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    champ = PT.gen(AS, ctx, challenger.ruleset())
    live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            v = challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10]))
            if v is not None and v >= 1.75: live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0)))
    row("LIVE (signals, peer rank)", live, kw, cut)
    conds = {"any uptrend stock": lambda A, i: True,
             "down close today": lambda A, i: A["c"][i] < A["c"][i-1],
             "5d return < 0": lambda A, i: A["c"][i] < A["c"][i-5],
             "5d return < -3%": lambda A, i: A["c"][i] / A["c"][i-5] - 1 < -0.03,
             "ibs<0.25 (no RSI2)": lambda A, i: A["ibs"][i] is not None and A["ibs"][i] < 0.25}
    for nm, cd in conds.items():
        for seed in (1, 2, 3):
            T = placebo(AS, ctx, B, cd, seed)
            row(f"PLACEBO {nm} rnd s{seed}", T, kw, cut)
        row(f"PLACEBO {nm} peer-rank", placebo(AS, ctx, B, cd, 1, "peer", F), kw, cut)
