#!/bin/bash
# Builds a labelled side-by-side (Seedance left, Kling right) from two lettered finals.
# Usage: ./sidebyside.sh out/01-hazen-final-seedance.mp4 out/01-hazen-final-kling.mp4 out/01-hazen-sidebyside.mp4
set -e
FONT=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
ffmpeg -v error -y -i "$1" -i "$2" -filter_complex "
 [0:v]scale=960:540,pad=960:580:0:40:black,drawtext=fontfile=$FONT:text='SEEDANCE':fontcolor=white:fontsize=24:x=(w-text_w)/2:y=8[l];
 [1:v]scale=960:540,pad=960:580:0:40:black,drawtext=fontfile=$FONT:text='KLING':fontcolor=white:fontsize=24:x=(w-text_w)/2:y=8[r];
 [l][r]hstack=inputs=2[o]" -map "[o]" -c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart "$3"
echo "wrote $3"
