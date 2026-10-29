import yaml, pathlib

def load_rules(path="rules.yaml"):
    return yaml.safe_load(pathlib.Path(path).read_text(encoding="utf-8"))
