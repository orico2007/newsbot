"""Lab run 66 (2026-11-22): does the run-64 20d-return flag (stock 20d ret > -5%) add to the run-59 clipped 3-tilt stack? Own idea. Backtest only."""
import datetime, statistics
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_wftilt import scaled

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); S = lab.load_bars()["SPY"]
    cut = (datetime.date.fromisoformat(S[-1]["t"][:10]) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2; B = breadth_series(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    rk = challenger.disp_rank(); ib = challenger.spy_ibs(); vr = challenger.spy_volratio()
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        d = t["t"][:10]
        if B.get(d, (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(d); v = challenger.vol60(AS[t["sym"]], i) if i else None
            if v is not None and v >= 1.75 and i >= 70:
                a = rk.get(d); b = ib.get(d); c = vr.get(d); cl = AS[t["sym"]]["c"]
                r20 = cl[i] / cl[i-20] - 1
                fl = [a is not None and a >= .5, b is not None and b < .3, c is not None and c >= 1.1, r20 > -.05]
                live.append(dict(t, fl=fl))
    f = lambda t, j: 1.25 if t["fl"][j] else .75
    s3 = lambda t: min(1.5, max(.5, f(t,0)*f(t,1)*f(t,2)))
    s4 = lambda t: min(1.5, max(.5, f(t,0)*f(t,1)*f(t,2)*f(t,3)))
    s3f = lambda t: s3(t) if t["fl"][3] else 0
    row("LIVE ref", live, kw, cut)
    for nm, fn in (("3-tilt clip", s3), ("4-tilt (+r20>-5%)", s4), ("3-tilt, drop r20<=-5%", s3f)):
        ms = [fn(t) for t in live]; m = statistics.mean(ms)
        print(nm, "mean mult %.2f" % m)
        row(nm, scaled(live, ms), kw, cut); row(nm + " norm", scaled(live, [x/m for x in ms]), kw, cut)
    print("overlap of r20 flag with others:", [round(sum(1 for t in live if t["fl"][3] and t["fl"][j])/max(1,sum(t["fl"][3] for t in live)),2) for j in range(3)])
    print("variants tried: 3 (x2 norm)")
