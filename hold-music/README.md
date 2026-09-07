# Hold music for Claude Code

Plays a little tune while Claude is working, and stops it the moment Claude
finishes. Think of it as on-hold music for your terminal.

There is no "Claude is thinking" event to hook into, but there are two events
that bracket it almost exactly:

| Event | Fires when | We do |
| --- | --- | --- |
| `UserPromptSubmit` | you hit enter, before Claude starts | start the music |
| `Stop` | Claude finishes its turn | stop the music |
| `Notification` | Claude pauses to ask you something | stop the music |
| `SessionEnd` | you quit Claude Code | stop the music |

So the music plays for exactly as long as Claude is off doing something, which
is the effect you were after.

## Before you start

**The session has to be running on your own computer.** Hooks run wherever the
session runs, and a remote machine has no speakers.

- **Claude Desktop, Code tab**: start the session as **Local**, not Cloud. In
  the prompt area there is an **Environment** dropdown — set it to **Local**
  before you send your first message. This is the single most common reason for
  silence: everything can be configured perfectly and a cloud session will still
  play nothing. There is no visible badge afterwards telling you which kind of
  session you are in, and an existing session cannot be switched, so check the
  dropdown up front.
- **Claude Code in a terminal** (`claude`): always local, nothing to choose.
- **Claude Code on the web**: remote, so no sound. Nothing to be done about it.
- **The Chat tab / the regular Claude app**: does not support hooks at all.

You need `python3` (only to generate the tune once) and any one of these audio
players, most of which you probably already have:

