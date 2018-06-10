#!/bin/bash

INPUT_FILE="${1:-/dev/stdin}"
OUTPUT_FILE="${2:-/dev/stdout}"

ES_PIPELINE_DIR=$METAPHOR_DIR/pipelines/Spanish

< $INPUT_FILE $ES_PIPELINE_DIR/parse-to-lf/malt_to_prop.py > $OUTPUT_FILE
