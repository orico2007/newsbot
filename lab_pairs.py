"""Lab run 17 (web-seeded relative-value idea): long-only pairs-style reversion. Stock underperforms its most-correlated peer
(partner chosen once a year from the PRIOR 252 days only) by z standard deviations of the 60d log spread -> long the laggard. Backtest only."""
import datetime, math
import lab, sweep, challenger
import portfolio_test as PT
from sweep import sim, trend_ok, gate_ok
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def partners(AS):
    """(sym, year) -> partner sym, from correlation of daily returns over the 252 days before that year's first session."""
    dates = sorted({d for A in AS.values() for d in A["t"]}); ix = {s: {t: i for i, t in enumerate(A["t"])} for s, A in AS.items()}
    R = {}
    for s, A in AS.items():
        c = A["c"]; R[s] = {A["t"][i]: c[i] / c[i-1] - 1 for i in range(1, len(c))}
    out = {}
    for y in range(2021, 2027):
        first = next(d for d in dates if d[:4] == str(y)); prior = [d for d in dates if d < first][-252:]
        if len(prior) < 200: continue
        vec = {}
        for s in AS:
            v = [R[s].get(d) for d in prior]
            if sum(x is not None for x in v) >= 200: vec[s] = v
        def corr(a, b):
            xs = [(x, y2) for x, y2 in zip(a, b) if x is not None and y2 is not None]
            n = len(xs); mx = sum(x for x, _ in xs) / n; my = sum(y2 for _, y2 in xs) / n
            sxy = sum((x - mx) * (y2 - my) for x, y2 in xs); sx = sum((x - mx) ** 2 for x, _ in xs); sy = sum((y2 - my) ** 2 for _, y2 in xs)
            return sxy / math.sqrt(sx * sy) if sx and sy else -1
        for s in vec:
            best = max(((corr(vec[s], vec[p]), p) for p in vec if p != s), default=None)
            if best and best[0] > 0.5: out[(s, str(y))] = best[1]
    return out

def signals(AS, ctx, P, zthr=-2.0, look=60, extra=None, gate="spy200"):
    out = []; ix = {s: {t: i for i, t in enumerate(A["t"])} for s, A in AS.items()}
    for s, A in AS.items():
        c = A["c"]; cd = 0
        for i in range(max(look, 210), len(c) - 2):
            if i < cd: continue
            d = A["t"][i]; p = P.get((s, d[:4]))
            if not p: continue
            B = AS[p]; j = ix[p].get(d)
            if j is None or j < look: continue
            # aligned window by dates of s
            sp = []
            for k in range(i - look, i + 1):
                jj = ix[p].get(A["t"][k])
                if jj is None: break
                sp.append(math.log(c[k] / B["c"][jj]))
            if len(sp) < look + 1: continue
            m = sum(sp[:-1]) / look; sd = math.sqrt(sum((x - m) ** 2 for x in sp[:-1]) / look)
            if not sd: continue
            z = (sp[-1] - m) / sd
            if z > zthr: continue
            if not trend_ok(A, i, "long", "s200") or not gate_ok(ctx, d, "long", gate): continue
            if not A["atr"][i] or A["atr"][i] / c[i] > 0.09: continue
            if extra and not extra(A, i): continue
            out.append((s, i, -z)); cd = i + 5
    return out

def trades(AS, sg, hold=7, stop=4.0, ex="prevhl"):
    out = []
    for s, i, rs in sg:
        r = sim(AS[s], i, "long", stop, ex, hold)
        if r: r.update(sym=s, t_exit=r["te"], score=rs, side="long", rule="pair"); out.append(r)
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); B = breadth_series(AS); F = feats(AS)
    br = lambda t: B.get(t["t"][:10], (0, 0))[0]
    live = []
    for t in champ:
        if br(t) < .10: continue
        f = F.get((t["sym"], t["t"])); live.append(dict(t, score=-f["m3"]) if f else t)
    P = partners(AS); print("pairs:", len(P))
    row("LIVE (breadth+rank) ref", live, kw, cut)
    V = [("z<-2, h7 prevhl", dict(zthr=-2.0), 7), ("z<-2.5, h7", dict(zthr=-2.5), 7), ("z<-2 & rsi2<10", dict(zthr=-2.0, extra=lambda A, i: A["r2"][i] is not None and A["r2"][i] < 10), 7),
         ("z<-2, h5", dict(zthr=-2.0), 5), ("z<-1.5 & rsi2<10", dict(zthr=-1.5, extra=lambda A, i: A["r2"][i] is not None and A["r2"][i] < 10), 7)]
    print("variants tried:", len(V))
    for nm, kwg, h in V:
        T = trades(AS, signals(AS, ctx, P, **kwg), h)
        row(nm, T, kw, cut)
        row("   + LIVE combined", live + T, kw, cut)
        Tb = [t for t in T if br(t) >= .10]
        row("   breadth>=10% alone", Tb, kw, cut)
