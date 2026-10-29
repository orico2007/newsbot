import csv, json, os, re, sys, time, logging, pathlib, argparse
from datetime import datetime, timezone, date
from rules_loader import load_rules
from risk import evaluate

log = logging.getLogger("bot")
DATA = pathlib.Path("data"); DATA.mkdir(exist_ok=True)
STATE_FILE = DATA / "state.json"
JOURNAL = DATA / "journal.csv"

def load_state():
    s = json.loads(STATE_FILE.read_text(encoding="utf-8")) if STATE_FILE.exists() else {}
    if s.get("day") != str(date.today()):
        s = {"day": str(date.today()), "seen": s.get("seen", [])[-2000:], "trades_today": 0, "halted": False}
    return s

def save_state(s): STATE_FILE.write_text(json.dumps(s), encoding="utf-8")

def journal(row):
    new = not JOURNAL.exists()
    with JOURNAL.open("a", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        if new: w.writerow(["time", "symbol", "headline", "score", "direction", "reason", "action", "detail"])
        w.writerow(row)

def run_once(broker, brain, rules, state, now=None):
    now = now or datetime.now(timezone.utc)
    if rules["risk"]["market_hours_only"] and not broker.market_open():
        return   # שוק סגור: לא מבזבזים קריאות ל-Claude, והחדשות נשארות לא-נקראות
    max_age = rules["entry"]["max_news_age_minutes"]
    for n in broker.news(minutes=max_age + 5):
        if n.id in state["seen"]:
            continue
        state["seen"].append(n.id)
        age = (now - n.created_at).total_seconds() / 60
        if age > max_age or len(n.symbols) != 1:     # חדשות על מניה אחת בלבד, בלי רעש של רשימות
            continue
        sym = n.symbols[0]
        v = brain.rate(sym, n.headline, n.summary)
        if v.score < rules["entry"]["min_score"] or v.direction != rules["entry"]["direction"]:
            journal([now.isoformat(), sym, n.headline, v.score, v.direction, v.reason, "skip", "below threshold"])
            continue
        try:
            price, prev, adv = broker.snapshot(sym)
            d = evaluate(rules, v, price, prev, adv, broker.account(), broker.positions(), sym, state, broker.market_open())
        except Exception as e:
            log.warning("snapshot/eval failed for %s: %s", sym, e)
            journal([now.isoformat(), sym, n.headline, v.score, v.direction, v.reason, "error", str(e)])
            continue
        if not d.ok:
            journal([now.isoformat(), sym, n.headline, v.score, v.direction, v.reason, "blocked", d.reason])
            continue
        broker.buy_bracket(sym, d.qty, d.stop_price, d.take_profit_price)
        state["trades_today"] = state.get("trades_today", 0) + 1
        journal([now.isoformat(), sym, n.headline, v.score, v.direction, v.reason, "BUY",
                 f"qty={d.qty} stop={d.stop_price} tp={d.take_profit_price}"])
        log.info("BUY %s x%d stop %.2f tp %.2f | %s", sym, d.qty, d.stop_price, d.take_profit_price, n.headline)
    save_state(state)

def _ts(s):
    s = re.sub(r"(\.\d{6})\d+", r"\1", s)      # Alpaca שולח ננו-שניות
    return datetime.fromisoformat(s)

def session(broker, brain, rules, max_minutes=345, early_minutes=20, sleep=time.sleep):
    """סשן אחד (ל-GitHub Actions): מחכה לפתיחת השוק, רץ עד הסגירה או עד max_minutes, ואז יוצא."""
    t0, opened = time.monotonic(), False
    while True:
        c = broker.clock()
        if c["is_open"]:
            opened = True
        elif opened:
            log.info("market closed - session over"); return
        else:
            wait = (_ts(c["next_open"]) - _ts(c["timestamp"])).total_seconds() / 60
            if wait > early_minutes:
                log.info("market opens in %.0f min - nothing to do now", wait); return
        if (time.monotonic() - t0) / 60 > max_minutes:
            log.info("max session length reached - handing over"); return
        try:
            run_once(broker, brain, rules, load_state())
        except Exception as e:
            log.exception("loop error: %s", e)
        sleep(20 if c["is_open"] else 30)

def is_open_hint(broker):
    try: return broker.market_open()
    except Exception: return False

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--session", action="store_true"); args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    rules = load_rules()
    live = rules["mode"] == "live"
    if live and os.getenv("ALLOW_LIVE") != "1":
        sys.exit("live mode blocked: set ALLOW_LIVE=1 deliberately. Run on paper first.")
    from broker import AlpacaBroker
    from brain import Brain
    broker, brain = AlpacaBroker(paper=not live), Brain()
    log.info("started in %s mode", "LIVE" if live else "PAPER")
    if args.session:
        return session(broker, brain, rules)
    while True:
        state = load_state()
        try:
            run_once(broker, brain, rules, state)
        except Exception as e:
            log.exception("loop error: %s", e)
        time.sleep(20 if is_open_hint(broker) else 60)

if __name__ == "__main__":
    main()
