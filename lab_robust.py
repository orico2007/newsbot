"""Lab run 28 (2026-11-11): robustness of the LIVE vol60>=1.75% setup - random symbol half-splits, drop-top-contributors, odd/even year split.
Own idea (overfitting audit of the universe-level vol filter). Backtest only."""
import datetime, random, statistics
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth
from lab_sector import feats

def pf(T):
    w = sum(t["pnl_pct"] for t in T if t["pnl_pct"] > 0); l = -sum(t["pnl_pct"] for t in T if t["pnl_pct"] < 0)
    return w / l if l else float("inf")

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = challenger.DEF_PORT
    B = lab_breadth.breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    T0 = PT.gen(AS, ctx, challenger.ruleset())
    base = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10]
    vol = lambda t: challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10]))
    hv = [t for t in base if (lambda v: v is not None and v >= 1.75)(vol(t))]
    print("syms", len(AS), "base", len(base), "live", len(hv))
    row("BASE (no vol filter)", base, kw, cut); row("LIVE vol>=1.75", hv, kw, cut)
    # 1) per-trade PF by vol bucket of raw trades (no portfolio) in random symbol halves
    syms = sorted(AS); rnd = random.Random(7); wins = 0; N = 200; gaps = []
    for _ in range(N):
        S = set(rnd.sample(syms, len(syms) // 2))
        a = [t for t in base if t["sym"] in S]; b = [t for t in a if (lambda v: v is not None and v >= 1.75)(vol(t))]
        if len(b) < 20: continue
        g = pf(b) - pf(a); gaps.append(g); wins += g > 0
    print(f"random symbol halves: vol filter raises per-trade PF in {wins}/{len(gaps)}; median gain {statistics.median(gaps):.2f}, 5th pct {sorted(gaps)[len(gaps)//20]:.2f}")
    # 2) drop top-k contributing symbols from LIVE
    from collections import defaultdict
    c = defaultdict(float)
    for t in hv: c[t["sym"]] += t["pnl_pct"]
    top = sorted(c, key=c.get, reverse=True)
    print("top contributors:", [(s, round(c[s], 1)) for s in top[:8]], "share of total", round(sum(c[s] for s in top[:5]) / sum(c.values()), 2))
    for k in (3, 5, 10):
        row(f"LIVE minus top{k} symbols", [t for t in hv if t["sym"] not in set(top[:k])], kw, cut)
    # 3) symbols sets: odd/even alphabetical
    for nm, S in (("even-index syms", set(syms[0::2])), ("odd-index syms", set(syms[1::2]))):
        row("LIVE " + nm, [t for t in hv if t["sym"] in S], kw, cut)
    # 4) time-shuffle placebo: random vol labels on same trades
    pl = []
    for _ in range(300):
        k = len(hv); s = rnd.sample(base, k); pl.append(pf(s))
    print(f"placebo (random {len(hv)} of {len(base)} base trades) per-trade PF: mean {statistics.mean(pl):.2f}, 95th {sorted(pl)[285]:.2f}, max {max(pl):.2f}; live per-trade PF {pf(hv):.2f}")
