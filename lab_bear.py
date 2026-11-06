"""Lab run 11 (own idea): bear-regime sleeves (SPY<200d), when the champion is idle. Short-the-rip and strict long reversion. Backtest only."""
import datetime
import lab, sweep, challenger
import portfolio_test as PT
from sweep import sim, trend_ok, trigger, gate_ok
from lab_52wh import row

def sleeve(AS, ctx, side, trend, trig, gate, exit_, hold, stop, cool=3):
    out = []
    for sym, A in AS.items():
        n = len(A["c"]); cd = 0
        for i in range(205, n - 2):
            if i < cd: continue
            if not (trigger(A, i, side, trig) and trend_ok(A, i, side, trend) and gate_ok(ctx, A["t"][i], side, gate)): continue
            if not A["atr"][i] or A["atr"][i] / A["c"][i] > 0.06: continue
            r = sim(A, i, side, stop, exit_, hold); cd = i + cool
            if r:
                sc = (A["r2"][i] or 50) if side == "long" else 100 - (A["r2"][i] or 50)
                r.update(sym=sym, t_exit=r["te"], score=90 - sc, side=side, rule="bear"); out.append(r)
    return out

def bear_long(AS, ctx):
    """Champion-idle sleeve: SPY below its 200d, stock above own 200d, RSI2<5, exit close>prev high, hold 7, stop 4 ATR."""
    g = globals(); orig = g["gate_ok"]
    g["gate_ok"] = lambda c, d, s, k: not c["a200"].get(d, True)
    try: return sleeve(AS, ctx, "long", "s200", "r2_5", "x", "prevhl", 7, 4.0)
    finally: g["gate_ok"] = orig

if __name__ == "__main__":
    AS, ctx = sweep.load_all(); spy = lab.load_bars()["SPY"]; last = spy[-1]["t"][:10]
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=365)).isoformat()
    kw = challenger.DEF_PORT; PT.gate_ok = challenger.gate2
    champ = PT.gen(AS, ctx, challenger.ruleset()); row("CHAMPION", champ, kw, cut)
    V = [("short r2>95 s50<s200, SPY<200d, prevhl h5 stop3", "short", "s50_200", "r2_5", "spy200", "prevhl", 5, 3.0),
         ("short r2>90 below200, SPY<200d, ma5 h7 stop3", "short", "s200", "r2_10", "spy200", "ma5", 7, 3.0),
         ("short ibs>.9&below200 SPY<200d prevhl h5", "short", "s200", "ibs_0.1", "spy200", "prevhl", 5, 3.0),
         ("short r2>95 trend none, bear regime, prevhl h5", "short", "none", "r2_5", "bear", "prevhl", 5, 3.0),
         ("long r2<5 above200, SPY<200d, prevhl h7", "long", "s200", "r2_5", "none_bear", "prevhl", 7, 4.0),
         ("long r2<5 s50>s200, SPY<200d, prevhl h7", "long", "s50_200", "r2_5", "none_bear", "prevhl", 7, 4.0)]
    print("variants tried:", len(V))
    for name, side, tr, trig, g, ex, h, st in V:
        if g == "none_bear":
            orig = sweep.gate_ok
            sweep.gate_ok = lambda c, d, s, k: not c["a200"].get(d, True)
            globals()["gate_ok"] = sweep.gate_ok
            T = sleeve(AS, ctx, side, tr, trig, "x", ex, h, st); globals()["gate_ok"] = orig; sweep.gate_ok = orig
        else:
            T = sleeve(AS, ctx, side, tr, trig, g, ex, h, st)
        row(name, T, kw, cut); row("   + champion combined", champ + T, kw, cut)
