"""Backtest לתבניות הגרף על נתונים יומיים היסטוריים. כניסה סמוך לסגירת יום האיתות,
סטופ/יעד מהתבנית, סטופ קודם אם שניהם באותו נר (שמרני), יציאת זמן, עמלות/החלקה."""
import json, argparse, pathlib, logging
from collections import defaultdict
from datetime import datetime, timezone, timedelta
import patterns

log = logging.getLogger("backtest")

def simulate(bars, detectors=None, shorts=True, max_hold=10, warmup=130, cooldown=3, slip_pct=0.05, min_conf_quality=0.0, sym=None):
    trades, i, n = [], warmup, len(bars)
    while i < n - 2:
        sigs = [s for s in patterns.detect_all(bars[:i + 1], detectors, {"rs": 0.0}, shorts=shorts) if s.quality >= min_conf_quality]
        if not sigs: i += 1; continue
        sig = max(sigs, key=lambda s: s.quality)
        long = sig.side == "long"
        entry = bars[i]["c"] * (1 + slip_pct / 100 if long else 1 - slip_pct / 100)     # כניסה סמוך לסגירה (15 דקות לפני), כמו בבוט
        stop, target = sig.stop, sig.target
        if (long and not (stop < entry < target)) or (not long and not (target < entry < stop)):
            i += 1; continue
        risk = abs(entry - stop)
        if risk <= 0: i += 1; continue
        exit_px, reason, j = None, "time", i + 1
        for j in range(i + 1, min(n, i + 1 + max_hold)):
            b = bars[j]
            if long:
                if b["o"] <= stop: exit_px, reason = b["o"], "stop-gap"; break
                if b["l"] <= stop: exit_px, reason = stop, "stop"; break
                if b["h"] >= target: exit_px, reason = target, "target"; break
            else:
                if b["o"] >= stop: exit_px, reason = b["o"], "stop-gap"; break
                if b["h"] >= stop: exit_px, reason = stop, "stop"; break
                if b["l"] <= target: exit_px, reason = target, "target"; break
        if exit_px is None:
            exit_px = bars[j]["c"]
        exit_px = exit_px * (1 - slip_pct / 100 if long else 1 + slip_pct / 100)
        pnl = (exit_px - entry) if long else (entry - exit_px)
        trades.append({"pattern": sig.name, "side": sig.side, "R": pnl / risk, "pnl_pct": pnl / entry * 100,
                       "held": j - i, "reason": reason, "i": i, "t": bars[i].get("t", ""), "sym": sym})
        i = j + cooldown
    return trades

def stats(trades):
    by = defaultdict(list)
    for t in trades:
        by[t["pattern"]].append(t); by["ALL"].append(t)
    out = {}
    for k, ts in by.items():
        w = [t for t in ts if t["R"] > 0]; l = [t for t in ts if t["R"] <= 0]
        gp, gl = sum(t["pnl_pct"] for t in w), -sum(t["pnl_pct"] for t in l)
        out[k] = {"n": len(ts), "win_rate": round(len(w) / len(ts) * 100, 1), "avg_R": round(sum(t["R"] for t in ts) / len(ts), 3),
                  "avg_pnl_pct": round(sum(t["pnl_pct"] for t in ts) / len(ts), 3),
                  "profit_factor": round(gp / gl, 2) if gl > 0 else None, "avg_hold": round(sum(t["held"] for t in ts) / len(ts), 1),
                  "long_n": sum(1 for t in ts if t["side"] == "long"), "short_n": sum(1 for t in ts if t["side"] == "short")}
    for side in ("long", "short"):
        ts = [t for t in allt_sides(trades) if t["side"] == side]
        if ts: out[f"ALL_{side}"] = _one(ts)
    ps = defaultdict(list)
    for t in trades: ps[(t["pattern"], t["side"])].append(t)
    for (p, side), ts in ps.items(): out[f"SIDE|{p}|{side}"] = _one(ts)      # per pattern AND direction
    return out

def annotate(trades, spy, etf_bars):
    """מוסיף לכל עסקה את משטר השוק (SPY) ודירוג הסקטור של אותו יום - כפי שהבוט רואה אותם"""
    import market
    cache = {}
    def at(day):
        if day not in cache:
            sl = [x for x in spy if x["t"][:10] <= day]
            ranked = market.rank_sectors({e: [x for x in bs if x["t"][:10] <= day] for e, bs in etf_bars.items()}, sl) if len(sl) >= 60 else []
            cache[day] = (market.regime(sl) if sl else "neutral", [r["etf"] for r in ranked])
        return cache[day]
    for t in trades:
        reg, order = at(t["t"][:10]); sec = market.SECTOR_OF.get(t["sym"]); n = 3
        t["regime"] = reg
        t["tier"] = "top" if sec in order[:n] else "bottom" if sec in order[-n:] and order else "mid"
    return trades

def aligned(t):
    """האם העסקה עוברת את מסנני השוק/סקטור של הבוט (veto_against)"""
    reg, tier, side = t.get("regime", "neutral"), t.get("tier", "mid"), t["side"]
    if side == "long": return not (tier == "bottom" or (reg == "bear" and tier != "top"))
    return not (tier == "top" or (reg == "bull" and tier != "bottom"))

def allt_sides(trades): return trades

