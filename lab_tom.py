"""Lab idea 2026-11-05: turn-of-month calendar effect (Quantpedia, Ariel/Lakonishok-Smidt) applied to champion entries and as a standalone sleeve. Backtest only."""
import datetime
import lab, research, sweep, challenger
import portfolio_test as PT
from lab_52wh import row

def tom_flags():
    spy = lab.load_bars()["SPY"]; d = [b["t"][:10] for b in spy]; f = {}
    for i, t in enumerate(d):
        m = t[:7]
        # trading-day index from month end / start
        j = i
        while j + 1 < len(d) and d[j+1][:7] == m: j += 1
        k = i
        while k - 1 >= 0 and d[k-1][:7] == m: k -= 1
        f[t] = (i - k + 1, j - i + 1)   # (day-of-month idx from start, days to month end incl.)
    return f

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); F = tom_flags()
    row("CHAMPION", champ, kw, cut)
    V = [("entries in TOM window (last2+first3)", lambda a: a[0] <= 3 or a[1] <= 2),
         ("entries NOT in TOM window", lambda a: not (a[0] <= 3 or a[1] <= 2)),
         ("entries first half of month (idx<=10)", lambda a: a[0] <= 10),
         ("entries second half (idx>10)", lambda a: a[0] > 10),
         ("entries last 5 + first 5 days", lambda a: a[0] <= 5 or a[1] <= 5)]
    print("variants tried:", len(V))
    for name, ok in V:
        T = [t for t in champ if t["t"][:10] in F and ok(F[t["t"][:10]])]
        row(name, T, kw, cut)
