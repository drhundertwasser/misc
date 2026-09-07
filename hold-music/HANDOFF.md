# Handoff: hold music for Claude Code

Paste this into a new conversation to pick up where the last one left off.

## What this is

A small project that plays music while Claude Code is working and stops it the
instant Claude finishes — hold music for your terminal. It is done and pushed;
what remains is running it on my Mac.

## Where it lives

- Repo: `drhundertwasser/misc`
- Branch: `claude/hold-music-thinking-ncn1dp`
- Folder: `hold-music/`
- No pull request has been opened.

## Status: complete and tested

| File | What it is |
| --- | --- |
| `generate_tune.py` | Writes `hold-music.wav` — an original chiptune loop, no dependencies |
| `play.sh` | Starts a detached looping player, records its PID |
| `stop.sh` | Kills the player's whole process group |
| `install-hooks.sh` | Merges the hooks into `~/.claude/settings.json`; `--uninstall` reverses it |
| `settings-snippet.json` | The same config to paste by hand instead |
| `README.md` | Full setup, knobs, troubleshooting |

The audio file is gitignored — several megabytes a script can rebuild in about
five seconds.

## How it hooks in

There is no "Claude is thinking" event, but four real events bracket it:

- `UserPromptSubmit` → start the music
- `Stop` → stop it (Claude finished)
- `Notification` → stop it (Claude is asking me something)
- `SessionEnd` → stop it (I quit)

## The one thing that decides whether this works

**Hooks run wherever the session runs.** In Claude Desktop's Code tab, a session
is either Local (my Mac) or Cloud (a remote machine with no speakers). It must
be **Local**. This is the most likely cause of silence, and everything else can
be configured perfectly while a Cloud session still plays nothing.

Claude Code in a terminal is always local. Claude Code on the web is always
remote. The regular Claude chat app has no hooks at all.

To start a Local session in Claude Desktop: open the **Code** tab, set the
**Environment** dropdown to **Local**, click **Select folder** and choose the
project folder, pick a model and a permission mode, then type the prompt. The
Desktop app has Claude Code built in — there is no CLI or Node.js to install
separately. There is no indicator afterwards showing whether a session is Local
or Cloud, and an existing session cannot be converted, so set the dropdown
before sending the first message.

## What I still need to do

```bash
git clone -b claude/hold-music-thinking-ncn1dp https://github.com/drhundertwasser/misc.git ~/misc
cd ~/misc/hold-music
./install-hooks.sh
```

Then start a new **Local** session and run `/hooks` to confirm four hooks are
listed. `python3` and `afplay` are already on macOS, so there is nothing else to
install.

## Decisions already made — no need to revisit

- **The tune is generated, not shipped.** The Jeopardy think-music is under
  copyright, so there is no legal file to commit. `HOLD_MUSIC_FILE` points the
  scripts at any track I already own.
- **`play.sh` prints nothing on stdout.** Anything a `UserPromptSubmit` hook
  prints is injected into Claude's context as instructions, so a chatty script
  would pollute every prompt.
- **The player runs in its own process group** and `stop.sh` kills the group,
  not just the loop. Killing only the loop leaves the player orphaned and
  still audible.
- **All errors are swallowed** so a broken audio setup can never block a
  prompt. The tradeoff is that it fails silently; the README says to run the
  player by hand to see the real error.
- **`install-hooks.sh` merges rather than overwrites**: backs up first, keeps
  existing settings and unrelated hooks, is a no-op on a second run, and
  refuses to touch a settings file that is not valid JSON.

Tested: existing settings preserved, unrelated hooks preserved, double-run
produces no duplicates, uninstall removes only its own entries, fresh machine
with no settings file, and malformed JSON aborts cleanly.

## Ideas if I want more later

- Different tunes for different work (tests vs. builds vs. long thinking)
- Fade out instead of a hard stop
- A `PreToolUse` hook so music only starts for genuinely slow operations
  rather than every prompt, including ones Claude answers instantly