- macOS: `afplay` — built in, nothing to install
- Linux: `paplay`, `aplay`, `ffplay`, `mpv`, or `play` (sox)
- Windows: use WSL, or see [Windows](#windows) below

## Setup

The short version, if you just want it working:

```bash
cd hold-music
./install-hooks.sh
```

That edits `~/.claude/settings.json` for you (backing it up first), generates
the tune, and prints what it did. To undo it later, run
`./install-hooks.sh --uninstall`. Then restart Claude Code, or start a new
session, and run `/hooks` to confirm the four hooks are listed.

Running it twice is harmless, anything already in your settings is preserved,
and if your settings file has a JSON syntax error it stops and tells you rather
than mangling the file.

The rest of this section is the same thing done by hand, if you would rather see
exactly what changes.

**1. Generate the tune.**

```bash
cd hold-music
python3 generate_tune.py
```

That writes `hold-music.wav`: an original 14-second chiptune phrase repeated to
fill about three minutes. (The file is not committed to git, since it is several
megabytes of something a script can rebuild on demand.)

If you skip this step, nothing breaks: the first prompt you send starts building
the tune in the background and plays nothing, and the music starts working from
the next prompt on. Generating takes about five seconds, and hooks hold up your
prompt while they run, so it is not something to do on the critical path.

Have a listen before wiring anything up:

```bash
./play.sh     # starts it
./stop.sh     # stops it
```

**2. Tell Claude Code about the scripts.**

Open `~/.claude/settings.json` (create it if it does not exist) and add a
`hooks` section. If the file already has other settings in it, just add the
`"hooks"` key alongside them — do not replace the whole file.

Replace `/ABSOLUTE/PATH/TO` with the real path to this folder. Run `pwd` inside
the `hold-music` directory to get it.

```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [ { "type": "command", "command": "/ABSOLUTE/PATH/TO/hold-music/play.sh" } ] }
    ],
    "Stop": [
      { "hooks": [ { "type": "command", "command": "/ABSOLUTE/PATH/TO/hold-music/stop.sh" } ] }
    ],
    "Notification": [
      { "hooks": [ { "type": "command", "command": "/ABSOLUTE/PATH/TO/hold-music/stop.sh" } ] }
    ],
    "SessionEnd": [
      { "hooks": [ { "type": "command", "command": "/ABSOLUTE/PATH/TO/hold-music/stop.sh" } ] }
    ]
  }
}
```

There is a ready-to-edit copy of this in [`settings-snippet.json`](settings-snippet.json).

**3. Check it took.** Claude Code watches the settings file and usually picks up
hook changes within a few seconds; if nothing happens, start a new session. Run
`/hooks` to see what it has loaded — it is a read-only viewer, which makes it a
good way to confirm your JSON parsed. Then ask for something slow.

## Using your own music instead

Point `HOLD_MUSIC_FILE` at any audio file your player can handle:

```json
{ "type": "command",
  "command": "HOLD_MUSIC_FILE=~/Music/my-hold-music.mp3 /ABSOLUTE/PATH/TO/hold-music/play.sh" }
```

Set the same variable on the `stop.sh` lines too, so it knows what to shut down.

A note on the obvious choice: the Jeopardy think-music is under copyright, so
there is no legal file for this repo to ship. Any track you already own is fine
for personal use.

## Knobs

| Variable | Default | What it does |
| --- | --- | --- |
| `HOLD_MUSIC_FILE` | `hold-music.wav` beside the script | which audio file to play |
| `HOLD_MUSIC_VOLUME` | `0.35` | 0.0 to 1.0, on players that support it |
| `HOLD_MUSIC_PLAYER` | auto-detected | force a player, e.g. `mpv --no-video` |

The tune itself is configurable too:

```bash
python3 generate_tune.py --bpm 150          # more frantic
python3 generate_tune.py --minutes 10       # for very long jobs
python3 generate_tune.py --out other.wav
```

To change the melody, edit the `MELODY` and `CHORDS` lists near the bottom of
`generate_tune.py`. They are plain note names like `("C5", 1)`, meaning "play C
in the fifth octave for one beat".

## How it works

`play.sh` starts a detached background loop that plays the file over and over,
and writes the loop's process ID to `/tmp/claude-hold-music.pid`. `stop.sh`
reads that file and kills the process.

Two details that took some care:

- **The loop gets its own process group** (`set -m` in `play.sh`), and `stop.sh`
  kills the whole group with `kill -- -$pid`. Killing just the loop leaves the
  player, and anything the player spawned, orphaned and still audible.
- **`play.sh` prints nothing on stdout.** Whatever a `UserPromptSubmit` hook
  prints gets injected into Claude's context as extra instructions, so a chatty
  script would quietly pollute every prompt you send.

Starting twice is harmless — `play.sh` notices the music is already playing and
does nothing — and stopping when nothing is playing is a no-op.

Hooks are blocking, so a slow one would delay your prompt. `play.sh` returns in
about ten milliseconds, well inside the 30-second `UserPromptSubmit` budget. If
you swap in something slower, add `"async": true` next to `"type": "command"`
to run it in the background instead.

## Windows

The scripts are bash. On Windows, run Claude Code under WSL and use them as-is.
For native PowerShell, replace the hook commands with:

```powershell
# start
powershell -c "(New-Object Media.SoundPlayer 'C:\path\hold-music.wav').PlayLooping()"
# stop
powershell -c "Get-Process powershell | Where-Object {$_.Id -ne $PID} | Stop-Process"
```

That stop command is blunt — it kills other PowerShell processes too — so treat
it as a starting point rather than something to leave running.

## Troubleshooting

**No sound.** Check a player exists (`command -v afplay ffplay paplay aplay mpv`)
and that `./play.sh` works on its own from the terminal. `play.sh` deliberately
swallows all errors so a broken setup can never block your prompts, which does
make it silent about its own problems — run the player by hand to see them:

```bash
afplay hold-music.wav        # macOS
ffplay -nodisp -autoexit hold-music.wav
```

**Music never stops.** Run `./stop.sh` by hand. If that fixes it, your `Stop`
hook is not firing — check `/hooks` and your JSON syntax (a stray comma is the
usual culprit).

**Hooks are listed in `/hooks` but nothing happens.** Check the session is
running locally rather than in the cloud. Then run `/debug` in the session to
turn on debug logging, which records which hooks matched and what exit code and
output each produced.

**Music stops too early.** The `Notification` hook fires when Claude wants your
input. If you would rather the music keep playing through permission prompts,
delete the `Notification` block.

**It plays during short replies too.** It will — any prompt starts it, even one
Claude answers instantly. That is the nature of the two events we have to work
with.
