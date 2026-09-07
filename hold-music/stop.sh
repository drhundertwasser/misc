#!/usr/bin/env bash
# Stop the hold music. Wire this to Claude Code's Stop, Notification and
# SessionEnd hooks so the music ends whenever Claude stops working.
#
# Safe to run when nothing is playing.

set -uo pipefail
exec 2>/dev/null

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
track="${HOLD_MUSIC_FILE:-$here/hold-music.wav}"
pidfile="${TMPDIR:-/tmp}/claude-hold-music.pid"

if [[ -f "$pidfile" ]]; then
  pid="$(cat "$pidfile")"
  if [[ -n "$pid" ]]; then
    # play.sh gives the loop its own process group, so the negative PID takes
    # the player and its children down too. Fall back to the bare PID in case
    # the group is gone or was never created.
    kill -TERM -- "-$pid" 2>/dev/null || kill -TERM "$pid" 2>/dev/null
    for _ in 1 2 3 4 5 6 7 8 9 10; do
      kill -0 "$pid" 2>/dev/null || break
      sleep 0.05
    done
    kill -KILL -- "-$pid" 2>/dev/null || kill -KILL "$pid" 2>/dev/null
  fi
  rm -f "$pidfile"
fi

# Belt and braces: if a player outlived its parent loop, take it out by name.
if command -v pkill >/dev/null; then
  pkill -f "$track" 2>/dev/null
fi

exit 0
