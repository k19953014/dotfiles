#!/usr/bin/env python3
"""Merge portable Codex settings without copying credentials or local paths."""
import argparse
import datetime
import json
from pathlib import Path
import re
import tomllib

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--codex-home", type=Path, default=Path.home() / ".codex")
args = parser.parse_args()
source = Path(__file__).resolve().parent
settings = tomllib.loads((source / "config.toml").read_text())
config_path = args.codex_home / "config.toml"
old_config = config_path.read_text() if config_path.exists() else ""
old_values = tomllib.loads(old_config)
new_config = old_config
# Remove only complete top-level assignments. Parsing each value handles
# multiline TOML strings and prevents editing a partial assignment.
for key in settings:
    if key not in old_values:
        continue
    match = re.search(r"(?m)^" + re.escape(key) + r"\s*=", new_config)
    if not match:
        raise SystemExit(f"Unsupported assignment syntax for {key}; no files changed")
    start = match.start()
    end = start
    for line in new_config[start:].splitlines(keepends=True):
        end += len(line)
        try:
            value = tomllib.loads(new_config[start:end])
        except tomllib.TOMLDecodeError:
            continue
        if key in value:
            break
    else:
        raise SystemExit(f"Cannot parse {key}; no files changed")
    new_config = new_config[:start] + new_config[end:]
# Prepend to keep these settings at the TOML root, before any table.
header = "".join(key + " = " + json.dumps(value, ensure_ascii=False) + "\n"
                 for key, value in settings.items())
new_config = header + new_config
expected = dict(old_values)
expected.update(settings)
if tomllib.loads(new_config) != expected:
    raise SystemExit("Unrelated configuration changed; no files changed")

agents_path = args.codex_home / "AGENTS.md"
old_agents = agents_path.read_text() if agents_path.exists() else ""
rules = (source / "AGENTS.md").read_text().strip()
heading = rules.splitlines()[0]
pattern = re.compile(r"(?ms)^" + re.escape(heading) + r"\n.*?(?=^## |\Z)")
if pattern.search(old_agents):
    new_agents = pattern.sub(lambda _: rules + "\n\n", old_agents, count=1).rstrip() + "\n"
else:
    new_agents = old_agents.rstrip() + ("\n\n" if old_agents.strip() else "") + rules + "\n"

stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
args.codex_home.mkdir(parents=True, exist_ok=True)
for path, old, new in [(config_path, old_config, new_config),
                       (agents_path, old_agents, new_agents)]:
    if old == new:
        print(f"ok      {path}")
        continue
    if path.exists():
        backup = path.with_name(path.name + ".backup-" + stamp)
        backup.write_bytes(path.read_bytes())
        backup.chmod(0o600)
    path.write_text(new)
    if path == config_path:
        path.chmod(0o600)
    print(f"updated {path}")
