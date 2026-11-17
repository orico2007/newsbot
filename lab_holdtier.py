"""Lab run 24 (2026-11-17): hold period chosen per volatility tier (vol60) on the LIVE setup (follow-up listed in run 21).
Trades are generated at hold 5/7/10/15 and each signal takes the hold assigned to its vol60 tier. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from challenger import R, A, E, F, vol60
from lab_52wh import row
from lab_breadth import breadth_series
from lab_sector import feats
from lab_retune import live

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    B = breadth_series(AS); Fs = feats(AS); IX = {s: {d: i for i, d in enumerate(a["t"])} for s, a in AS.items()}
    TH = {}
    for h in (5, 7, 10, 15):
        TH[h] = {(t["sym"], t["t"]): t for t in live(AS, ctx, [R(**x, hold=h) for x in (A, E, F)], B, Fs, IX)}
    keys = list(TH[7])
    vol = {k: vol60(AS[k[0]], IX[k[0]].get(k[1][:10])) for k in keys}
    def pick(f):
        return [TH[f(vol[k])].get(k, TH[7][k]) for k in keys]
    V = [("LIVE hold 7", pick(lambda v: 7)), ("hold 5 all", [TH[5].get(k, TH[7][k]) for k in keys]),
         ("hold 10 all", [TH[10].get(k, TH[7][k]) for k in keys]),
         ("vol<2.5: 10, else 7", pick(lambda v: 10 if v < 2.5 else 7)),
         ("vol<2.5: 7, else 5", pick(lambda v: 7 if v < 2.5 else 5)),
         ("vol<2.5: 10, else 5", pick(lambda v: 10 if v < 2.5 else 5)),
         ("vol<2.5: 5, else 10", pick(lambda v: 5 if v < 2.5 else 10)),
         ("vol<2.5: 7, else 10", pick(lambda v: 7 if v < 2.5 else 10)),
         ("vol<2.5: 15, else 7", pick(lambda v: 15 if v < 2.5 else 7))]
    print("variants tried:", len(V), "data through", last, "signals", len(keys))
    for n, T in V: row(n, T, kw, cut)
