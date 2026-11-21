"""Lab run 60 (2026-11-21): run-59 capped 3-tilt size stack through a position-cap / exposure-cap simulator (follow-up named in runs 58/59). Own idea.
Web page checked first (no testable rules): https://alphaarchitect.com/what-drives-momentum-and-reversal/ . Backtest only."""
import datetime, statistics
import lab, sweep, challenger
import portfolio_test as PT
from lab_breadth import breadth_series
from lab_sector import feats

def build():
    AS, ctx = sweep.load_all(); S = lab.load_bars()["SPY"]
    PT.gate_ok = challenger.gate2; B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    rk = challenger.disp_rank(); ib = challenger.spy_ibs(); vr = challenger.spy_volratio(); live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        d = t["t"][:10]
        if B.get(d, (0, 0))[0] >= .10:
            i = IX[t["sym"]].get(d); v = challenger.vol60(AS[t["sym"]], i) if i else None
            if v is not None and v >= 1.75 and i >= 70:
                a = rk.get(d); b = ib.get(d); c = vr.get(d)
                fl = (a is not None and a >= .5, b is not None and b < .3, c is not None and c >= 1.1)
                live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0), fl=fl, k=sum(fl)))
    return S, live

def sim(taken, mult, cap, base=10.0):
    ev = []
    for t in taken: ev.append((t["t"], 1, t)); ev.append((t["t_exit"], 0, t))
    ev.sort(key=lambda e: (e[0], e[1]))  # exits before entries on same date
    eq = 100.0; peak = eq; mdd = 0; open_ = {}; done = []
    for d, kind, t in ev:
        if kind == 1:
            sz = base * mult(t)
            used = sum(open_.values())
            if cap: sz = min(sz, cap - used)
            if sz < 2.0: continue
            open_[id(t)] = sz
        else:
            sz = open_.pop(id(t), None)
            if sz is None: continue
            eq *= 1 + sz / 100 * t["pnl_pct"] / 100; peak = max(peak, eq); mdd = max(mdd, (peak - eq) / peak * 100)
            done.append((t, sz))
    return eq - 100, mdd, done

def pf(done, sel=lambda t: True):
    w = sum(sz * t["pnl_pct"] for t, sz in done if sel(t) and t["pnl_pct"] > 0); l = -sum(sz * t["pnl_pct"] for t, sz in done if sel(t) and t["pnl_pct"] < 0)
    return w / l if l else 9

if __name__ == "__main__":
    S, live = build(); last = S[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = dict(challenger.DEF_PORT); P = lab.portfolio(live, **kw); taken = P["trades"]
    print("live taken", len(taken), "ret", P["ret_pct"], "mdd", P["mdd"])
    f = lambda t, j: 1.25 if t["fl"][j] else .75
    st = lambda t: f(t, 0) * f(t, 1) * f(t, 2)
    clip = lambda lo, hi: (lambda t: min(hi, max(lo, st(t))))
    mean_clip = statistics.mean(clip(.5, 1.5)(t) for t in taken); print("mean clip mult on taken", round(mean_clip, 3))
    V = [("flat 10% (live)", lambda t: 1.0), ("clip .5-1.5", clip(.5, 1.5)), ("clip .5-1.5 / mean (norm)", lambda t: clip(.5, 1.5)(t) / mean_clip),
         ("clip .75-1.25", clip(.75, 1.25)), ("uncapped stack", st)]
    print("%-28s %6s %7s %6s %6s %7s  %s" % ("variant", "cap%", "ret%", "DD%", "PF", "L12 PF", "PF 2021/22/23/24/25/26"))
    for nm, fn in V:
        for cap in (None, 120, 100):
            r, dd, done = sim(taken, fn, cap)
            ys = "/".join("%.2f" % pf(done, lambda t, y=y: t["t"][:4] == y) if any(t["t"][:4] == y for t, _ in done) else "-" for y in "2021 2022 2023 2024 2025 2026".split())
            print("%-28s %6s %7.1f %6.1f %6.2f %7.2f  %s" % (nm, cap or "none", r, dd, pf(done), pf(done, lambda t: t["t"][:10] >= cut), ys))
    print("variants tried: 5 sizing x 3 caps = 15 (mostly the same underlying trades)")
