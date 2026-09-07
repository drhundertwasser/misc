#!/usr/bin/env bash
# Start the hold music. Meant to be wired to Claude Code's UserPromptSubmit hook.
#
# Returns immediately: playback happens in a detached background process whose
# PID is written to a file so stop.sh can find it later. Prints nothing on
# stdout, because whatever a UserPromptSubmit hook prints gets fed to Claude as
# extra context.
#
#   HOLD_MUSIC_FILE    audio file to play (default: hold-music.wav next to this script)
#   HOLD_MUSIC_VOLUME  0.0 to 1.0 (default 0.35)
#   HOLD_MUSIC_PLAYER  force a specific player command

set -uo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
track="${HOLD_MUSIC_FILE:-$here/hold-music.wav}"
volume="${HOLD_MUSIC_VOLUME:-0.35}"
pidfile="${TMPDIR:-/tmp}/claude-hold-music.pid"

# Never let a problem here block the prompt from going through.
exec 2>/dev/null

# Already playing? Leave it alone.
if [[ -f "$pidfile" ]] && kill -0 "$(cat "$pidfile")" 2>/dev/null; then
  exit 0
fi

# No tune yet? Build it in the background and stay quiet this turn. Generating
# takes a few seconds and hooks block the prompt, so doing it inline would hang
# the first thing you type. Music starts from the next prompt onwards.
if [[ ! -f "$track" ]]; then
  if [[ "$track" == "$here/hold-music.wav" ]]; then
    # mkdir is atomic, so overlapping prompts cannot start two generators.
    if mkdir "$here/.generating" 2>/dev/null; then
      (
        python3 "$here/generate_tune.py" --out "$track.part" >/dev/null 2>&1 &&
          mv -f "$track.part" "$track"
        rmdir "$here/.generating"
      ) >/dev/null 2>&1 &
    fi
  fi
  exit 0
fi

# Pick a player. Each entry plays the file once and exits.
pct=$(awk -v v="$volume" 'BEGIN { printf "%d", v * 100 }')
if [[ -n "${HOLD_MUSIC_PLAYER:-}" ]]; then
  # shellcheck disable=SC2206
  player=(${HOLD_MUSIC_PLAYER} "$track")
elif command -v afplay >/dev/null; then           # macOS
  player=(afplay -v "$volume" "$track")
elif command -v ffplay >/dev/null; then           # ffmpeg
  player=(ffplay -nodisp -autoexit -loglevel quiet -volume "$pct" "$track")
elif command -v mpv >/dev/null; then
  player=(mpv --no-video --really-quiet --volume="$pct" "$track")
elif command -v paplay >/dev/null; then           # PulseAudio / PipeWire
  player=(paplay "$track")
elif command -v aplay >/dev/null; then            # ALSA
  player=(aplay -q "$track")
elif command -v play >/dev/null; then             # sox
  player=(play -q "$track")
else
  exit 0
fi

# Loop the track until we are told to stop, killing the player on the way out.
# `set -m` puts the background job in a process group of its own, so stop.sh can
# kill the loop, the player, and anything the player spawned in one go. Without
# it a player that shells out leaves orphans behind, still making noise.
set -m
(
  child=""
  trap 'if [[ -n "$child" ]]; then kill "$child" 2>/dev/null; fi; exit 0' TERM INT
  while true; do
    "${player[@]}" >/dev/null 2>&1 &
    child=$!
    wait "$child"
  done
) >/dev/null 2>&1 &

echo $! > "$pidfile"
set +m
exit 0
