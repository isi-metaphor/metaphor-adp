#!/bin/bash

# Usage:
#   ./run-en.sh [input] [output]
# or
#   ./run-en.sh [input]
# or
#   < [input] ./run-en.sh

INPUT_FILE="${1:-/dev/stdin}"
OUTPUT_FILE="${2:-/dev/stdout}"

EN_PIPELINE_DIR=$METAPHOR_DIR/pipelines/English

if [ -d "$2" ]; then
    $EN_PIPELINE_DIR/preproc.sh < $INPUT_FILE |
    tee $2/tmp.tok |
    $EN_PIPELINE_DIR/parse.sh |
    tee $2/tmp.candc |
    $EN_PIPELINE_DIR/create-lf.sh > /dev/stdout
else
    $EN_PIPELINE_DIR/preproc.sh < $INPUT_FILE |
    $EN_PIPELINE_DIR/parse.sh |
    $EN_PIPELINE_DIR/create-lf.sh > $OUTPUT_FILE
fi
