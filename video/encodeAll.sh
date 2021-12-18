#!/bin/sh

OUTPUT_DIR=./new_encoding

#IFS=$'\n'  # split only on newlines
for FILE in *mp4
do
    FILENAME=`basename "${FILE}" .mp4`
    ffmpeg -i  "$FILE" "$OUTPUT_DIR/$FILENAME.mp4"
    #echo $FILENAME
done
