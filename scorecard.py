"""כרטיס ציונים של מסחר אמיתי (נייר): data/trades.csv -> data/scorecard.md + data/scorecard.json (כיבוי אסטרטגיות מפסידות)."""
import csv, json, pathlib
from collections import defaultdict

TRADE_COLS = ["closed", "symbol", "strategy", "pattern", "side", "entry", "exit", "pnl_pct", "R", "held_days", "entry_slip_pct", "reason"]

def append_trade(path, row):
    p = pathlib.Path(path); new = not p.exists()
    with p.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, TRADE_COLS)
        if new: w.writeheader()
        w.writerow({k: row.get(k, "") for k in TRADE_COLS})

def read_trades(path):
    p = pathlib.Path(path)
    if not p.exists(): return []
    with p.open(encoding="utf-8", newline="") as f:
        out = []
        for r in csv.DictReader(f):
            try: r["pnl_pct"] = float(r["pnl_pct"]); r["R"] = float(r["R"]) if r["R"] != "" else None
            except ValueError: continue
            r["entry_slip_pct"] = float(r["entry_slip_pct"]) if r.get("entry_slip_pct") not in ("", None) else None
            out.append(r)
        return out

def _agg(ts):
    w = [t for t in ts if t["pnl_pct"] > 0]; l = [t for t in ts if t["pnl_pct"] <= 0]
    gp, gl = sum(t["pnl_pct"] for t in w), -sum(t["pnl_pct"] for t in l)
    sl = [t["entry_slip_pct"] for t in ts if t["entry_slip_pct"] is not None]
    rs = [t["R"] for t in ts if t["R"] is not None]
    return {"n": len(ts), "win_rate": round(len(w) / len(ts) * 100, 1), "avg_pnl_pct": round(sum(t["pnl_pct"] for t in ts) / len(ts), 3),
            "avg_win": round(gp / len(w), 2) if w else 0, "avg_loss": round(-gl / len(l), 2) if l else 0,
            "profit_factor": round(gp / gl, 2) if gl > 0 else None, "avg_R": round(sum(rs) / len(rs), 2) if rs else None,
            "avg_slippage_pct": round(sum(sl) / len(sl), 3) if sl else None}

def compute(trades):
    out = {"ALL": _agg(trades)} if trades else {}
    by_s, by_p = defaultdict(list), defaultdict(list)
    for t in trades: by_s[t["strategy"]].append(t); by_p[t["pattern"]].append(t)
    out["strategy"] = {k: _agg(v) for k, v in by_s.items()}
    out["pattern"] = {k: _agg(v) for k, v in by_p.items() if k}
    return out

def losers(st, min_n=15, max_avg=-0.5):
    """דפוסים עם מספיק עסקאות אמיתיות ותוחלת שלילית ברורה"""
    return sorted(k for k, v in st.get("pattern", {}).items() if v["n"] >= min_n and v["avg_pnl_pct"] <= max_avg and k not in ("news", "scan"))

def markdown(st, bad):
    if not st: return "# Scorecard\n\nNo closed trades yet."
    def row(k, v): return f"| {k} | {v['n']} | {v['win_rate']} | {v['avg_pnl_pct']} | {v['avg_win']} / {v['avg_loss']} | {v['profit_factor']} | {v['avg_R']} | {v['avg_slippage_pct']} |"
    head = "| | Trades | Win % | Avg P&L % | Avg win / loss % | Profit factor | Avg R | Entry slippage % |\n|---|---|---|---|---|---|---|---|"
    L = ["# Scorecard (paper trades)", "", head, row("ALL", st["ALL"])]
    L += ["", "## By strategy", head] + [row(k, v) for k, v in sorted(st["strategy"].items())]
    L += ["", "## By pattern / signal", head] + [row(k, v) for k, v in sorted(st["pattern"].items(), key=lambda kv: -kv[1]["avg_pnl_pct"])]
    L += ["", f"Auto-disabled (n>=15, avg P&L <= -0.5%): {', '.join(bad) or 'none'}"]
    return "\n".join(L)

def write(trades_path, out_dir="data"):
    st = compute(read_trades(trades_path)); bad = losers(st)
    d = pathlib.Path(out_dir)
    (d / "scorecard.md").write_text(markdown(st, bad), encoding="utf-8")
    (d / "scorecard.json").write_text(json.dumps({"stats": st, "disabled": bad}, indent=1), encoding="utf-8")
    return st, bad
