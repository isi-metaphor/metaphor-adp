#!/bin/bash

INPUT_FILE="${1:-/dev/stdin}"
OUTPUT_FILE="${2:-/dev/stdout}"

BOXER_BIN=$BOXER_DIR/bin/boxer
BOXER_OPT="--semantics tacitus --resolve true --stdin"

< $INPUT_FILE $BOXER_BIN $BOXER_OPT > $OUTPUT_FILE
