"""Lab run 10 (2026-11-09, web idea): MAX effect (Bali/Cakici/Whitelaw, NBER w14804) - max daily return over past 21d as a conditioner of the LIVE setup, alone and controlling for vol60. Backtest only."""
import datetime, math
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); bars = lab.load_bars(); spy = bars["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); B = breadth_series(AS); F = feats(AS)
    m3 = lambda t: F.get((t["sym"], t["t"]), {}).get("m3", 99)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    def feat(t):
        A = AS[t["sym"]]; i = IX[t["sym"]].get(t["t"][:10])
        if i is None or i < 70: return None
        r = [A["c"][j]/A["c"][j-1]-1 for j in range(i-59, i+1)]
        m = sum(r)/60; sd = math.sqrt(sum((x-m)**2 for x in r)/59)*100
        return dict(vol=sd, mx=max(r[-21:])*100, mx5=sorted(r[-21:])[-5:] and sum(sorted(r[-21:])[-5:])/5*100)
    live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] >= .10:
            u = dict(t); u["score"] = -m3(t); u["_f"] = feat(t); live.append(u)
    live = [t for t in live if t["_f"]]
    mxs = sorted(t["_f"]["mx"] for t in live); q = lambda p: mxs[int(p*(len(mxs)-1))]
    print("MAX terciles", round(q(1/3),2), round(q(2/3),2))
    row("LIVE ref", live, kw, cut); n = 1
    for lo, hi, nm in ((0, q(1/3), "MAX low tercile"), (q(1/3), q(2/3), "MAX mid"), (q(2/3), 99, "MAX high")):
        row(nm, [t for t in live if lo <= t["_f"]["mx"] < hi], kw, cut); n += 1
    for th in (3, 4, 5, 6, 8):
        row(f"MAX>={th}%", [t for t in live if t["_f"]["mx"] >= th], kw, cut); n += 1
    # control for vol: MAX inside each vol bucket
    for vn, vf in (("vol>=1.75", lambda t: t["_f"]["vol"] >= 1.75), ("vol<1.75", lambda t: t["_f"]["vol"] < 1.75)):
        for th in (4, 6):
            row(f"{vn} & MAX>={th}%", [t for t in live if vf(t) and t["_f"]["mx"] >= th], kw, cut)
            row(f"{vn} & MAX<{th}%", [t for t in live if vf(t) and t["_f"]["mx"] < th], kw, cut); n += 2
    row("vol>=1.75 (run 8 candidate)", [t for t in live if t["_f"]["vol"] >= 1.75], kw, cut)
    print("variants tried this run:", n)
