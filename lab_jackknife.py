"""Lab run 41 (2026-11-18): ticker / sector JACKKNIFE of the vol60>=1.75% LIVE setup (own idea). Is the edge concentrated in a few
names or one sector? Trades are the LIVE trades (peer-rank score); subsets are removed AFTER signal generation, then the portfolio
simulator is re-run (slots freed by removed names go to the next-ranked signals). Backtest only."""
import datetime, random, collections
import lab, sweep, challenger, market
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    champ = PT.gen(AS, ctx, challenger.ruleset()); live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            v = challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10]))
            if v is not None and v >= 1.75: live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0)))
    P0 = row("LIVE ref", live, kw, cut)
    pnl = collections.defaultdict(float); cnt = collections.Counter()
    for t in P0["trades"]:
        pnl[t["sym"]] += t["pnl_pct"]; cnt[t["sym"]] += 1
    print("trade keys:", list(P0["trades"][0].keys()))
    ranked = sorted(pnl, key=lambda s: -pnl[s]); tot = sum(pnl.values())
    print("symbols traded:", len(cnt), "top10 share of pnl: %.0f%%" % (100 * sum(pnl[s] for s in ranked[:10]) / tot if tot else 0))
    print("top10:", [(s, cnt[s], round(pnl[s], 1)) for s in ranked[:10]])
    n = 0
    for k in (5, 10, 20):
        drop = set(ranked[:k]); row(f"drop top-{k} winners (adversarial)", [t for t in live if t["sym"] not in drop], kw, cut); n += 1
    syms = sorted(AS); res = []
    for seed in range(1, 9):
        rnd = random.Random(seed); drop = set(rnd.sample(syms, len(syms) // 5))
        P = row(f"random drop 20% of universe s{seed}", [t for t in live if t["sym"] not in drop], kw, cut); res.append(P); n += 1
    print("random20 PF min/max:", min(p["pf_pct"] for p in res), max(p["pf_pct"] for p in res), "ret min/max:", min(p["ret_pct"] for p in res), max(p["ret_pct"] for p in res))
    secs = collections.Counter(market.SECTOR_OF.get(t["sym"]) for t in live); print("trades by sector:", dict(secs))
    for sc in sorted(secs, key=str):
        row(f"leave out sector {sc}", [t for t in live if market.SECTOR_OF.get(t["sym"]) != sc], kw, cut); n += 1
    print("variants tried:", n)
