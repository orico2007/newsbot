"""מחקר אוטומטי: מה באמת עובד? (walk-forward, בלי להסתכל על העתיד)
שלבים: איסוף איתותים -> חלוקה לאימון/מבחן לפי תאריך -> סינון מאפיינים -> אימות תבניות לפי כיוון ומשטר -> כיוונון יציאות.
כלל הברזל: בוחרים על ה-train, ומודדים רק על ה-test שלא נראה. מה שלא עובד בשניהם לא נכנס.
פלט: data/research.md + validated.json + filters.json + exits.json (הבוט קורא אותם)."""
import json, argparse, pathlib, logging, itertools
from collections import defaultdict
from datetime import datetime, timezone, timedelta
import patterns, tools, features, backtest
from indicators import atr as _atr

log = logging.getLogger("research")
WARMUP, SLIP = 130, 0.05
DEFAULT_CFG = {"stop": "pattern", "stop_k": None, "target": "pattern", "target_k": None, "hold": 10, "scale": []}

# ------------------------------------------------------------------ איסוף
def collect(args):
    sym, bars = args
    recs = []
    for i in range(WARMUP, len(bars) - 2):
        try: sigs = patterns.detect_all(bars[:i + 1], None, {"rs": 0.0}, shorts=True)
        except Exception: continue
        if not sigs: continue
        f = features.compute(bars[:i + 1]); a = _atr(bars[:i + 1])
        for s in sigs:
            recs.append({"sym": sym, "i": i, "t": bars[i]["t"][:10], "p": s.name, "side": s.side, "stop": s.stop, "target": s.target,
                         "vol": bool(s.volume_ok), "tools": tools.count(s, bars[:i + 1])[0], "f": f, "atr": a})
    return sym, recs

# ------------------------------------------------------------------ סימולציית עסקה עם הגדרות יציאה
def run_trade(bars, rec, cfg):
    i, long, n = rec["i"], rec["side"] == "long", len(bars)
    entry = bars[i]["c"] * (1 + SLIP / 100 if long else 1 - SLIP / 100)
    if cfg["stop"] == "atr":
        if not rec.get("atr"): return None
        st = entry - cfg["stop_k"] * rec["atr"] if long else entry + cfg["stop_k"] * rec["atr"]
    else: st = rec["stop"]
    if (long and not st < entry) or (not long and not st > entry): return None
    risk = abs(entry - st)
    if not (0.002 <= risk / entry <= 0.12): return None
    if cfg["target"] == "r": tg = entry + cfg["target_k"] * risk if long else entry - cfg["target_k"] * risk
    elif cfg["target"] == "none": tg = None
    else:
        tg = rec["target"]
        if (long and not tg > entry) or (not long and not tg < entry): return None
    levels = [(entry + r * risk if long else entry - r * risk, pct / 100.0, r) for r, pct in cfg.get("scale", [])
              if tg is None or r * risk < 0.9 * abs(tg - entry)]
    done, legs, left, cur = 0, [], 1.0, st
    last = min(n, i + 1 + cfg["hold"]) - 1
    if last <= i: return None
    exit_j = last
    for j in range(i + 1, last + 1):
        b = bars[j]
        hit = None
        if long:
            if b["o"] <= cur: hit = b["o"]
            elif b["l"] <= cur: hit = cur
        else:
            if b["o"] >= cur: hit = b["o"]
            elif b["h"] >= cur: hit = cur
        if hit is not None:
            legs.append((left, hit)); left = 0; exit_j = j; break
        while done < len(levels) and (b["h"] >= levels[done][0] if long else b["l"] <= levels[done][0]):
            lv, frac, r = levels[done]; frac = min(frac, left)
            if left - frac < 0.05: break
            legs.append((frac, lv)); left -= frac; done += 1
            cur = max(cur, entry if done == 1 else levels[done - 2][0]) if long else min(cur, entry if done == 1 else levels[done - 2][0])
        if tg is not None and (b["h"] >= tg if long else b["l"] <= tg):
            legs.append((left, tg)); left = 0; exit_j = j; break
    if left > 0: legs.append((left, bars[last]["c"])); exit_j = last
    pnl = 0.0
    for frac, px in legs:
        px = px * (1 - SLIP / 100 if long else 1 + SLIP / 100)
        pnl += frac * ((px - entry) if long else (entry - px))
    return {"pattern": rec["p"], "side": rec["side"], "R": pnl / risk, "pnl_pct": pnl / entry * 100, "held": exit_j - i, "t": rec["t"], "sym": rec["sym"],
            "f": rec["f"], "tools": rec["tools"], "end": exit_j, "i": i}

