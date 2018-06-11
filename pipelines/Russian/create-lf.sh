#!/bin/bash

INPUT_FILE="${1:-/dev/stdin}"
OUTPUT_FILE="${2:-/dev/stdout}"

RU_PIPELINE_DIR=$METAPHOR_DIR/pipelines/Russian

< $INPUT_FILE $RU_PIPELINE_DIR/parse-to-lf/malt_ru.py > $OUTPUT_FILE
