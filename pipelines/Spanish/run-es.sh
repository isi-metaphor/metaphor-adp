#!/bin/bash

INPUT_FILE="${1:-/dev/stdin}"
OUTPUT_FILE="${2:-/dev/stdout}"

ES_PIPELINE_DIR=$METAPHOR_DIR/pipelines/Spanish

if [ -d "$2" ]; then
    $ES_PIPELINE_DIR/preproc.sh < $INPUT_FILE |
    tee $2/tmp.tok |
    $ES_PIPELINE_DIR/parse.sh |
    tee $2/tmp.malt |
    $ES_PIPELINE_DIR/create-lf.sh > /dev/stdout
else
    $ES_PIPELINE_DIR/preproc.sh < $INPUT_FILE |
    $ES_PIPELINE_DIR/parse.sh |
    $ES_PIPELINE_DIR/create-lf.sh > $OUTPUT_FILE
fi