def evaluate(recs, bars_by_sym, cfg, cooldown=3):
    """סימולציה לכל (תבנית, כיוון, סימבול) עם סמן פנוי - כמו ב-backtest העצמאי"""
    free, out = {}, []
    for rec in sorted(recs, key=lambda r: (r["sym"], r["p"], r["side"], r["i"])):
        k = (rec["sym"], rec["p"], rec["side"])
        if rec["i"] < free.get(k, 0): continue
        t = run_trade(bars_by_sym[rec["sym"]], rec, cfg)
        if not t: continue
        free[k] = t["end"] + cooldown
        for key in ("regime", "tier"):
            if key in rec: t[key] = rec[key]
        out.append(t)
    return out

# ------------------------------------------------------------------ סטטיסטיקה
def stat(ts):
    if not ts: return {"n": 0, "win": 0.0, "avgR": 0.0, "avg_pct": 0.0, "pf": None, "pf_pct": None}
    w = [t["R"] for t in ts if t["R"] > 0]; l = [-t["R"] for t in ts if t["R"] <= 0]
    wp = [t["pnl_pct"] for t in ts if t["pnl_pct"] > 0]; lp = [-t["pnl_pct"] for t in ts if t["pnl_pct"] <= 0]
    return {"n": len(ts), "win": round(100 * len(w) / len(ts), 1), "avgR": round(sum(t["R"] for t in ts) / len(ts), 3),
            "avg_pct": round(sum(t["pnl_pct"] for t in ts) / len(ts), 3),
            "pf": round(sum(w) / sum(l), 2) if l and sum(l) > 0 else None, "pf_pct": round(sum(wp) / sum(lp), 2) if lp and sum(lp) > 0 else None}

def split_cut(trades, frac=2 / 3):
    dates = sorted({t["t"] for t in trades})
    return dates[int(len(dates) * frac)] if dates else ""

# ------------------------------------------------------------------ שלב: סינון מאפיינים
def _apply(ts, rules): return [t for t in ts if features.passes(t["f"], rules)]

def search_filters(train, test, max_rules=3, keep_frac=0.35):
    """greedy: מוסיפים כלל רק אם הוא משפר את avgR גם ב-train וגם ב-test (שלא נראה)"""
    rules = []
    for _ in range(max_rules):
        base_tr, base_te = stat(_apply(train, rules)), stat(_apply(test, rules))
        cand = []
        cur = _apply(train, rules)
        for fn in features.NAMES:
            vals = sorted(t["f"][fn] for t in cur if t["f"].get(fn) is not None)
            if len(vals) < 200: continue
            for q in (0.15, 0.3, 0.5, 0.7, 0.85):
                v = vals[int(q * (len(vals) - 1))]
                for op in (">=", "<="):
                    r = {"f": fn, "op": op, "v": round(v, 3)}
                    sub = _apply(cur, [r])
                    if len(sub) < keep_frac * len(cur): continue
                    s = stat(sub)
                    cand.append((s["avgR"] - base_tr["avgR"], r))
        cand.sort(key=lambda x: -x[0])
        picked = None
        for gain, r in cand[:10]:
            if gain < 0.02: break
            te_sub = _apply(_apply(test, rules), [r]); s_te = stat(te_sub)
            if len(te_sub) >= 0.3 * max(1, base_te["n"]) and s_te["avgR"] - base_te["avgR"] >= 0.02 and s_te["avgR"] > 0:
                picked = (r, gain, s_te); break
        if not picked: break
        rules.append(picked[0])
    return rules

