"""Backtest לתבניות הגרף על נתונים יומיים היסטוריים. כניסה בפתיחת היום שאחרי האיתות,
סטופ/יעד מהתבנית, סטופ קודם אם שניהם באותו נר (שמרני), יציאת זמן, עמלות/החלקה."""
import json, argparse, pathlib, logging
from collections import defaultdict
from datetime import datetime, timezone, timedelta
import patterns

log = logging.getLogger("backtest")

def simulate(bars, detectors=None, shorts=True, max_hold=10, warmup=130, cooldown=3, slip_pct=0.05, min_conf_quality=0.0):
    trades, i, n = [], warmup, len(bars)
    while i < n - 2:
        sigs = [s for s in patterns.detect_all(bars[:i + 1], detectors, {"rs": 0.0}, shorts=shorts) if s.quality >= min_conf_quality]
        if not sigs: i += 1; continue
        sig = max(sigs, key=lambda s: s.quality)
        entry_bar = bars[i + 1]
        long = sig.side == "long"
        entry = entry_bar["o"] * (1 + slip_pct / 100 if long else 1 - slip_pct / 100)
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
                       "held": j - i, "reason": reason, "i": i})
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
    return out

def disabled_from(st, min_n=30, max_avg_r=-0.1):
    """גלאים עם מספיק עסקאות ותוחלת שלילית ברורה - מכבים אוטומטית"""
    return sorted(k for k, v in st.items() if k != "ALL" and v["n"] >= min_n and v["avg_R"] <= max_avg_r)

def to_markdown(st, symbols, years, disabled):
    rows = sorted(((k, v) for k, v in st.items() if k != "ALL"), key=lambda kv: -kv[1]["avg_R"])
    md = [f"# Backtest - {years}y daily, {len(symbols)} symbols", "",
          "Entry at next open, stop first on conflict, 0.05% slippage each side, 10-day time stop. Past results do not guarantee future results.", "",
          "| Pattern | Trades | Win % | Avg R | Avg % | Profit factor | Avg hold (d) | Long/Short |", "|---|---|---|---|---|---|---|---|"]
    for k, v in [("ALL", st.get("ALL"))] + rows:
        if v: md.append(f"| {k} | {v['n']} | {v['win_rate']} | {v['avg_R']} | {v['avg_pnl_pct']} | {v['profit_factor']} | {v['avg_hold']} | {v['long_n']}/{v['short_n']} |")
    md += ["", f"Auto-disabled (n>=30, avg R <= -0.1): {', '.join(disabled) or 'none'}"]
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
            t = simulate(bars, shorts=not a.no_shorts); allt += t
            log.info("%s: %d trades", s, len(t))
        except Exception as e:
            log.warning("%s failed: %s", s, e)
    st = stats(allt) if allt else {}
    dis = disabled_from(st)
    d = pathlib.Path("data"); d.mkdir(exist_ok=True)
    (d / "backtest.json").write_text(json.dumps({"updated": datetime.now(timezone.utc).isoformat(), "stats": st, "disabled": dis}, indent=1), encoding="utf-8")
    (d / "backtest.md").write_text(to_markdown(st, syms, a.years, dis), encoding="utf-8")
    log.info("done: %d trades, disabled=%s", len(allt), dis)

if __name__ == "__main__":
    main()
