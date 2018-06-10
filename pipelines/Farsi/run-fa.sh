#!/bin/bash

# Usage:
#   ./run-fa.sh [input] [output]
# or
#   ./run-fa.sh [input]
# or
#   < [input] ./run-fa.sh

INPUT_FILE="${1:-/dev/stdin}"
OUTPUT_FILE="${2:-/dev/stdout}"

FA_PIPELINE_DIR=$METAPHOR_DIR/pipelines/Farsi

if [ -d "$2" ]; then
    $FA_PIPELINE_DIR/preproc.sh < $INPUT_FILE |
    tee $2/preparse_o.txt |
    $FA_PIPELINE_DIR/parse.sh |
    tee $2/parser_o.txt |
    $FA_PIPELINE_DIR/create-lf.sh > /dev/stdout
else
    $FA_PIPELINE_DIR/preproc.sh < $INPUT_FILE |
    $FA_PIPELINE_DIR/parse.sh |
    $FA_PIPELINE_DIR/create-lf.sh > $OUTPUT_FILE
fi
