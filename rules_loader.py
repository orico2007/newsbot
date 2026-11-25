import copy, pathlib, yaml

def _merge(base, over):
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict): _merge(base[k], v)
        else: base[k] = v
    return base

def load_rules(path="rules.yaml"):
    """Load rules.yaml. If `profile: <name>` is set and `profiles.<name>` exists, that block is merged over the defaults
    (e.g. profile: small for a ~$1-2k account: few big positions, whole shares only, no day trades, no crypto)."""
    r = yaml.safe_load(pathlib.Path(path).read_text(encoding="utf-8"))
    prof = (r.get("profile") or "standard")
    over = (r.get("profiles") or {}).get(prof)
    if over: _merge(r, copy.deepcopy(over))
    return r
