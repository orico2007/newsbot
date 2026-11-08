"""Champion vs challengers. Backtests the LIVE mean-reversion setup (champion) against variants on the cached price history
and writes data/challengers.md. It never touches rules.yaml or the bot: a challenger is only a suggestion until a human/Claude
reviews it and changes the live rules on purpose.

A challenger is flagged PROMOTE-CANDIDATE only if it beats the champion on profit factor, total return AND the last 12 months."""
import sys, pathlib, datetime
import lab, research, sweep, market
import portfolio_test as PT

orig_gate = sweep.gate_ok
def gate2(c, d, side, kind):
    return c["reg"].get(d) == "bull" if kind == "bullreg" else orig_gate(c, d, side, kind)
PT.gate_ok = gate2

def R(trig, extra, score, gate="spy200", exit_="prevhl", hold=7, stop=4.0, trend="s50_200"):
    return ("long", trend, trig, gate, extra, exit_, hold, stop, score)

A = dict(trig="r2_5&ibs_0.25", extra="atrpct4", score=90)
E = dict(trig="r2_10&ext_1.5atr", extra="price15", score=65)
F = dict(trig="r2_5", extra="nocrash", score=60)
G = dict(trig="down3_r2_20", extra="nocrash", score=55)

def ruleset(**kw):
    return [R(**x, **kw) for x in (A, E, F)]

DEF_PORT = dict(size_pct=10, max_pos=12, per_day=4)
VARIANTS = [   # name, rules, portfolio kwargs
    ("CHAMPION (live): A+E+F, SPY>200d, breadth>=10%, weakest-peer rank, hold 7, stop 4 ATR, 10% x 12", ruleset(), DEF_PORT, "live"),
    ("previous champion: A+E+F, SPY>200d, no breadth filter, no sector rank", ruleset(), DEF_PORT),
    ("gate: strict bull regime", ruleset(gate="bullreg"), DEF_PORT),
    ("gate: none (always on)", ruleset(gate="none"), DEF_PORT),
    ("hold 5 days", ruleset(hold=5), DEF_PORT),
    ("hold 10 days", ruleset(hold=10), DEF_PORT),
    ("stop 3 ATR", ruleset(stop=3.0), DEF_PORT),
    ("stop 6 ATR", ruleset(stop=6.0), DEF_PORT),
    ("exit: close > MA5 instead of prior high", ruleset(exit_="ma5", hold=7), DEF_PORT),
    ("trend filter: only close > SMA200", ruleset(trend="s200"), DEF_PORT),
    ("add rule G (3 down days)", ruleset() + [R(**G)], DEF_PORT),
    ("A+E only", [R(**A), R(**E)], DEF_PORT),
    ("hold 8 days", ruleset(hold=8), DEF_PORT),
    ("hold 12 days", ruleset(hold=12), DEF_PORT),
    ("hold 15 days", ruleset(hold=15), DEF_PORT),
    ("hold 10 + strict bull gate", ruleset(hold=10, gate="bullreg"), DEF_PORT),
    ("hold 10 + stop 6 ATR", ruleset(hold=10, stop=6.0), DEF_PORT),
    ("A only", [R(**A)], DEF_PORT),
    ("A+E+F, 15 positions, 5/day", ruleset(), dict(size_pct=8, max_pos=15, per_day=5)),
    ("size 8% x 10, 3/day", ruleset(), dict(size_pct=8, max_pos=10, per_day=3)),
    ("size 12% x 10, 4/day", ruleset(), dict(size_pct=12, max_pos=10, per_day=4)),
    # lab run 7 (sector-peer weakness; see data/lab_log.md). Post-processors act on the champion's trade list.
    ("lab: only if sector peers 3d < 0%", ruleset(), DEF_PORT, "peers_lt0"),
    ("lab: rank by weakest sector peers first", ruleset(), DEF_PORT, "peers_rank"),
    ("lab: sector peers 3d < 0% and peers 20d > 0%", ruleset(), DEF_PORT, "peers_lt0_up20"),
    # lab run 10: champion + monthly ETF sector-momentum rotation sleeve (top 3 of 14 sector ETFs by 12-1m return, hold 21d), 18 slots shared
    ("lab: champion + sector-ETF rotation sleeve (top3 12-1m, monthly)", ruleset(), dict(size_pct=10, max_pos=18, per_day=6), "rot_sleeve"),
    # lab run 11: champion + bear-regime long sleeve (SPY<200d, stock>own 200d, rsi2<5, prevhl exit hold 7 stop 4 ATR), same 12 slots
    ("lab: champion + bear-regime long sleeve (SPY<200d, stock>200d, rsi2<5)", ruleset(), DEF_PORT, "bear_sleeve"),
    # lab run 12: only enter when >=10% of the universe has RSI2<10 on the signal day (market-wide washout, not an idiosyncratic dip)
    ("lab: only if >=10% of universe RSI2<10 (breadth washout)", ruleset(), DEF_PORT, "breadth10"),
    # lab run 13: NEW LIVE setup (breadth>=10% + weakest-peer rank) plus bear-regime long sleeve filtered by the same breadth>=10%
    ("lab: live setup (breadth+rank) + bear-regime long sleeve (breadth>=10%)", ruleset(), DEF_PORT, "live_bear10"),
]

