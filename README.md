# NewsBot – בוט מסחר מבוסס חדשות (Paper בלבד כברירת מחדל)

זרימה: `חדשות Alpaca -> Claude נותן ציון 1-10 -> שער סיכון (risk.py + rules.yaml) -> פקודת Bracket (כניסה + סטופ + יעד)`

## הרצה
1. פתחו חשבון Paper ב-alpaca.markets והעתיקו מפתחות.
2. `cp .env.example .env`, מלאו מפתחות Alpaca, ואז `export $(cat .env | xargs)`
   - ברירת מחדל: Claude Code מותקן ומחובר אצלכם (`claude` בטרמינל) - בלי מפתח API.
   - אפשר גם `BRAIN_BACKEND=api` עם `ANTHROPIC_API_KEY`.
3. `pip install -r requirements.txt && python -m pytest -q && python bot.py`

כל החלטה (כולל דילוגים וחסימות) נרשמת ל-`journal.csv`. אחרי 3-4 שבועות בדמו בודקים שם אם יש יתרון אמיתי.
שינוי חוקים = עריכת `rules.yaml` בלבד. מעבר ל-Live חסום אלא אם `mode: live` וגם `ALLOW_LIVE=1`.

## הרצה אוטומטית בענן (GitHub Actions)
ה-workflow ב-`.github/workflows/trade.yml` מתעורר סביב פתיחת השוק האמריקאי (ימים ב'-ו'), בודק מול Alpaca אם השוק פתוח, סוחר (Paper) עד הסגירה, ושומר יומן ל-`data/journal.csv` בתוך הריפו.

Secrets נדרשים (Settings -> Secrets and variables -> Actions):
- `ALPACA_KEY_ID`, `ALPACA_SECRET_KEY` - מפתחות Paper
- `CLAUDE_CODE_OAUTH_TOKEN` - מתקבל מהפקודה `claude setup-token` (משתמש במנוי Claude)

אל תריצו במקביל גם את הגרסה המקומית (Task Scheduler) וגם את ה-Actions.