def _one(ts):
    w = [t for t in ts if t["R"] > 0]; l = [t for t in ts if t["R"] <= 0]
    gp, gl = sum(t["pnl_pct"] for t in w), -sum(t["pnl_pct"] for t in l)
    return {"n": len(ts), "win_rate": round(len(w) / len(ts) * 100, 1), "avg_R": round(sum(t["R"] for t in ts) / len(ts), 3),
            "avg_pnl_pct": round(sum(t["pnl_pct"] for t in ts) / len(ts), 3), "profit_factor": round(gp / gl, 2) if gl > 0 else None,
            "avg_hold": round(sum(t["held"] for t in ts) / len(ts), 1), "long_n": sum(1 for t in ts if t["side"] == "long"), "short_n": sum(1 for t in ts if t["side"] == "short")}

def _bad(v, min_n, max_avg_r, min_pf):
    return v["n"] >= min_n and (v["avg_R"] <= max_avg_r or (v["profit_factor"] is not None and v["profit_factor"] < min_pf))

def _bad_sides(st, min_n=15, max_avg_r=-0.05, min_pf=0.85):
    bad = {}
    for k, v in st.items():
        if k.startswith("SIDE|"):
            _, p, side = k.split("|")
            if _bad(v, min_n, max_avg_r, min_pf): bad.setdefault(p, set()).add(side)
    return bad

def disabled_from(st, min_n=30, max_avg_r=-0.05, min_pf=0.85):
    """גלאי כבוי כולו רק אם כל הכיוונים שלו מפסידים; אם רק כיוון אחד מפסיד - כבוי רק הכיוון (disabled_sides)"""
    bad = _bad_sides(st)
    out = set()
    for k, v in st.items():
        if k.startswith(("ALL", "SIDE|", "ALIGNED")): continue
        sides = {s for s, n in (("long", v["long_n"]), ("short", v["short_n"])) if n}
        if v["n"] >= min_n and _bad(v, min_n, max_avg_r, min_pf) and (not bad or (sides and sides <= bad.get(k, set()))): out.add(k)
    return sorted(out)

def disabled_sides_from(st, min_n=15, max_avg_r=-0.05, min_pf=0.85):
    """pattern:side - כיוון ספציפי שמפסיד, גם אם הגלאי כולו לא כבוי"""
    whole = set(disabled_from(st))
    return sorted(f"{p}:{s}" for p, ss in _bad_sides(st).items() if p not in whole for s in ss)

def to_markdown(st, symbols, years, disabled):
    rows = sorted(((k, v) for k, v in st.items() if not k.startswith(("ALL", "SIDE|", "ALIGNED"))), key=lambda kv: -kv[1]["avg_R"])
    md = [f"# Backtest - {years}y daily, {len(symbols)} symbols", "",
          "Entry near the signal day's close (bot buys 15 min before close), stop first on conflict, 0.05% slippage each side, 10-day time stop. Past results do not guarantee future results.", "",
          "| Pattern | Trades | Win % | Avg R | Avg % | Profit factor | Avg hold (d) | Long/Short |", "|---|---|---|---|---|---|---|---|"]
    for k, v in [("ALL", st.get("ALL")), ("ALIGNED with market+sector", st.get("ALIGNED")), ("ALIGNED longs", st.get("ALIGNED_long")), ("ALIGNED shorts", st.get("ALIGNED_short")), ("ALL longs", st.get("ALL_long")), ("ALL shorts", st.get("ALL_short"))] + rows:
        if v: md.append(f"| {k} | {v['n']} | {v['win_rate']} | {v['avg_R']} | {v['avg_pnl_pct']} | {v['profit_factor']} | {v['avg_hold']} | {v['long_n']}/{v['short_n']} |")
    md += ["", f"Auto-disabled directions (n>=15): {', '.join(disabled_sides_from(st)) or 'none'}"]
    md += ["", f"Auto-disabled (n>=30 and avg R <= -0.05 or profit factor < 0.85): {', '.join(disabled) or 'none'}"]
    return "\n".join(md)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--years", type=int, default=3)
    ap.add_argument("--symbols", default=""); ap.add_argument("--no-shorts", action="store_true")
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    from rules_loader import load_rules
    from broker import AlpacaBroker
    rules = load_rules()
    syms = [s for s in a.symbols.split(",") if s] or rules["swing"]["watchlist"]
    b = AlpacaBroker(paper=True)
    start = (datetime.now(timezone.utc) - timedelta(days=365 * a.years + 30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    allt = []
    for s in syms:
        try:
            bars = b.bars(s, "1Day", start)
            if len(bars) < 200: continue
            t = simulate(bars, shorts=not a.no_shorts, sym=s); allt += t
            log.info("%s: %d trades", s, len(t))
        except Exception as e:
            log.warning("%s failed: %s", s, e)
    try:
        spy = b.bars("SPY", "1Day", start)
        import market
        etf = {e: b.bars(e, "1Day", start) for e in market.SECTORS}
        annotate(allt, spy, etf)
        al = [t for t in allt if aligned(t)]
        log.info("market/sector-aligned: %d of %d trades", len(al), len(allt))
    except Exception as e:
        log.warning("alignment skipped: %s", e); al = []
    st = stats(allt) if allt else {}
    if al:
        sa = stats(al)
        for k in ("ALL", "ALL_long", "ALL_short"):
            if k in sa: st["ALIGNED_" + k[4:] if k != "ALL" else "ALIGNED"] = sa[k]
    dis = disabled_from(st)
    d = pathlib.Path("data"); d.mkdir(exist_ok=True)
    (d / "backtest.json").write_text(json.dumps({"updated": datetime.now(timezone.utc).isoformat(), "stats": st, "disabled": dis, "disabled_sides": disabled_sides_from(st)}, indent=1), encoding="utf-8")
    (d / "backtest.md").write_text(to_markdown(st, syms, a.years, dis), encoding="utf-8")
    log.info("done: %d trades, disabled=%s", len(allt), dis)

if __name__ == "__main__":
    main()
