#!/usr/bin/env bash
# Add (or remove) the hold-music hooks in your Claude Code settings.
#
#   ./install-hooks.sh              # turn the music on
#   ./install-hooks.sh --uninstall  # turn it back off
#
# Edits ~/.claude/settings.json, keeping everything already in there and
# writing a timestamped backup first. Safe to run twice: it notices when the
# hooks are already installed and leaves the file alone.

set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
settings="${CLAUDE_SETTINGS:-$HOME/.claude/settings.json}"
mode="install"
[[ "${1:-}" == "--uninstall" ]] && mode="uninstall"

if ! command -v python3 >/dev/null; then
  echo "Need python3 to edit the settings file safely. Install it and retry." >&2
  exit 1
fi

mkdir -p "$(dirname "$settings")"

if [[ -f "$settings" ]]; then
  backup="$settings.backup-$(date +%Y%m%d-%H%M%S)"
  cp "$settings" "$backup"
  echo "Backed up your existing settings to:"
  echo "  $backup"
fi

python3 - "$settings" "$here" "$mode" <<'PY'
import json, os, sys

settings_path, script_dir, mode = sys.argv[1], sys.argv[2], sys.argv[3]

# Which script each event should run.
WIRING = {
    "UserPromptSubmit": "play.sh",
    "Stop": "stop.sh",
    "Notification": "stop.sh",
    "SessionEnd": "stop.sh",
}

if os.path.exists(settings_path):
    with open(settings_path) as fh:
        text = fh.read().strip()
    try:
        settings = json.loads(text) if text else {}
    except json.JSONDecodeError as exc:
        sys.exit(
            f"Your settings file is not valid JSON, so I stopped rather than\n"
            f"risk mangling it: {settings_path}\n"
            f"  {exc}\n"
            f"Fix that error (usually a stray or missing comma) and run this again."
        )
else:
    settings = {}

hooks = settings.setdefault("hooks", {})
ours = lambda cmd: cmd.startswith(script_dir + os.sep)  # noqa: E731
changed = []

if mode == "install":
    for event, script in WIRING.items():
        command = os.path.join(script_dir, script)
        groups = hooks.setdefault(event, [])
        if any(ours(h.get("command", "")) for g in groups for h in g.get("hooks", [])):
            continue  # already wired up
        groups.append({"hooks": [{"type": "command", "command": command}]})
        changed.append(event)
else:
    for event in list(hooks):
        groups = hooks[event]
        for group in groups:
            group["hooks"] = [h for h in group.get("hooks", [])
                              if not ours(h.get("command", ""))]
        kept = [g for g in groups if g.get("hooks")]
        if len(kept) != len(groups):
            changed.append(event)
        if kept:
            hooks[event] = kept
        else:
            del hooks[event]

if not hooks:
    del settings["hooks"]

# Write to a temp file and rename, so an interrupted run cannot truncate
# the real settings file.
tmp = settings_path + ".tmp"
with open(tmp, "w") as fh:
    json.dump(settings, fh, indent=2)
    fh.write("\n")
os.replace(tmp, settings_path)

if changed:
    verb = "Added" if mode == "install" else "Removed"
    print(f"{verb} hooks for: {', '.join(changed)}")
else:
    print("Nothing to change - your settings were already how you want them.")
PY

echo
echo "Settings file: $settings"
if [[ "$mode" == "install" ]]; then
  if [[ ! -f "$here/hold-music.wav" ]]; then
    echo
    echo "Now generating the tune (takes about five seconds)..."
    python3 "$here/generate_tune.py"
  fi
  echo
  echo "Done. In Claude Code, run /hooks to confirm they loaded, then ask"
  echo "for something slow and you should hear it. Music only plays in LOCAL"
  echo "sessions - cloud sessions run on a remote machine with no speakers."
fi