# ------------------------------------------------------------------ שלב: אימות תבניות
def validate(train, test, min_tr=20, min_te=8, pf_tr=1.15, pf_te=1.05):
    by = defaultdict(lambda: {"tr": [], "te": []})
    for t in train: by[(t["pattern"], t["side"])]["tr"].append(t)
    for t in test: by[(t["pattern"], t["side"])]["te"].append(t)
    out = {}
    for (p, side), d in by.items():
        a, b = stat(d["tr"]), stat(d["te"])
        if a["n"] < min_tr or b["n"] < min_te: continue
        if not ((a["pf"] or 0) >= pf_tr and a["avgR"] >= 0.05 and (b["pf"] or 0) >= pf_te and b["avgR"] > 0): continue
        regs = []
        for reg in ("bull", "bear", "neutral"):
            ts = [t for t in d["tr"] + d["te"] if t.get("regime") == reg]; s = stat(ts)
            if s["n"] >= 10 and (s["pf"] or 0) >= 1.0 and s["avgR"] > 0: regs.append(reg)
        pf = b["pf"] or 1.0
        out[f"{p}:{side}"] = {"train": a, "test": b, "regimes": regs or ["bull", "bear", "neutral"],
                              "mult": 1.25 if pf >= 1.5 else 1.0 if pf >= 1.2 else 0.75}
    return out

# ------------------------------------------------------------------ שלב: כיוון יציאות
def tune_exits(recs_tr, recs_te, bars_by_sym):
    """coordinate descent על הגדרות יציאה; הבחירה על train (ממוצע % לעסקה, כי הגודל קבוע באחוזים), דיווח על test"""
    space = {"stop": [("pattern", None), ("atr", 1.5), ("atr", 2.0), ("atr", 3.0)],
             "target": [("pattern", None), ("r", 1.5), ("r", 2.0), ("r", 3.0), ("none", None)],
             "hold": [5, 10, 15, 20],
             "scale": [[], [(1.0, 33), (2.0, 33)], [(1.0, 50)]]}
    def cfg_of(c): return {"stop": c["stop"][0], "stop_k": c["stop"][1], "target": c["target"][0], "target_k": c["target"][1], "hold": c["hold"], "scale": c["scale"]}
    cur = {"stop": space["stop"][0], "target": space["target"][0], "hold": 10, "scale": []}
    score = lambda c, recs: stat(evaluate(recs, bars_by_sym, cfg_of(c)))
    best = score(cur, recs_tr); table = [("baseline", stat(evaluate(recs_te, bars_by_sym, cfg_of(cur))))]
    for _ in range(2):
        for dim in ("stop", "target", "hold", "scale"):
            for v in space[dim]:
                c = dict(cur); c[dim] = v
                s = score(c, recs_tr)
                if s["n"] >= 0.7 * max(1, best["n"]) and s["avg_pct"] > best["avg_pct"] + 0.02 and (s["pf_pct"] or 0) >= (best["pf_pct"] or 0) * 0.98: best, cur = s, c
    final = cfg_of(cur)
    return final, best, stat(evaluate(recs_te, bars_by_sym, final)), table[0][1]

# ------------------------------------------------------------------ צינור מלא
def _cuts(trades):
    dates = sorted({t["t"] for t in trades})
    if not dates: return "", ""
    return dates[int(len(dates) * 0.5)], dates[int(len(dates) * 0.75)]

