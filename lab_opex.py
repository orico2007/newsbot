"""Lab run 18 (2026-11-10, web idea): option-expiration-week / monthly-opex calendar effect (Quantpedia 'Option Expiration Week Effect'; Stoll-Whaley 1987 expiry-week studies). Tag LIVE-setup (breadth>=10%, peer rank, vol60>=1.75%) signals by position relative to the 3rd Friday of the month; backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

def third_fridays(dates):
    ys = {d[:7] for d in dates}; out = []
    for ym in ys:
        y, m = int(ym[:4]), int(ym[5:])
        d = datetime.date(y, m, 1)
        while d.weekday() != 4: d += datetime.timedelta(1)
        out.append((d + datetime.timedelta(14)).isoformat())
    return sorted(out)

def opex_pos(dates):
    """map trading day -> trading-day offset from the monthly opex day (third Friday, or the prior trading day if closed)."""
    idx = {d: i for i, d in enumerate(dates)}; pos = {}
    for tf in third_fridays(dates):
        j = max((i for i, d in enumerate(dates) if d <= tf), default=None)
        if j is None or tf > dates[-1]: continue
        for k in range(-6, 8):
            if 0 <= j + k < len(dates): pos[dates[j + k]] = k
    return pos

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    dates = [b["t"][:10] for b in spy]; pos = opex_pos(dates)
    champ = PT.gen(AS, ctx, challenger.ruleset()); B = breadth_series(AS); F = feats(AS)
    IX = {s: {d: i for i, d in enumerate(A["t"])} for s, A in AS.items()}
    live = []
    for t in champ:
        if B.get(t["t"][:10], (0, 0))[0] < .10: continue
        k = (t["sym"], t["t"])
        v = challenger.vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10]))
        if v is None or v < 1.75: continue
        live.append(dict(t, score=-F[k]["m3"] if k in F else t.get("score", 0)))
    print("data through", last, "n live+vol175 signals", len(live))
    row("LIVE (vol60>=1.75)", live, kw, cut)
    P = lambda t: pos.get(t["t"][:10])
    groups = [("opex week (-4..0 days to opex)", lambda t: P(t) is not None and -4 <= P(t) <= 0),
              ("week after opex (+1..+5)", lambda t: P(t) is not None and 1 <= P(t) <= 5),
              ("not opex week", lambda t: not (P(t) is not None and -4 <= P(t) <= 0)),
              ("opex day exactly (0)", lambda t: P(t) == 0),
              ("hold spans opex day (entry -7..-1)", lambda t: P(t) is not None and -6 <= P(t) <= -1),
              ("no pos info", lambda t: P(t) is None)]
    print("variants tried:", len(groups))
    for n, f in groups: row(n, [t for t in live if f(t)], kw, cut)
    # raw per-offset average trade return (unconstrained) for dose-response
    import collections
    agg = collections.defaultdict(list)
    for t in live:
        if P(t) is not None: agg[P(t)].append(t["pnl_pct"] if "pnl_pct" in t else t.get("ret", 0))
    for k in sorted(agg): print(k, len(agg[k]), round(sum(agg[k]) / len(agg[k]), 3))
