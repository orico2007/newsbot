"""Lab run 41 (2026-11-19): ticker / sector JACKKNIFE of the LIVE vol60>=1.75% setup. Own idea. Backtest only.
Does the edge depend on a few symbols or one sector? Leave-one-sector-out, drop top-k P&L symbols, random 20% symbol drops."""
import datetime, random, statistics as st
import lab, sweep, challenger, market
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def pf_ret(T, kw):
    P = lab.portfolio(T, **kw); return P

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            v = challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10]))
            if v is not None and v >= 1.75: live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0)))
    base = row("LIVE ref", live, kw, cut)
    syms = sorted({t["sym"] for t in live}); print("symbols traded:", len(syms), "of", len(AS))
    # per-symbol standalone contribution (sum pnl_pct of portfolio-accepted trades)
    contrib = {}
    for t in base["trades"]: contrib[t["sym"]] = contrib.get(t["sym"], 0) + t["pnl_pct"]
    rk = sorted(contrib, key=lambda s: -contrib[s]); tot = sum(contrib.values())
    print("top10 symbols by pnl share:", [(s, round(contrib[s] / tot * 100, 1)) for s in rk[:10]])
    nv = 0
    # leave-one-sector-out
    secs = sorted({market.SECTOR_OF.get(s) or "?" for s in syms})
    for sc in secs:
        T = [t for t in live if (market.SECTOR_OF.get(t["sym"]) or "?") != sc]; nv += 1
        row(f"drop sector {sc} ({sum(1 for t in live if (market.SECTOR_OF.get(t['sym']) or '?')==sc)} trades)", T, kw, cut)
    for k in (3, 5, 10):
        T = [t for t in live if t["sym"] not in rk[:k]]; nv += 1
        row(f"drop top-{k} P&L symbols", T, kw, cut)
    # random 20% symbol drops
    res = []
    for seed in range(30):
        rnd = random.Random(seed); drop = set(rnd.sample(syms, max(1, len(syms) // 5)))
        P = lab.portfolio([t for t in live if t["sym"] not in drop], **kw); res.append((P["pf_pct"], P["ret_pct"], P["mdd"]))
    for i, nm in enumerate(("PF", "ret%", "mdd")):
        v = sorted(r[i] for r in res); print(f"random-20%-drop x30 {nm}: min={v[0]} p10={v[3]} med={v[15]} p90={v[26]} max={v[-1]}")
    print("variants: sectors", len(secs), "+3 topk + 30 random draws (distribution, not selection)")
