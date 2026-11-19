"""Lab run 51 (2026-11-19): Monte Carlo month-block bootstrap of the vol60>=1.75% LIVE setup's portfolio trades (own idea: risk audit - distribution of
return / max drawdown / losing-year odds, plus a cost stress). Backtest only."""
import datetime, random
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def pctl(v, p): v = sorted(v); return v[min(len(v) - 1, int(p * len(v)))]

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    PT.gate_ok = challenger.gate2; kw = challenger.DEF_PORT
    B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    live = []
    for t in PT.gen(AS, ctx, challenger.ruleset()):
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            v = challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10]))
            if v is not None and v >= 1.75: live.append(dict(t, score=-F.get((t["sym"], t["t"]), {}).get("m3", 0)))
    P = row("LIVE ref", live, kw, cut); tt = P["trades"]; print("keys", sorted(tt[0]))
    size = 0.10
    months = {}
    for t in tt: months.setdefault(t.get("te", t["t"])[:7], []).append(t["pnl_pct"] * size)
    first, lastm = min(t["t"][:7] for t in tt), max(months)
    allm = []; y, m = int(first[:4]), int(first[5:])
    while f"{y}-{m:02d}" <= lastm: allm.append(f"{y}-{m:02d}"); m += 1; y, m = (y + 1, 1) if m == 13 else (y, m)
    ser = [months.get(k, []) for k in allm]; N = len(ser)
    print("months", N, "trades", len(tt), "empty months", sum(1 for s in ser if not s))
    def run(ser_, haircut=0.0):
        eq = 100.0; peak = 100.0; dd = 0.0; yr = []
        for s in ser_:
            for x in s: eq *= 1 + (x - haircut * size) / 100
            peak = max(peak, eq); dd = max(dd, (peak - eq) / peak * 100)
        return eq - 100, dd
    rnd = random.Random(11)
    for hc, name in [(0, "as backtested (0.05%/side slip)"), (0.2, "extra 0.2% round-trip cost per trade"), (0.5, "extra 0.5% round-trip cost per trade")]:
        R = []; D = []; L = 0; Y = 0
        for _ in range(5000):
            pick = [ser[rnd.randrange(N)] for _ in range(N)]
            r, d = run(pick, hc); R.append(r); D.append(d); L += r < 0
            # 12-month windows losing
            w = [run(pick[k:k + 12], hc)[0] for k in range(0, N - 11, 12)]; Y += any(x < 0 for x in w)
        print(f"{name:40} ret5/50/95 = {pctl(R,.05):.1f}/{pctl(R,.5):.1f}/{pctl(R,.95):.1f}  DD50/95/99 = {pctl(D,.5):.1f}/{pctl(D,.95):.1f}/{pctl(D,.99):.1f}  P(total<0) = {L/5000:.3f}  P(any losing 12m block) = {Y/5000:.3f}")
    # actual realised
    print("realised by calendar year (pct of equity, sum of pnl*size):", {y: round(sum(x for k, s in zip(allm, ser) if k[:4] == y for x in s), 1) for y in sorted({k[:4] for k in allm})})
    # trade-level iid bootstrap PF
    pn = [t["pnl_pct"] for t in tt]; PF = []
    for _ in range(5000):
        s = [pn[rnd.randrange(len(pn))] for _ in pn]; w = sum(x for x in s if x > 0); l = -sum(x for x in s if x < 0); PF.append(w / l)
    print(f"trade-level bootstrap PF 5/50/95 = {pctl(PF,.05):.2f}/{pctl(PF,.5):.2f}/{pctl(PF,.95):.2f}; P(PF<1.5)={sum(p<1.5 for p in PF)/5000:.3f} P(PF<1)={sum(p<1 for p in PF)/5000:.3f}")
