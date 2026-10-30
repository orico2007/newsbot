"""מעבדת מחקר מקומית: טוענת את מטמון הנרות, אוספת איתותים (עם cache), מריצה סימולציית תיק עם מגבלת פוזיציות, ומאמתת walk-forward שנתי."""
import gzip, json, pickle, sys, os, time, pathlib, statistics
from collections import defaultdict
import patterns, tools, features, research, backtest, market
from indicators import atr as _atr, sma

CACHE = pathlib.Path(os.environ.get("LAB_DIR", "/tmp/lab")); CACHE.mkdir(parents=True, exist_ok=True)

def load_bars(path="bars_cache/bars.json.gz"):
    d = json.load(gzip.open(path, "rt", encoding="utf-8"))
    return {s: [{"t": r[0], "o": r[1], "h": r[2], "l": r[3], "c": r[4], "v": r[5]} for r in rows] for s, rows in d.items()}

def collect_cached(bars_by, universe, name="recs", procs=2):
    """איסוף איתותים לכל הסימבולים, נשמר לדיסק (הדבר היקר). אם כבר קיים - טוען"""
    f = CACHE / f"{name}.pkl"
    if f.exists(): return pickle.load(open(f, "rb"))
    import multiprocessing as mp
    work = [(s, bars_by[s]) for s in universe if len(bars_by.get(s, [])) >= 300]
    recs = []
    with mp.Pool(procs) as pool:
        for k, (s, r) in enumerate(pool.imap_unordered(research.collect, work)):
            recs += r
            if k % 10 == 0: print(f"collect {k}/{len(work)} {s} total {len(recs)}", flush=True)
    pickle.dump(recs, open(f, "wb"))
    return recs

def spy_regime_series(spy):
    """לכל תאריך: bull/bear/neutral לפי הכלל של הבוט (market.regime) - נחשב פעם אחת עם חלון נע"""
    out = {}
    for i in range(60, len(spy)):
        out[spy[i]["t"][:10]] = market.regime(spy[max(0, i - 260):i + 1])
    return out

def sma_flags(spy, n):
    c = [b["c"] for b in spy]; out = {}
    for i in range(n, len(spy)): out[spy[i]["t"][:10]] = c[i] > sum(c[i - n + 1:i + 1]) / n
    return out

# ------------------------------------------------------------------ תיק (כמו הבוט: סלוטים, פוזיציות מוגבלות)
def portfolio(trades, max_pos=8, per_day=2, size_pct=8.0, sector_cap=2, start_equity=100.0):
    """trades: עסקאות פוטנציאליות (כל אחת עם t=תאריך כניסה, end=אינדקס יציאה, held, score).
    מדמה: בכל יום לוקחים את הטובות ביותר (לפי score) עד per_day ועד max_pos פתוחות. מחזיר סטטיסטיקות תיק."""
    by_day = defaultdict(list)
    for t in trades: by_day[t["t"]].append(t)
    days = sorted(by_day); open_pos, taken, curve, eq = [], [], [], start_equity
    # יציאות מעובדות לפי תאריך יציאה (t_exit); נסמן כל עסקה בתאריך יציאה
    for d in days:
        open_pos = [p for p in open_pos if p["t_exit"] > d]
        slots = max_pos - len(open_pos)
        if slots <= 0: continue
        held_syms = {p["sym"] for p in open_pos}; secs = defaultdict(int)
        for p in open_pos: secs[market.SECTOR_OF.get(p["sym"])] += 1
        n = 0
        for t in sorted(by_day[d], key=lambda x: -x.get("score", 0)):
            if n >= per_day or n >= slots: break
            if t["sym"] in held_syms: continue
            sec = market.SECTOR_OF.get(t["sym"])
            if sec and sector_cap and secs[sec] >= sector_cap: continue
            open_pos.append(t); taken.append(t); held_syms.add(t["sym"]); secs[sec] += 1; n += 1
    # equity לפי תאריך יציאה
    taken.sort(key=lambda t: t["t_exit"])
    peak, mdd = eq, 0.0
    monthly = defaultdict(float)
    for t in taken:
        eq *= 1 + size_pct / 100 * t["pnl_pct"] / 100
        peak = max(peak, eq); mdd = max(mdd, (peak - eq) / peak * 100)
        monthly[t["t_exit"][:7]] += size_pct * t["pnl_pct"] / 100
    s = research.stat(taken)
    ms = list(monthly.values())
    sharpe = (statistics.mean(ms) / statistics.pstdev(ms) * (12 ** 0.5)) if len(ms) > 3 and statistics.pstdev(ms) > 0 else 0
    yrs = max(1e-9, (len(days) / 252)) if days else 1
    return {"n": s["n"], "win": s["win"], "pf": s["pf"], "pf_pct": s["pf_pct"], "avg_pct": s["avg_pct"], "avgR": s["avgR"], "alpha": s["alpha"],
            "ret_pct": round(eq - start_equity, 1), "mdd": round(mdd, 1), "sharpe": round(sharpe, 2), "trades": taken}
