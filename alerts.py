"""התראות לטלפון. ntfy.sh (בלי הרשמה: מתקינים את אפליקציית ntfy ונרשמים לנושא) או Telegram. כשל = שקט."""
import os, requests

def send(text, title="NewsBot"):
    if os.getenv("PYTEST_CURRENT_TEST") or os.getenv("NEWSBOT_NO_ALERTS"): return      # בדיקות לא שולחות התראות אמיתיות
    topic = os.getenv("NTFY_TOPIC")
    tg_token, tg_chat = os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_CHAT_ID")
    try:
        if topic:
            requests.post(f"https://ntfy.sh/{topic}", data=text.encode("utf-8"), headers={"Title": title}, timeout=8)
        if tg_token and tg_chat:
            requests.post(f"https://api.telegram.org/bot{tg_token}/sendMessage", json={"chat_id": tg_chat, "text": f"{title}\n{text}"}, timeout=8)
    except Exception:
        pass