def pipeline(recs, bars_by_sym, spy=None, etf=None):
    """שלוש תקופות: A=אימון (בוחרים), B=אימות (מאשרים), C=holdout (נוגעים בו רק כדי למדוד - לעולם לא לבחור).
    בלי C כל מה שנבחר על נתונים 'שלא נראו' נראה טוב מדי (בחירה על אותו מבחן = רמאות עצמית)."""
    if spy and etf: backtest.annotate(recs, spy, etf)
    base_trades = evaluate(recs, bars_by_sym, DEFAULT_CFG)
    c1, c2 = _cuts(base_trades)
    A = [t for t in base_trades if t["t"] < c1]; B = [t for t in base_trades if c1 <= t["t"] < c2]; C = [t for t in base_trades if t["t"] >= c2]
    res = {"cut1": c1, "cut2": c2, "n_signals": len(recs), "baseline": {}, "filters": {}, "validated": {}, "exits": None}
    sides = ("long", "short")
    S = lambda ts, side=None: stat([t for t in ts if side is None or t["side"] == side])
    for side in sides: res["baseline"][side] = {"A": S(A, side), "B": S(B, side), "C": S(C, side)}
    for side in sides: res["filters"][side] = search_filters([t for t in A if t["side"] == side], [t for t in B if t["side"] == side])
    fl = lambda ts: [t for t in ts if features.passes(t["f"], res["filters"][t["side"]])]
    FA, FB, FC = fl(A), fl(B), fl(C)
    res["after_filters"] = {s: {"A": S(FA, s), "B": S(FB, s), "C": S(FC, s)} for s in sides}
    res["validated"] = validate(FA, FB)
    V = res["validated"]
    keep = lambda ts: [t for t in ts if f"{t['pattern']}:{t['side']}" in V and t.get("regime", "bull") in V[f"{t['pattern']}:{t['side']}"]["regimes"]]
    VA, VB, VC = keep(FA), keep(FB), keep(FC)
    res["after_validation"] = {"A": S(VA), "B": S(VB), "C": S(VC), "C_long": S(VC, "long"), "C_short": S(VC, "short")}
    vkeys = {(t["sym"], t["pattern"], t["side"], t["i"]) for t in VA + VB + VC}
    vrecs = [r for r in recs if (r["sym"], r["p"], r["side"], r["i"]) in vkeys]
    ra = [r for r in vrecs if r["t"] < c1]; rb = [r for r in vrecs if c1 <= r["t"] < c2]; rc = [r for r in vrecs if r["t"] >= c2]
    if len(ra) >= 30 and len(rb) >= 10:
        cfg, s_a, s_b, s_base_b = tune_exits(ra, rb, bars_by_sym)
        res["exits"] = {"cfg": cfg, "A": s_a, "B": s_b, "baseline_B": s_base_b, "C": stat(evaluate(rc, bars_by_sym, cfg)) if rc else stat([]),
                        "baseline_C": stat(evaluate(rc, bars_by_sym, DEFAULT_CFG)) if rc else stat([])}
    return res

# ------------------------------------------------------------------ פלט
def exits_json(res):
    """מאמצים יציאות חדשות רק אם הן משפרות על תקופת האימות B, ולא מזיקות ב-C (ה-holdout)"""
    e = res.get("exits")
    if not e or e["B"]["n"] < 10 or e["B"]["avg_pct"] <= e["baseline_B"]["avg_pct"]: return {}
    if e["C"]["n"] >= 10 and e["C"]["avg_pct"] < e["baseline_C"]["avg_pct"]: return {}
    c = e["cfg"]
    return {"stop_atr": c["stop_k"] if c["stop"] == "atr" else None, "target_r": c["target_k"] if c["target"] == "r" else None,
            "no_target": c["target"] == "none", "hold": c["hold"], "scale": c["scale"]}

