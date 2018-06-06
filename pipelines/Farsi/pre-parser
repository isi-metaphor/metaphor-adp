#!/bin/bash

INPUT_FILE="${1:-/dev/stdin}"
OUTPUT_FILE="${2:-/dev/stdout}"

FA_PIPELINE_DIR=$METAPHOR_DIR/pipelines/Farsi

if [ -d "$2" ]; then
    $FA_PIPELINE_DIR/tokenizer/farsilemm.py \
        $FA_PIPELINE_DIR/tokenizer/lemmatizationDict.txt < $INPUT_FILE |
    tee $2/preproc_o.txt |
    $FA_PIPELINE_DIR/tokenizer/tokenize |
    tee $2/tokenizer_o.txt |
    $FA_PIPELINE_DIR/tokenizer/addDot.py |
    tee $2/dot_o.txt |
    $FA_PIPELINE_DIR/tokenizer/tag |
    tee $2/tagger_o.txt |
    $FA_PIPELINE_DIR/tokenizer/taggedFileToCONLL.py |
    tee $2/parser_o.txt
else
    $FA_PIPELINE_DIR/tokenizer/farsilemm.py \
        $FA_PIPELINE_DIR/tokenizer/lemmatizationDict.txt < $INPUT_FILE |
    $FA_PIPELINE_DIR/tokenizer/tokenize |
    $FA_PIPELINE_DIR/tokenizer/addDot.py |
    $FA_PIPELINE_DIR/tokenizer/tag |
    $FA_PIPELINE_DIR/tokenizer/taggedFileToCONLL.py > $OUTPUT_FILE
fi
