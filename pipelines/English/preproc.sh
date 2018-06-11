#!/bin/bash

INPUT_FILE="${1:-/dev/stdin}"
OUTPUT_FILE="${2:-/dev/stdout}"

< $INPUT_FILE $BOXER_DIR/bin/tokkie --stdin > $OUTPUT_FILE
