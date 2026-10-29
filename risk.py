"""Risk Gate: כל פקודה חייבת לעבור כאן לפני שהיא מגיעה לברוקר. הקוד מחליט, לא המודל."""
import math
from models import Decision

def evaluate(rules, verdict, price, prev_close, avg_dollar_vol, account, positions, symbol, state, market_open):
    e, r = rules["entry"], rules["risk"]
    if state.get("halted"):
        return Decision(False, "halted for today")
    if r["market_hours_only"] and not market_open:
        return Decision(False, "market closed")
    if verdict.direction != e["direction"]:
        return Decision(False, f"direction {verdict.direction}")
    if verdict.score < e["min_score"]:
        return Decision(False, f"score {verdict.score} < {e['min_score']}")
    if price < e["min_price"]:
        return Decision(False, f"price {price} < {e['min_price']}")
    if avg_dollar_vol < e["min_avg_daily_dollar_volume"]:
        return Decision(False, "illiquid")
    if prev_close and (price / prev_close - 1) * 100 > e["max_chase_pct"]:
        return Decision(False, "already ran (chasing)")
    if symbol in {p["symbol"] for p in positions}:
        return Decision(False, "already holding")
    if len(positions) >= r["max_open_positions"]:
        return Decision(False, "max open positions")
    if state.get("trades_today", 0) >= r["max_trades_per_day"]:
        return Decision(False, "max trades today")
    equity, last_eq = float(account["equity"]), float(account["last_equity"])
    if last_eq > 0 and (equity / last_eq - 1) * 100 <= -r["max_daily_loss_pct"]:
        state["halted"] = True
        return Decision(False, "daily loss limit hit")
    budget = min(equity * r["max_position_pct"] / 100, float(account["buying_power"]))
    qty = math.floor(budget / price)
    if qty < 1:
        return Decision(False, "position too small")
    return Decision(True, "ok", qty,
                    round(price * (1 - r["stop_loss_pct"] / 100), 2),
                    round(price * (1 + r["take_profit_pct"] / 100), 2))
