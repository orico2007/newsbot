import portfolio_test as P
from portfolio_test import *
if __name__ == "__main__":
    AS, ctx = load_all()
    A  = ("long", "s50_200", "r2_5&ibs_0.25", "spy200", "atrpct4", "prevhl", 7, 4.0, 90)
    A2 = ("long", "s50_200", "r2_5&ibs_0.25", "spy200", "none", "prevhl", 7, 4.0, 85)
    B  = ("long", "s200", "ext_2.5atr", "spy200", "none", "prevhl", 7, 4.0, 70)
    C  = ("long", "s200", "r2_5", "spy200", "none", "prevhl", 7, 4.0, 60)
    D  = ("long", "s50_200", "r2_10", "spy200", "none", "prevhl", 7, 4.0, 50)
    E  = ("long", "s50_200", "r2_10&ext_1.5atr", "spy200", "price15", "prevhl", 7, 4.0, 65)
    S1 = ("short", "s50_200", "dn5pct&ibs_0.25", "bear", "rvol_lo", "prevhl", 5, 4.0, 80)
    for name, rules in (("A", [A]), ("A+B", [A, B]), ("A+B+C", [A, B, C]), ("A+B+C+D", [A, B, C, D]), ("A+E", [A, E]), ("A+B+E", [A, B, E]), ("A+B+C+D+E", [A, B, C, D, E])):
        t = gen(AS, ctx, rules); P_ = lab.portfolio(t)
        ys = {}
        import research
        for y in sorted({x["t"][:4] for x in P_["trades"]}):
            s = research.stat([x for x in P_["trades"] if x["t"][:4] == y]); ys[y] = (s["n"], s["win"], s["pf_pct"])
        print(f"{name:12} n={P_['n']:4} win={P_['win']:5} PF={P_['pf_pct']} ret={P_['ret_pct']:5} mdd={P_['mdd']} | {ys}")
