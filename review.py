"""סקירה שבועית: Claude קורא כרטיס ציונים, backtest ודוחות אחרונים ומציע שינויים בכללים (לא מיישם בעצמו)."""
import pathlib, shutil, subprocess, sys

PROMPT = """You are reviewing a paper-trading bot (US stocks + crypto) run by a retail trader. Below are its scorecard, backtest, and recent daily reports.
Write a concise weekly review in Markdown with: (1) what worked and what did not, with numbers; (2) at most 5 concrete, evidence-based changes to rules.yaml
(name the key and a suggested value; say how many trades support each); (3) any risk you see (concentration, slippage, losing streaks).
Do not invent data. If there are fewer than 20 closed trades, say the sample is too small and keep suggestions to process fixes only.

{material}
"""

def gather(data="data", n_reports=5):
    d = pathlib.Path(data); parts = []
    for name in ("scorecard.md", "backtest.md"):
        p = d / name
        if p.exists(): parts.append(f"=== {name} ===\n{p.read_text(encoding='utf-8')[:6000]}")
    reps = sorted((d / "reports").glob("*.md"))[-n_reports:] if (d / "reports").exists() else []
    for r in reps: parts.append(f"=== report {r.stem} ===\n{r.read_text(encoding='utf-8')[:3000]}")
    return "\n\n".join(parts) or "(no data yet)"

def run_claude(prompt):
    exe = shutil.which("claude")
    if not exe: raise RuntimeError("claude CLI not found")
    out = subprocess.run([exe, "-p", "--tools", ""], input=prompt, capture_output=True, text=True, encoding="utf-8", timeout=300)
    return out.stdout.strip()

def main():
    material = gather()
    text = run_claude(PROMPT.format(material=material)) if material != "(no data yet)" else "No data yet - nothing to review."
    pathlib.Path("data").mkdir(exist_ok=True)
    pathlib.Path("data/review.md").write_text("# Weekly review\n\n" + text + "\n", encoding="utf-8")
    print(text[:500])

if __name__ == "__main__":
    sys.exit(main())
