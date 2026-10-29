import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
import pytest

@pytest.fixture(autouse=True)
def _isolate_data(tmp_path, monkeypatch):
    for k in ("NTFY_TOPIC", "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"): monkeypatch.delenv(k, raising=False)
    """לא נוגעים בתיקיית data האמיתית: כל הכתיבות של הבוט והבדיקות הולכות לתיקייה זמנית"""
    import bot, crypto
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setattr(bot, "DATA", d); monkeypatch.setattr(bot, "STATE_FILE", d / "state.json"); monkeypatch.setattr(bot, "JOURNAL", d / "journal.csv")
    monkeypatch.setattr(crypto, "DATA", d); monkeypatch.setattr(crypto, "STATE_FILE", d / "state_crypto.json"); monkeypatch.setattr(crypto, "JOURNAL", d / "journal_crypto.csv")
    monkeypatch.chdir(tmp_path)
