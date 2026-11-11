"""Lab run 23 (2026-11-11): sector-concentration cap (max simultaneous positions per sector) on the LIVE vol60>=1.75% setup. Own idea (follow-up list of run 22). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
import lab_breadth
from lab_sector import feats

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = dict(challenger.DEF_PORT)
    print("DEF_PORT:", kw)
    T0 = PT.gen(AS, ctx, challenger.ruleset()); B = lab_breadth.breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    hv = lambda t: (lambda v: v is not None and v >= 1.75)(challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10])))
    live = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
            for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10 and hv(t)]
    caps = [0, 1, 2, 3, 4]  # 0/None = no cap
    print("variants tried:", len(caps))
    for c in caps:
        k = dict(kw); k["sector_cap"] = c
        row(f"sector_cap={c or 'none'}", live, k, cut)
    # sector mix of the trades
    from collections import Counter
    import market
    print(Counter(market.SECTOR_OF.get(t["sym"]) for t in live).most_common())
