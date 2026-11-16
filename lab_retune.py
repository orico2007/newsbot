"""Lab run 21 (2026-11-16): re-tune hold / stop / trigger breadth under the NEW live base (breadth>=10%, peer rank, vol60>=1.75%).
Those parameters were tuned before the vol filter existed. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from challenger import R, A, E, F, G, vol60
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats

H = dict(trig="r2_10", extra="nocrash", score=50)

def live(AS, ctx, rules, B, Fs, IX, volmin=1.75):
    T0 = PT.gen(AS, ctx, rules); out = []
    for t in T0:
        if B.get(t["t"][:10], (0, 0))[0] < 0.10: continue
        v = vol60(AS[t["sym"]], IX[t["sym"]].get(t["t"][:10]))
        if v is None or v < volmin: continue
        out.append(dict(t, score=-Fs[(t["sym"], t["t"])]["m3"]) if (t["sym"], t["t"]) in Fs else t)
    return out

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    B = breadth_series(AS); Fs = feats(AS); IX = {s: {d: i for i, d in enumerate(a["t"])} for s, a in AS.items()}
    base = lambda **k: [R(**x, **k) for x in (A, E, F)]
    V = [("LIVE (vol175)", base(), {}),
         ("hold 5", base(hold=5), {}), ("hold 10", base(hold=10), {}), ("hold 15", base(hold=15), {}),
         ("stop 3 ATR", base(stop=3.0), {}), ("stop 6 ATR", base(stop=6.0), {}),
         ("exit ma5", base(exit_="ma5", hold=7), {}),
         ("+ rule G (3 down days)", base() + [R(**G)], {}),
         ("+ rule H (rsi2<10 nocrash)", base() + [R(**H)], {}),
         ("gate none", base(gate="none"), {}),
         ("vol>=1.5 + rule H", base() + [R(**H)], dict(volmin=1.5)),
         ("vol>=2.0", base(), dict(volmin=2.0)),
         ]
    print("variants tried:", len(V), "data through", last)
    for name, rules, k in V:
        T = live(AS, ctx, rules, B, Fs, IX, **k); row(name, T, kw, cut)
        if name.startswith("LIVE"): row("   LIVE 12% x 10", T, dict(size_pct=12, max_pos=10, per_day=4), cut)
