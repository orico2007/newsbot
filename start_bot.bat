@echo off
cd /d "%~dp0"
set PYTHONUTF8=1
:loop
python bot.py >> bot.log 2>&1
timeout /t 30 /nobreak >nul
goto loop
