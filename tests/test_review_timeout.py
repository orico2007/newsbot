import subprocess, review

def test_run_claude_survives_timeout(monkeypatch):
    monkeypatch.setattr(review.shutil, "which", lambda n: "claude")
    def boom(*a, **k): raise subprocess.TimeoutExpired("claude", 1)
    monkeypatch.setattr(review.subprocess, "run", boom)
    assert "unavailable" in review.run_claude("x")