def to_markdown(res, symbols, years):
    L = [f"# Research (walk-forward, 3 periods) - {years}y daily, {len(symbols)} symbols", "",
         f"Signals: {res['n_signals']}. **A** (before {res['cut1']}) = choose, **B** ({res['cut1']} to {res['cut2']}) = confirm, **C** (after {res['cut2']}) = holdout: never used for choosing, so it is the honest estimate. Past results do not guarantee future results.", ""]
    row = lambda name, s: f"| {name} | {s['n']} | {s['win']} | {s['avgR']} | {s['avg_pct']} | {s['pf']} |"
    hdr = ["| Set | Trades | Win % | Avg R | Avg % | Profit factor |", "|---|---|---|---|---|---|"]
    L += ["## Honest result: holdout period C (never used to choose anything)", ""] + hdr
    for side in ("long", "short"): L.append(row(f"baseline {side}s", res["baseline"][side]["C"]))
    for side in ("long", "short"): L.append(row(f"+ filters {side}s", res["after_filters"][side]["C"]))
    av = res["after_validation"]
    L += [row("**FINAL: filters + validated patterns**", av["C"]), row("FINAL longs", av["C_long"]), row("FINAL shorts", av["C_short"]), "",
          "## Same sets on earlier periods (selection bias makes A and B look better than reality)", ""] + hdr
    L += [row("FINAL on A (chosen on this)", av["A"]), row("FINAL on B (confirmation)", av["B"]), ""]
    L += ["## Feature filters chosen (improve A and confirmed on B)", ""]
    for side in ("long", "short"):
        L.append(f"- {side}: " + (", ".join(f"{r['f']} {r['op']} {r['v']}" for r in res["filters"][side]) or "none"))
    L += ["", f"## Validated patterns ({len(res['validated'])}) - good on A and confirmed on B", "",
          "| Pattern:side | A n | A PF | B n | B PF | B win % | B avg R | Regimes | Size x |", "|---|---|---|---|---|---|---|---|---|"]
    for k, v in sorted(res["validated"].items(), key=lambda kv: -(kv[1]["test"]["avgR"])):
        L.append(f"| {k} | {v['train']['n']} | {v['train']['pf']} | {v['test']['n']} | {v['test']['pf']} | {v['test']['win']} | {v['test']['avgR']} | {','.join(v['regimes'])} | {v['mult']} |")
    L += ["", "## Exit tuning", ""]
    e = res.get("exits")
    if e:
        c = e["cfg"]
        L += [f"Best on A: stop={c['stop']}{c['stop_k'] or ''}, target={c['target']}{c['target_k'] or ''}, hold={c['hold']}d, scale={c['scale'] or 'off'}",
              f"- avg % per trade: A {e['A']['avg_pct']} | B {e['B']['avg_pct']} vs default {e['baseline_B']['avg_pct']} | holdout C {e['C']['avg_pct']} vs default {e['baseline_C']['avg_pct']}",
              f"- adopted by the bot: {'yes' if exits_json(res) else 'no (did not beat the default exits on B and C)'}"]
    else: L.append("Not enough validated trades to tune exits.")
    return "\n".join(L)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--years", type=int, default=6); ap.add_argument("--symbols", default=""); ap.add_argument("--wide", action="store_true")
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    from rules_loader import load_rules
    from broker import AlpacaBroker
    import market
    rules = load_rules(); b = AlpacaBroker(paper=True)
    syms = [s for s in a.symbols.split(",") if s] or list(rules["swing"]["watchlist"])
    if a.wide: syms = sorted(set(syms) | set(market.SECTOR_OF))[:150]
    start = (datetime.now(timezone.utc) - timedelta(days=365 * a.years + 30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    bars_by, work = {}, []
    for s in syms:
        try:
            bs = b.bars(s, "1Day", start)
            if len(bs) >= 300: bars_by[s] = bs; work.append((s, bs))
        except Exception as e: log.warning("%s failed: %s", s, e)
    import multiprocessing as mp
    recs = []
    with mp.Pool(min(4, mp.cpu_count())) as pool:
        for s, r in pool.imap_unordered(collect, work): recs += r; log.info("%s: %d signals", s, len(r))
    spy = b.bars("SPY", "1Day", start); etf = {e: b.bars(e, "1Day", start) for e in market.SECTORS}
    res = pipeline(recs, bars_by, spy, etf)
    d = pathlib.Path("data"); d.mkdir(exist_ok=True)
    (d / "research.md").write_text(to_markdown(res, list(bars_by), a.years), encoding="utf-8")
    (d / "filters.json").write_text(json.dumps(res["filters"], indent=1), encoding="utf-8")
    (d / "validated.json").write_text(json.dumps({"updated": datetime.now(timezone.utc).isoformat(), "holdout_from": res["cut2"], "patterns": res["validated"]}, indent=1), encoding="utf-8")
    (d / "exits.json").write_text(json.dumps(exits_json(res), indent=1), encoding="utf-8")
    log.info("done: %d validated patterns", len(res["validated"]))

if __name__ == "__main__":
    main()
