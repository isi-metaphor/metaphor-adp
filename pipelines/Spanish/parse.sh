#!/bin/bash

# Parse Spanish

INPUT_FILE="${1:-/dev/stdin}"
OUTPUT_FILE="${2:-/dev/stdout}"

MALT_DIR=$METAPHOR_DIR/external-tools/malt-1.7.2

< $INPUT_FILE \
  java -Xmx16g -cp $MALT_DIR/maltparser-1.7.2.jar:$MALT_DIR \
     MaltParserWrap -c ancora_under40.mco -m parse -w $MALT_DIR \
     -lfi parser-es.log > $OUTPUT_FILE
