"""Lab run 10 robustness for the ETF 12-1m rotation sleeve: ex-SMH, top-5, 6-month hold shift. Backtest only."""
import datetime
import lab, sweep, challenger, market
import portfolio_test as PT
from lab_52wh import row
from lab_rotation import rotation, monthly_corr
if __name__ == "__main__":
    AS, ctx = sweep.load_all(); bars = lab.load_bars(); spy = bars["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); sk = dict(size_pct=10, max_pos=12, per_day=12, sector_cap=0)
    ck = dict(size_pct=10, max_pos=18, per_day=6)
    etfs = list(market.SECTORS); sel = [e for e in etfs if e not in ("SMH", "XBI", "ITA")]
    V = [("ETF top3 12-1m (base)", etfs, 252, 21, 3, 21), ("ex SMH", [e for e in etfs if e != "SMH"], 252, 21, 3, 21),
         ("11 broad SPDR only (no SMH/XBI/ITA)", sel, 252, 21, 3, 21), ("top5", etfs, 252, 21, 5, 21),
         ("top3 hold 10d (weaker holding)", etfs, 252, 21, 3, 10), ("top3 12m no skip", etfs, 252, 0, 3, 21)]
    print("variants tried:", len(V))
    for name, syms, lb, sk_, n, h in V:
        T = rotation(bars, syms, lb, sk_, n, False, hold=h, ctx=ctx)
        P = row(name, T, sk if n <= 3 else dict(sk, max_pos=12), cut)
        row("   + champion combined", champ + T, ck, cut)
    # year split: early 2021-23 vs 2024-26 on base
    T = rotation(bars, etfs, 252, 21, 3, False, ctx=ctx)
    for lo, hi in (("2021", "2023"), ("2024", "2026")):
        row(f"base {lo}-{hi}", [t for t in T if lo <= t["t"][:4] <= hi], sk, cut)
    from collections import Counter
    print(Counter(t["sym"] for t in T).most_common())
