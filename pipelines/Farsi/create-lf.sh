#!/bin/bash

# Convert the parse results to LF

INPUT_FILE="${1:-/dev/stdin}"
OUTPUT_FILE="${2:-/dev/stdout}"

FA_PIPELINE_DIR=$METAPHOR_DIR/pipelines/Farsi

$FA_PIPELINE_DIR/parse-to-lf/convertParseTreeToLF.py \
    $INPUT_FILE $OUTPUT_FILE \
    $FA_PIPELINE_DIR/parse-to-lf/farsiWordsForLFCreation.txt
