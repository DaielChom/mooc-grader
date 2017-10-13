#!/bin/sh

for fname in `ls ./utils/*.py`
 do
  filename=$(basename "$fname")
  extension="${filename##*.}"
  filename="${filename%.*}"
  epyfname="$filename.e$extension"
  echo "encrypting $fname into $epyfname"
  ./utils/crypt "$fname" > ./utils/"$epyfname"
 done
