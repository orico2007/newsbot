"""Lab run 83 (2026-11-24): decay audit of the live vol60+zreg setup - PF / win / avg trade by half-year and quarter, plus trade-count trend. Descriptive only, no tuning."""
import datetime
import lab, sweep, challenger, research
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_zscore import zreg

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"][-1]["t"][:10]
    cut = (datetime.date.fromisoformat(spy) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2; B = breadth_series(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(t["t"][:10]); v = challenger.vol60(AS[t["sym"]], i)
            if v is not None and v >= 1.75 and i is not None and i >= 65 and zreg(AS[t["sym"]], i, 20) < -1.5: live.append(t)
    P = row("LIVE", live, kw, cut); tt = P["trades"]
    print("last data", spy, "trades", len(tt)); print(list(tt[0].keys()))
    def bucket(f):
        d = {}
        for t in tt: d.setdefault(f(t["t"]), []).append(t)
        return d
    for nm, f in [("half-year", lambda s: s[:4] + ("H1" if int(s[5:7]) <= 6 else "H2")),
                  ("quarter", lambda s: s[:4] + "Q" + str((int(s[5:7]) - 1) // 3 + 1))]:
        print("--", nm)
        for k, v in sorted(bucket(f).items()):
            st = research.stat(v); print(f"{k} n={st['n']:3} win={st['win']} PF={st['pf_pct']}")
    print("variants tried: 0 (descriptive)")
