import lab, research, sweep
import portfolio_test as PT
AS, ctx = sweep.load_all()
gate = "bullreg"
orig = sweep.gate_ok
def g2(c, d, side, kind):
    return c["reg"].get(d) == "bull" if kind == "bullreg" else orig(c, d, side, kind)
PT.gate_ok = g2
A = ("long", "s50_200", "r2_5&ibs_0.25", gate, "atrpct4", "prevhl", 7, 4.0, 90)
E = ("long", "s50_200", "r2_10&ext_1.5atr", gate, "price15", "prevhl", 7, 4.0, 65)
F = ("long", "s50_200", "r2_5", gate, "nocrash", "prevhl", 7, 4.0, 60)   # extra frequency
G = ("long", "s50_200", "down3_r2_20", gate, "nocrash", "prevhl", 7, 4.0, 55)
def row(name, rules, **kw):
    P = lab.portfolio(PT.gen(AS, ctx, rules), **kw)
    ys = {y: research.stat([x for x in P["trades"] if x["t"][:4] == y])["pf_pct"] for y in sorted({x["t"][:4] for x in P["trades"]})}
    print(f"{name:28} n={P['n']:4} win={P['win']:5} PF={P['pf_pct']:5} ret={P['ret_pct']:6} mdd={P['mdd']:5} sharpe={P['sharpe']} | {ys}")
row("A+E base 8%x8", [A, E])
for sp, mp, pd in [(10,10,3),(12,8,3),(15,6,3),(12,10,4),(20,5,3)]:
    row(f"A+E size{sp} pos{mp} day{pd}", [A, E], size_pct=sp, max_pos=mp, per_day=pd)
row("A+E+F size10", [A, E, F], size_pct=10, max_pos=10, per_day=3)
row("A+E+F+G size10", [A, E, F, G], size_pct=10, max_pos=10, per_day=3)
print("---")
row("A+E+F size12 pos10 day4", [A, E, F], size_pct=12, max_pos=10, per_day=4)
row("A+E+F size10 pos12 day4", [A, E, F], size_pct=10, max_pos=12, per_day=4)
row("A+E+F size8 pos10 day3", [A, E, F], size_pct=8, max_pos=10, per_day=3)