def post(T, kind, F):
    """Optional post-processing of a trade list using sector-peer features (lab_sector.feats)."""
    g = lambda t: F.get((t["sym"], t["t"]))
    if kind == "peers_lt0": return [t for t in T if g(t) and g(t)["m3"] < 0]
    if kind == "peers_lt0_up20": return [t for t in T if g(t) and g(t)["m3"] < 0 and g(t)["m20"] > 0]
    if kind == "peers_rank": return [dict(t, score=-g(t)["m3"]) for t in T if g(t)]
    return T

def run():
    AS, ctx = sweep.load_all()
    spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    rows = []
    F = None
    for v in VARIANTS:
        name, rules, kw = v[:3]; T0 = PT.gen(AS, ctx, rules)
        if len(v) > 3 and v[3] == "bear_sleeve":
            import lab_bear
            T0 = T0 + lab_bear.bear_long(AS, ctx)
        elif len(v) > 3 and v[3] == "live":
            import lab_breadth, lab_sector
            B = lab_breadth.breadth_series(AS); F = lab_sector.feats(AS)
            ok = lambda t: B.get(t["t"][:10], (0, 0))[0] >= 0.10
            T0 = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t for t in T0 if ok(t)]
        elif len(v) > 3 and v[3] == "live_bear10":
            import lab_breadth, lab_bear, lab_sector
            B = lab_breadth.breadth_series(AS); F = lab_sector.feats(AS)
            ok = lambda t: B.get(t["t"][:10], (0, 0))[0] >= 0.10
            T0 = [dict(t, score=-F[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in F else t
                  for t in T0 + lab_bear.bear_long(AS, ctx) if ok(t)]
        elif len(v) > 3 and v[3] == "breadth10":
            import lab_breadth
            B = lab_breadth.breadth_series(AS)
            T0 = [t for t in T0 if B.get(t["t"][:10], (0, 0))[0] >= 0.10]
        elif len(v) > 3 and v[3] == "rot_sleeve":
            import lab_rotation
            T0 = T0 + lab_rotation.rotation(lab.load_bars(), list(market.SECTORS), 252, 21, 3, False, ctx=ctx)
        elif len(v) > 3:
            if F is None:
                import lab_sector; F = lab_sector.feats(AS)
            T0 = post(T0, v[3], F)
        P = lab.portfolio(T0, **kw)
        T = P["trades"]; l12 = research.stat([t for t in T if t["t"] >= cut])
        ys = {y: research.stat([t for t in T if t["t"][:4] == y])["pf_pct"] for y in sorted({t["t"][:4] for t in T})}
        rows.append(dict(name=name, n=P["n"], win=P["win"], pf=P["pf_pct"], ret=P["ret_pct"], mdd=P["mdd"], sharpe=P["sharpe"],
                         l12_n=l12["n"], l12_pf=l12["pf_pct"], l12_win=l12["win"], years=ys))
        print(rows[-1]["name"], rows[-1]["pf"], rows[-1]["ret"], flush=True)
    return rows, last

def markdown(rows, last):
    ch = rows[0]
    L = [f"# Champion vs challengers (data through {last})", "",
         "Backtests only. The live bot is **not** changed by this file. A challenger marked PROMOTE-CANDIDATE beat the champion on profit factor, total return, the last 12 months and all but at most one of the non-2022 years; it still needs review before it goes live.", "",
         "| Variant | Trades | Win % | PF | Return % | Max DD % | Sharpe | Last 12m n | Last 12m win % | Last 12m PF | Verdict |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        yrs = [y for y in ch["years"] if y != "2022" and r["years"].get(y) is not None]
        beat = sum(1 for y in yrs if r["years"][y] > ch["years"][y])
        r["beat"] = f"{beat}/{len(yrs)}"
        v = "champion" if r is ch else ("PROMOTE-CANDIDATE" if r["pf"] > ch["pf"] * 1.03 and r["ret"] > ch["ret"] and r["l12_pf"] > ch["l12_pf"] and beat >= len(yrs) - 1 else "")
        if v == "" and r is not ch: v = f"better in {beat}/{len(yrs)} years"
        L.append(f"| {r['name']} | {r['n']} | {r['win']} | {r['pf']} | {r['ret']} | {r['mdd']} | {r['sharpe']} | {r['l12_n']} | {r['l12_win']} | {r['l12_pf']} | {v} |")
    L += ["", "## Profit factor by year", "", "| Variant | " + " | ".join(sorted(ch["years"])) + " |", "|---|" + "---|" * len(ch["years"])]
    for r in rows: L.append(f"| {r['name']} | " + " | ".join(str(r["years"].get(y, "")) for y in sorted(ch["years"])) + " |")
    return "\n".join(L) + "\n"

if __name__ == "__main__":
    rows, last = run()
    out = pathlib.Path("data/challengers.md"); out.parent.mkdir(exist_ok=True); out.write_text(markdown(rows, last), encoding="utf-8")
    print(out.read_text(encoding="utf-8"))
