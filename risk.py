"""Risk Gate: כל פקודה חייבת לעבור כאן לפני שהיא מגיעה לברוקר. הקוד מחליט, לא המודל."""
import math
from models import Decision

def evaluate_entry(rules, strategy, side, symbol, price, prev_close, adv, account, positions, state,
                   market_open, atr=None, shortable=True):
    a, n, s = rules["account"], rules["news"], rules[strategy]
    meta = state.get("meta", {})
    no = lambda why: Decision(False, why)
    if state.get("halted"): return no("halted for today")
    if not s["enabled"]: return no(f"{strategy} disabled")
    if a["market_hours_only"] and not market_open: return no("market closed")
    if side == "short" and not s["allow_short"]: return no("shorts disabled")
    if side == "short" and not shortable: return no("not shortable / hard to borrow")
    if price < n["min_price"]: return no(f"price {price} < {n['min_price']}")
    if adv < n["min_avg_daily_dollar_volume"]: return no("illiquid")
    if prev_close:
        move = (price / prev_close - 1) * 100
        if side == "long" and move > n["max_chase_pct"]: return no("already ran up (chasing)")
        if side == "short" and -move > n["max_chase_pct"]: return no("already dropped (chasing)")
    if symbol in {p["symbol"] for p in positions}: return no("already holding")
    if len(positions) >= a["max_open_positions_total"]: return no("max open positions")
    if sum(1 for p in positions if meta.get(p["symbol"], {}).get("strategy") == strategy) >= s["max_positions"]:
        return no(f"max {strategy} positions")
    if state.get("trades_today", 0) >= a["max_trades_per_day"]: return no("max trades today")
    equity, last_eq = float(account["equity"]), float(account["last_equity"])
    if last_eq > 0 and (equity / last_eq - 1) * 100 <= -a["max_daily_loss_pct"]:
        state["halted"] = True
        return no("daily loss limit hit")
    cfg = s[side]
    budget = min(equity * cfg["position_pct"] / 100, float(account["buying_power"]))
    gross = sum(abs(float(p.get("market_value", 0) or 0)) for p in positions)
    room = equity * a["max_gross_exposure_pct"] / 100 - gross
    budget = min(budget, room)
    qty = math.floor(budget / price)
    if qty < 1: return no("position too small / exposure cap")
    if strategy == "day":
        sd, td = price * cfg["stop_pct"] / 100, price * cfg["take_profit_pct"] / 100
    else:
        if not atr: return no("no ATR for swing sizing")
        sd = min(atr * cfg["atr_stop_mult"], price * cfg["max_stop_pct"] / 100)
        td = atr * cfg["atr_target_mult"]
    if sd < 0.01 or td < 0.01: return no("stop/target too tight")
    if side == "long":
        stop, take, order_side = price - sd, price + td, "buy"
    else:
        stop, take, order_side = price + sd, price - td, "sell"
    return Decision(True, "ok", qty, order_side, round(stop, 2), round(take, 2), "day" if strategy == "day" else "gtc")
