#!/bin/bash

INPUT_FILE="${1:-/dev/stdin}"
OUTPUT_FILE="${2:-/dev/stdout}"

CANDC_BIN=$BOXER_DIR/bin/candc
CANDC_OPT="--models $BOXER_DIR/models/boxer --candc-printer boxer"

< $INPUT_FILE $CANDC_BIN $CANDC_OPT > $OUTPUT_FILE
