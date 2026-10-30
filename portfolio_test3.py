from portfolio_test import *
import research, lab
if __name__ == "__main__":
    AS, ctx = load_all()
    spy = lab.load_bars()["SPY"]; c = [b["c"] for b in spy]
    # שער "שוק בריא": SPY מעל SMA200 וגם SMA50 מעל SMA200 (golden), ועל מגמה עולה של SMA200
    s50, s200 = sweep.sma_arr(c, 50), sweep.sma_arr(c, 200)
    ctx["healthy"] = {spy[i]["t"][:10]: (s50[i] > s200[i] and c[i] > s200[i] and s200[i] >= s200[i - 20]) for i in range(220, len(spy)) if s200[i] and s50[i]}
    ctx["bull_only"] = {d: ctx["reg"].get(d) == "bull" for d in ctx["healthy"]}
    orig = sweep.gate_ok
    def gate2(ctx_, d, side, kind):
        if kind == "healthy": return ctx_["healthy"].get(d, False)
        if kind == "bullreg": return ctx_["reg"].get(d) == "bull"
        return orig(ctx_, d, side, kind)
    import portfolio_test as PT; PT.gate_ok = gate2
    for g in ("spy200", "healthy", "bullreg"):
        A = ("long", "s50_200", "r2_5&ibs_0.25", g, "atrpct4", "prevhl", 7, 4.0, 90)
        E = ("long", "s50_200", "r2_10&ext_1.5atr", g, "price15", "prevhl", 7, 4.0, 65)
        t = PT.gen(AS, ctx, [A, E]); P_ = lab.portfolio(t)
        ys = {y: (lambda s: (s["n"], s["win"], s["pf_pct"]))(research.stat([x for x in P_["trades"] if x["t"][:4] == y])) for y in sorted({x["t"][:4] for x in P_["trades"]})}
        print(f"A+E gate={g:8} n={P_['n']:4} win={P_['win']:5} PF={P_['pf_pct']} ret={P_['ret_pct']:5} mdd={P_['mdd']} | {ys}")
    # כמה ימים בכל שנה השער פתוח
    from collections import Counter
    for k in ("healthy",):
        cnt = Counter(d[:4] for d, v in ctx[k].items() if v); tot = Counter(d[:4] for d in ctx[k])
        print(k, {y: f"{cnt[y]}/{tot[y]}" for y in sorted(tot)})
