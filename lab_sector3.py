"""Lab run 8: combine sector-weakness with strong-sector trend, and apply it to the gap-recover sleeve (follow-ups of run 7 / run 5). Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from lab_52wh import row
from lab_sector import feats
import lab_gap

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); F = feats(AS)
    g = lambda t: F.get((t["sym"], t["t"]))
    row("CHAMPION", champ, kw, cut)
    strict = [t for t in champ if g(t) and g(t)["m3"] < 0]
    row("strict: peers3d<0 (run7 ref)", strict, kw, cut)
    row("peers3d<0 & peers20d>0", [t for t in strict if g(t)["m20"] > 0], kw, cut)
    row("peers3d<0 & >=50% peers>SMA50", [t for t in strict if g(t)["ab"] >= 0.5], kw, cut)
    gap = lab_gap.trades(AS, lab_gap.signals(AS, ctx, "gap2_recover"), 7, "prevhl")
    gapf = [t for t in gap if g(t) and g(t)["m3"] < 0]
    row("gap<-2% recover alone", gap, kw, cut)
    row("gap<-2% recover & peers3d<0", gapf, kw, cut)
    row("champ strict + gap strict combined", strict + gapf, kw, cut)
    def rk(T):
        o = []
        for t in T:
            u = dict(t); u["score"] = -g(t)["m3"]; o.append(u)
        return o
    allt = [t for t in champ + gap if g(t)]
    row("champ + gap, rank weakest peers (no filter)", rk(allt), kw, cut)
    print("variants tried this script: 7")
