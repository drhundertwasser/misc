#!/usr/bin/env python3
"""Generate an original chiptune loop to use as Claude Code hold music.

Writes a WAV file using nothing but the Python standard library, so there is
no pip install step. Run it once and the play script does the rest:

    python3 generate_tune.py                 # -> hold-music.wav
    python3 generate_tune.py --minutes 5     # a longer file = fewer loop gaps
    python3 generate_tune.py --bpm 150 --out fast.wav

The tune is a short 8-bar phrase repeated back to back. Most command line
audio players cannot loop a file on their own, so we bake the repeats into
the file instead and let the player restart it only rarely.
"""

import argparse
import math
import random
import struct
import wave

SAMPLE_RATE = 22050

# Semitone distance from A4 (440 Hz) for every note name we use.
_PITCH_CLASS = {
    "C": -9, "C#": -8, "Db": -8, "D": -7, "D#": -6, "Eb": -6, "E": -5,
    "F": -4, "F#": -3, "Gb": -3, "G": -2, "G#": -1, "Ab": -1, "A": 0,
    "A#": 1, "Bb": 1, "B": 2,
}


def note_hz(name):
    """Turn a note name like 'C#4' or 'A3' into a frequency in Hz."""
    octave = int(name[-1])
    semitones = _PITCH_CLASS[name[:-1]] + 12 * (octave - 4)
    return 440.0 * (2.0 ** (semitones / 12.0))


def envelope(i, total, attack, release):
    """A simple attack/release volume shape, so notes do not click."""
    if i < attack:
        return i / attack
    if i > total - release:
        return max(0.0, (total - i) / release)
    return 1.0


def add_lead(buf, start, duration, hz, gain=0.30):
    """A pulse wave with a little vibrato - the melody voice."""
    n = int(duration * SAMPLE_RATE)
    attack = int(0.010 * SAMPLE_RATE)
    release = int(0.070 * SAMPLE_RATE)
    phase = 0.0
    for i in range(n):
        t = i / SAMPLE_RATE
        vibrato = 1.0 + 0.006 * math.sin(2 * math.pi * 5.5 * t)
        phase += 2 * math.pi * hz * vibrato / SAMPLE_RATE
        # 30% duty-cycle pulse: brighter and reedier than a plain square.
        value = 1.0 if (phase % (2 * math.pi)) < (2 * math.pi * 0.30) else -1.0
        idx = start + i
        if idx < len(buf):
            buf[idx] += value * gain * envelope(i, n, attack, release)


def add_bass(buf, start, duration, hz, gain=0.34):
    """A soft triangle wave an octave or two down - the walking bass."""
    n = int(duration * SAMPLE_RATE)
    attack = int(0.006 * SAMPLE_RATE)
    release = int(0.040 * SAMPLE_RATE)
    for i in range(n):
        phase = (hz * i / SAMPLE_RATE) % 1.0
        value = 4.0 * abs(phase - 0.5) - 1.0
        idx = start + i
        if idx < len(buf):
            buf[idx] += value * gain * envelope(i, n, attack, release)


def add_tick(buf, start, gain=0.10):
    """A very short noise burst standing in for a hi-hat."""
    n = int(0.030 * SAMPLE_RATE)
    for i in range(n):
        idx = start + i
        if idx < len(buf):
            buf[idx] += random.uniform(-1.0, 1.0) * gain * (1.0 - i / n)


# Melody, written out bar by bar as (note or None for a rest, beats).
MELODY = [
    ("A4", 1), ("C5", 1), ("E5", 1), ("C5", 1),
    ("F4", 1), ("A4", 1), ("C5", 2),
    ("G4", 1), ("E5", 1), ("D5", 1), ("C5", 1),
    ("B4", 1), ("D5", 1), ("G5", 2),
    ("E5", 0.5), ("D5", 0.5), ("C5", 1), ("A4", 2),
    ("F5", 1), ("E5", 1), ("C5", 2),
    ("B4", 1), ("G#4", 1), ("B4", 1), ("D5", 1),
    ("A4", 2), (None, 2),
]

# One chord per bar. Each entry is (root note, fifth note) for the bass line.
CHORDS = [
    ("A2", "E3"), ("F2", "C3"), ("C2", "G2"), ("G2", "D3"),
    ("A2", "E3"), ("F2", "C3"), ("E2", "B2"), ("A2", "E3"),
]

BEATS_PER_BAR = 4


def render_phrase(bpm):
    """Render the 8-bar phrase once and return it as a list of floats."""
    beat = 60.0 / bpm
    total_beats = len(CHORDS) * BEATS_PER_BAR
    buf = [0.0] * int(total_beats * beat * SAMPLE_RATE + SAMPLE_RATE)

    # Melody.
    position = 0.0
    for name, beats in MELODY:
        if name is not None:
            add_lead(buf, int(position * beat * SAMPLE_RATE), beats * beat * 0.92,
                     note_hz(name))
        position += beats

    # Bass and ticks, one bar at a time.
    for bar, (root, fifth) in enumerate(CHORDS):
        bar_start = bar * BEATS_PER_BAR
        pattern = [root, root, fifth, root]
        for step, name in enumerate(pattern):
            at = int((bar_start + step) * beat * SAMPLE_RATE)
            add_bass(buf, at, beat * 0.85, note_hz(name))
        for step in range(BEATS_PER_BAR * 2):
            at = int((bar_start + step * 0.5) * beat * SAMPLE_RATE)
            add_tick(buf, at, gain=0.10 if step % 2 else 0.05)

    # Trim to exactly the phrase length so repeats butt up seamlessly.
    return buf[: int(total_beats * beat * SAMPLE_RATE)]


def write_wav(path, samples):
    peak = max(abs(s) for s in samples) or 1.0
    scale = 0.85 * 32767 / peak
    frames = b"".join(struct.pack("<h", int(s * scale)) for s in samples)
    with wave.open(path, "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(SAMPLE_RATE)
        out.writeframes(frames)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", default="hold-music.wav", help="output WAV path")
    parser.add_argument("--bpm", type=float, default=132.0, help="tempo (default 132)")
    parser.add_argument("--minutes", type=float, default=3.0,
                        help="roughly how long the finished file should be")
    args = parser.parse_args()

    random.seed(7)  # keep the hi-hat noise identical between runs
    phrase = render_phrase(args.bpm)
    phrase_seconds = len(phrase) / SAMPLE_RATE
    repeats = max(1, round(args.minutes * 60 / phrase_seconds))

    write_wav(args.out, phrase * repeats)
    print(f"Wrote {args.out}: {phrase_seconds:.1f}s phrase x {repeats} "
          f"= {phrase_seconds * repeats / 60:.1f} min")


if __name__ == "__main__":
    main()
