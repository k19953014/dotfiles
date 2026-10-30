"""Compact subscription quota display for Herdr's tab bar."""
import json
import math
import os
from pathlib import Path
import subprocess
import time


def read_json(command):
    result = subprocess.run(command, capture_output=True, text=True, timeout=8, check=True)
    return json.loads(result.stdout)


def format_provider(provider, now):
    windows = {}
    stale = "stale" in (provider.get("Note") or "").lower()
    for key in ("Primary", "Secondary", "Tertiary"):
        window = provider.get(key)
        if not window:
            continue
        minutes = window.get("windowMinutes")
        if minutes not in (300, 10080):
            continue
        expired = window.get("resetsAt") is not None and window["resetsAt"] <= now
        value = window.get("usedPercentage")
        if expired or stale or not isinstance(value, (int, float)) or not math.isfinite(value):
            windows[minutes] = "--"
            stale = stale or expired
        else:
            windows[minutes] = f"{max(0, min(100, 100 - value)):.0f}%"
    label = provider.get("Label") or provider["ProviderID"]
    suffix = " (stale)" if stale else ""
    return f"{label} 5h {windows.get(300, '--')} 7d {windows.get(10080, '--')}{suffix}"


def main():
    herdr = os.environ.get("HERDR_BIN_PATH") or "herdr"
    plugins = read_json([herdr, "plugin", "list", "--plugin", "usagebar", "--json"])
    plugin = next(p for p in plugins["result"]["plugins"] if p["plugin_id"] == "usagebar")
    binary = Path(plugin["plugin_root"]) / "bin" / "usagebar"
    snapshot = read_json([str(binary), "collect", "--all", "--quotas-only"])
    providers = snapshot.get("providers") or []
    selected = []
    for kind in ("claude", "codex"):
        matches = [p for p in providers if p["ProviderID"] == kind or p.get("GroupLabel", "").lower() == kind]
        selected.extend(matches or [{"ProviderID": kind, "Label": kind.title()}])
    print(" | ".join(format_provider(p, time.time()) for p in selected))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, StopIteration, subprocess.SubprocessError):
        print("Quota unavailable")
