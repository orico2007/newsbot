"""מוריד היסטוריית נרות יומיים (כל העמודים) לקובץ אחד דחוס, כדי שאפשר יהיה לחקור מקומית בלי להריץ GitHub Actions בכל פעם."""
import gzip, json, sys, time, argparse
from datetime import datetime, timezone, timedelta
sys.path.insert(0, ".")
from broker import AlpacaBroker
import market
from rules_loader import load_rules

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--years", type=int, default=9); ap.add_argument("--out", default="bars_cache/bars.json.gz")
    a = ap.parse_args()
    b = AlpacaBroker(paper=True); rules = load_rules()
    syms = sorted(set(rules["swing"]["watchlist"]) | set(market.SECTOR_OF) | set(market.SECTORS) | {"SPY", "QQQ", "IWM", "DIA", "VIXY"})
    start = (datetime.now(timezone.utc) - timedelta(days=365 * a.years + 30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    out, fails = {}, []
    for k, s in enumerate(syms):
        for attempt in range(3):
            try:
                bs = b.bars(s, "1Day", start)
                out[s] = [[x["t"][:10], x["o"], x["h"], x["l"], x["c"], x["v"]] for x in bs]
                break
            except Exception as e:
                time.sleep(2 * (attempt + 1))
                if attempt == 2: fails.append(s); print("failed", s, e)
        if k % 20 == 0: print(k, "/", len(syms), s, len(out.get(s, [])), flush=True)
        time.sleep(0.3)
    import os; os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with gzip.open(a.out, "wt", encoding="utf-8") as f: json.dump(out, f, separators=(",", ":"))
    print("symbols", len(out), "failed", fails, "bars", sum(len(v) for v in out.values()), "size", os.path.getsize(a.out))

if __name__ == "__main__": main()
