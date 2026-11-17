"""Lab run 21b (2026-11-17, web idea): FOMC-meeting cycle (Lucca-Moench pre-FOMC drift; Quantpedia FOMC meeting effect). Tag LIVE-setup (breadth>=10%, peer rank, vol60>=1.75%) signals by trading-day offset to the FOMC decision day. Dates typed from memory of the Fed calendar (decision day, 2nd day of meeting); backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats
FOMC = """2021-01-27 2021-03-17 2021-04-28 2021-06-16 2021-07-28 2021-09-22 2021-11-03 2021-12-15
2022-01-26 2022-03-16 2022-05-04 2022-06-15 2022-07-27 2022-09-21 2022-11-02 2022-12-14
2023-02-01 2023-03-22 2023-05-03 2023-06-14 2023-07-26 2023-09-20 2023-11-01 2023-12-13
2024-01-31 2024-03-20 2024-05-01 2024-06-12 2024-07-31 2024-09-18 2024-11-07 2024-12-18
2025-01-29 2025-03-19 2025-05-07 2025-06-18 2025-07-30 2025-09-17 2025-10-29 2025-12-10
2026-01-28 2026-03-18 2026-04-29 2026-06-17 2026-07-29 2026-09-16 2026-10-28""".split()
def fomc_pos(dates):
    pos = {}
    for f in FOMC:
        j = max((i for i, d in enumerate(dates) if d <= f), default=None)
        if j is None or f > dates[-1]: continue
        for k in range(-6, 8):
            if 0 <= j+k < len(dates): pos.setdefault(dates[j+k], k)
    return pos
if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    dates = [b["t"][:10] for b in spy]; pos = fomc_pos(dates)
    champ = PT.gen(AS, ctx, challenger.ruleset()); B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] < .10: continue
        k = (t["sym"], t["t"]); v = challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10]))
        if v is None or v < 1.75: continue
        live.append(dict(t, score=-F[k]["m3"] if k in F else t.get("score", 0)))
    print("data through", last, "n", len(live))
    row("LIVE (vol60>=1.75)", live, kw, cut)
    P = lambda t: pos.get(t["t"][:10])
    groups = [("entry day before FOMC (-1)", lambda t: P(t) == -1),
              ("entry FOMC day (0)", lambda t: P(t) == 0),
              ("entry day after (+1)", lambda t: P(t) == 1),
              ("FOMC window -2..+1", lambda t: P(t) is not None and -2 <= P(t) <= 1),
              ("hold spans FOMC (-6..-1)", lambda t: P(t) is not None and -6 <= P(t) <= -1),
              ("excluding window -2..+1", lambda t: not (P(t) is not None and -2 <= P(t) <= 1)),
              ("post-FOMC +1..+5", lambda t: P(t) is not None and 1 <= P(t) <= 5)]
    print("variants:", len(groups))
    for n, f in groups: row(n, [t for t in live if f(t)], kw, cut) if len([t for t in live if f(t)])>=5 else print(n, "n<5")
