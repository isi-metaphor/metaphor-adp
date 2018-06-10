#!/bin/bash

# Usage:
#   ./run-ru.sh [input] [output]
# or
#   ./run-ru.sh [input]
# or
#   < [input] ./run-ru.sh

INPUT_FILE="${1:-/dev/stdin}"
OUTPUT_FILE="${2:-/dev/stdout}"

RU_PIPELINE_DIR=$METAPHOR_DIR/pipelines/Russian

if [ -d "$2" ]; then
    $RU_PIPELINE_DIR/preproc.sh < $INPUT_FILE |
    tee $2/preparse_o.txt |
    $RU_PIPELINE_DIR/parse.sh |
    tee $2/parser_o.txt |
    $RU_PIPELINE_DIR/create-lf.sh > /dev/stdout
else
    $RU_PIPELINE_DIR/preproc.sh < $INPUT_FILE |
    $RU_PIPELINE_DIR/parse.sh |
    $RU_PIPELINE_DIR/create-lf.sh > $OUTPUT_FILE
fi
