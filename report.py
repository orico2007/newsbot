"""דוח יומי: data/report.md + data/reports/YYYY-MM-DD.md - רווח/הפסד, עסקאות, חסימות, סקטורים."""
import csv, json, pathlib
from collections import Counter

def read_journal(path, day):
    p = pathlib.Path(path)
    if not p.exists(): return []
    with p.open(encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader(f) if (r.get("time") or "").startswith(day)]

def build(day, account, positions, rows, sectors=None, crypto_rows=None):
    eq, last = float(account["equity"]), float(account["last_equity"])
    pnl = eq - last
    ent = [r for r in rows if r["action"] == "ENTER"]
    ex = [r for r in rows if r["action"] == "EXIT"]
    tr = [r for r in rows if r["action"] == "TRAIL"]
    blocked = Counter((r["detail"].split(" conf=")[0])[:60] for r in rows if r["action"] == "blocked")
    errors = [r for r in rows if r["action"] == "error"]
    L = [f"# Daily report {day}", "", f"- Equity: ${eq:,.2f}  |  Day P&L: **{pnl:+,.2f} ({(pnl / last * 100) if last else 0:+.2f}%)**",
         f"- Entries: {len(ent)}  |  Exits: {len(ex)}  |  Trailing-stop raises: {len(tr)}  |  Blocked ideas: {sum(blocked.values())}  |  Errors: {len(errors)}", ""]
    if sectors:
        L += ["## Market", f"Regime: **{sectors.get('regime')}**. Leading: " + ", ".join(f"{r['etf']} ({r['score']})" for r in sectors.get("ranked", [])[:3]) +
              ". Lagging: " + ", ".join(f"{r['etf']} ({r['score']})" for r in sectors.get("ranked", [])[-3:]), ""]
    if positions:
        L += ["## Open positions", "| Symbol | Side | Qty | Unrealized P&L |", "|---|---|---|---|"]
        for p in positions:
            L.append(f"| {p['symbol']} | {p.get('side', '')} | {p.get('qty', '')} | {float(p.get('unrealized_pl', 0) or 0):+,.2f} |")
        L.append("")
    if ent:
        L += ["## Entries", "| Time (UTC) | Symbol | Strategy | Side | Why |", "|---|---|---|---|---|"]
        for r in ent: L.append(f"| {r['time'][11:16]} | {r['symbol']} | {r['strategy']} | {r['side']} | {r['headline'][:70]} {r['detail'][:60]} |")
        L.append("")
    if ex:
        L += ["## Exits"] + [f"- {r['time'][11:16]} {r['symbol']} ({r['strategy']}): {r['detail']}" for r in ex] + [""]
    if blocked:
        L += ["## Why ideas were blocked"] + [f"- {n}x {why}" for why, n in blocked.most_common(8)] + [""]
    if crypto_rows:
        ce = [r for r in crypto_rows if r["action"] == "ENTER"]; cx = [r for r in crypto_rows if r["action"] == "EXIT"]
        L += ["## Crypto", f"Entries: {len(ce)}, exits: {len(cx)}"] + [f"- {r['symbol']}: {r['detail']}" for r in cx] + [""]
    return "\n".join(L)

def write(day, account, positions, journal_path, crypto_journal_path, sectors_path, out_dir="data"):
    sec = None
    sp = pathlib.Path(sectors_path)
    if sp.exists():
        try: sec = json.loads(sp.read_text(encoding="utf-8"))
        except Exception: pass
    md = build(day, account, positions, read_journal(journal_path, day), sec, read_journal(crypto_journal_path, day))
    out = pathlib.Path(out_dir); (out / "reports").mkdir(parents=True, exist_ok=True)
    (out / "report.md").write_text(md, encoding="utf-8")
    (out / "reports" / f"{day}.md").write_text(md, encoding="utf-8")
    return md
