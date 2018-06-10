#!/bin/bash

INPUT_FILE="${1:-/dev/stdin}"
OUTPUT_FILE="${2:-/dev/stdout}"

TOKENIZER_BIN=$BOXER_DIR/bin/tokkie

TOKENIZER_OPT="--stdin"

< $INPUT_FILE $BOXER_DIR/bin/tokkie --stdin > $OUTPUT_FILE
