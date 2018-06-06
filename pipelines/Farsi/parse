#!/bin/bash

# Parse Farsi

INPUT_FILE="${1:-/dev/stdin}"
OUTPUT_FILE="${2:-/dev/stdout}"

MALT_DIR=$METAPHOR_DIR/external-tools/malt-1.5

< $INPUT_FILE \
    java -Xmx16g -cp $MALT_DIR/dist/malt/malt.jar:$MALT_DIR \
       MaltParserWrap -c farsiMALTModel.mco -w $MALT_DIR \
       -lfi parser-fa.log -m parse > $OUTPUT_FILE
