# 722 Proofs in a Night — mini documentary

A ~7.5 minute narrated explainer, for a lay audience, on OpenAI's October 6 2026
release of 722 AI-written mathematical manuscripts (the "quasi-Riemann hypothesis",
matrix multiplication, Kakeya, and the backlash from mathematicians).

Files:

- `722_proofs_in_a_night.mp4` — the finished video (1080p, 30 fps, narrated). Just play this.
- `722_proofs_in_a_night.srt` — optional subtitles. Drop it next to the MP4 in VLC and they load automatically.
- `script.py` — the narration and on-screen text, one scene per entry. Edit the words here.
- `render.py` — builds the video from `script.py` (draws the frames, synthesizes the voice, mixes audio).

## Re-generating the video after editing the script

You need Python 3, ffmpeg, and the `piper-tts` package, plus one voice file.

```bash
pip install piper-tts numpy pillow
mkdir -p voice && cd voice
curl -LO https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
curl -LO https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
cd ..
python3 render.py      # output lands in ./out/722_proofs_in_a_night.mp4
```

`render.py` expects the voice at `../voice/en_US-lessac-medium.onnx` relative to itself;
change the `VOICE` line near the top if you put it somewhere else. Rendering takes about
four minutes on a four-core machine. Delete `out/*.wav` if you change narration text, since
synthesized audio is cached.

## Sources used for the facts

- Scientific American, "The most exciting claims from OpenAI's heap of new proofs", Oct 8 2026
- The `openai/math` GitHub repository README (counts, Lean coverage, compute figure)
- Association for Human Mathematics statement, guest post on Terence Tao's blog, Oct 7 2026
- Fields Medalists' declaration "A Severe Misalignment of AI in Mathematics", Sep 11 2026
- Kevin Buzzard, Xena blog, Oct 1 2026
- explainx.ai breakdown of headline claims vs. what Lean actually verified

Most of the results are not yet peer reviewed. The video says so.
