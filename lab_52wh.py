"""Lab idea 2026-11-05: 52-week-high momentum continuation (George & Hwang; Quantpedia). Daily-bar translation, tested with the champion's portfolio simulator."""
import datetime
import lab, research, sweep, challenger
import portfolio_test as PT
from sweep import sim, trend_ok, gate_ok

def signals(AS, ctx, near=0.0, vol=0, hold_gate="spy200", lo=260, cool=10):
    out = []
    for sym, A in AS.items():
        c, n = A["c"], len(A["c"]); cd = 0
        for i in range(lo, n - 2):
            if i < cd: continue
            hi = max(c[i - 252:i])
            if c[i] < hi * (1 - near): continue
            if c[i] <= hi and near == 0: continue
            if not trend_ok(A, i, "long", "s50_200") or not gate_ok(ctx, A["t"][i], "long", hold_gate): continue
            if vol and not (A["vavg"][i] and A["v"][i] > vol * A["vavg"][i]): continue
            if not A["atr"][i] or A["atr"][i] / c[i] > 0.06: continue
            rs = (c[i] / c[i - 63] - 1) * 100
            out.append((sym, i, rs)); cd = i + cool
    return out

def trades(AS, sg, hold, stop, exit_="none"):
    out = []
    for sym, i, rs in sg:
        r = sim(AS[sym], i, "long", stop, exit_, hold)
        if r: r.update(sym=sym, t_exit=r["te"], score=rs, side="long", rule="52wh"); out.append(r)
    return out

def row(name, T, kw, cut):
    P = lab.portfolio(T, **kw); tt = P["trades"]
    l12 = research.stat([t for t in tt if t["t"] >= cut])
    ys = {y: research.stat([t for t in tt if t["t"][:4] == y])["pf_pct"] for y in sorted({t["t"][:4] for t in tt})}
    print(f"{name:42} n={P['n']:4} win={P['win']:5} PF={P['pf_pct']:5} ret={P['ret_pct']:6} mdd={P['mdd']:5} sh={P['sharpe']:5} L12 n={l12['n']} PF={l12['pf_pct']} | {ys}", flush=True)
    return P

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT
    champ = PT.gen(AS, ctx, challenger.ruleset())
    row("CHAMPION", champ, kw, cut)
    PT.gate_ok = challenger.gate2
    V = [("52wh new high, hold10 stop4", dict(near=0), 10, 4.0, "none"),
         ("52wh new high, hold20 stop4", dict(near=0), 20, 4.0, "none"),
         ("52wh new high, hold5 stop4", dict(near=0), 5, 4.0, "none"),
         ("52wh new high + vol>1.5x, hold10", dict(near=0, vol=1.5), 10, 4.0, "none"),
         ("52wh within 2%, hold10", dict(near=0.02), 10, 4.0, "none"),
         ("52wh new high, hold10, stop6", dict(near=0), 10, 6.0, "none"),
         ("52wh new high, exit ma10 (hold20)", dict(near=0), 20, 4.0, "ma10")]
    print("variants tried:", len(V))
    for name, sgkw, hold, stop, ex in V:
        T = trades(AS, signals(AS, ctx, **sgkw), hold, stop, ex)
        P = row(name, T, kw, cut)
        comb = row("   + champion combined (max 12 pos)", champ + T, kw, cut)
