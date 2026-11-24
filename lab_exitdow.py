"""Lab run 85 (2026-11-24): exit-weekday alignment of the live vol60+zreg setup. Descriptive: PF by exit weekday, and by held days (stop vs time exit). No tuning."""
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
    tt = row("LIVE", live, kw, cut)["trades"]
    wd = lambda s: datetime.date.fromisoformat(s[:10]).weekday()
    for nm, f in [("entry dow", lambda t: wd(t["t"])), ("exit dow", lambda t: wd(t["t_exit"])),
                  ("held", lambda t: min(t["held"], 8))]:
        d = {}
        for t in tt: d.setdefault(f(t), []).append(t)
        print("--", nm)
        for k, v in sorted(d.items()):
            st = research.stat(v); h = [x for x in v if x["t"] >= "2024"]
            print(f"{k} n={st['n']:3} win={st['win']} PF={st['pf_pct']} late n={len(h)} PF={research.stat(h)['pf_pct'] if h else '-'}")
    print("variants tried: 0 (descriptive)")
