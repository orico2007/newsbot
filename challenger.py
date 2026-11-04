"""Champion vs challengers. Backtests the LIVE mean-reversion setup (champion) against variants on the cached price history
and writes data/challengers.md. It never touches rules.yaml or the bot: a challenger is only a suggestion until a human/Claude
reviews it and changes the live rules on purpose.

A challenger is flagged PROMOTE-CANDIDATE only if it beats the champion on profit factor, total return AND the last 12 months."""
import sys, pathlib, datetime
import lab, research, sweep
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
    ("CHAMPION (live): A+E+F, SPY>200d, hold 7, stop 4 ATR, 10% x 12", ruleset(), DEF_PORT),
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
    ("size 8% x 10, 3/day", ruleset(), dict(size_pct=8, max_pos=10, per_day=3)),
    ("size 12% x 10, 4/day", ruleset(), dict(size_pct=12, max_pos=10, per_day=4)),
]

def run():
    AS, ctx = sweep.load_all()
    spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    rows = []
    for name, rules, kw in VARIANTS:
        P = lab.portfolio(PT.gen(AS, ctx, rules), **kw)
        T = P["trades"]; l12 = research.stat([t for t in T if t["t"] >= cut])
        ys = {y: research.stat([t for t in T if t["t"][:4] == y])["pf_pct"] for y in sorted({t["t"][:4] for t in T})}
        rows.append(dict(name=name, n=P["n"], win=P["win"], pf=P["pf_pct"], ret=P["ret_pct"], mdd=P["mdd"], sharpe=P["sharpe"],
                         l12_n=l12["n"], l12_pf=l12["pf_pct"], l12_win=l12["win"], years=ys))
        print(rows[-1]["name"], rows[-1]["pf"], rows[-1]["ret"], flush=True)
    return rows, last

def markdown(rows, last):
    ch = rows[0]
    L = [f"# Champion vs challengers (data through {last})", "",
         "Backtests only. The live bot is **not** changed by this file. A challenger marked PROMOTE-CANDIDATE beat the champion on profit factor, total return and the last 12 months; it still needs review before it goes live.", "",
         "| Variant | Trades | Win % | PF | Return % | Max DD % | Sharpe | Last 12m n | Last 12m win % | Last 12m PF | Verdict |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        v = "champion" if r is ch else ("PROMOTE-CANDIDATE" if r["pf"] > ch["pf"] * 1.03 and r["ret"] > ch["ret"] and r["l12_pf"] > ch["l12_pf"] else "")
        L.append(f"| {r['name']} | {r['n']} | {r['win']} | {r['pf']} | {r['ret']} | {r['mdd']} | {r['sharpe']} | {r['l12_n']} | {r['l12_win']} | {r['l12_pf']} | {v} |")
    L += ["", "## Profit factor by year", "", "| Variant | " + " | ".join(sorted(ch["years"])) + " |", "|---|" + "---|" * len(ch["years"])]
    for r in rows: L.append(f"| {r['name']} | " + " | ".join(str(r["years"].get(y, "")) for y in sorted(ch["years"])) + " |")
    return "\n".join(L) + "\n"

if __name__ == "__main__":
    rows, last = run()
    out = pathlib.Path("data/challengers.md"); out.parent.mkdir(exist_ok=True); out.write_text(markdown(rows, last), encoding="utf-8")
    print(out.read_text(encoding="utf-8"))
