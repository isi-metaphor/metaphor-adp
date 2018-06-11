#!/bin/bash

# The variable $METAPHOR_DIR should point to the root of the
# Metaphor-ADP directory.
# export METAPHOR_DIR=~/code/Metaphor-ADP

# Usage:
#   ./preproc [input] [output]
# or
#   ./preproc [input]
# or
#   < [input] ./pre-parser
# [input] and [output] should be absolute paths.

PLATFORM=$(uname -s | tr '[:upper:]' '[:lower:]')

ES_PIPELINE_DIR=$METAPHOR_DIR/pipelines/Spanish

TREE_TAGGER_BIN=$METAPHOR_DIR/external-tools/tree-tagger-3.2/$PLATFORM/bin
TREE_TAGGER_CMD=$METAPHOR_DIR/external-tools/tree-tagger-3.2/cmd
TREE_TAGGER_LIB=$METAPHOR_DIR/external-tools/tree-tagger-3.2/$PLATFORM/lib

MALT_IFORMAT=$ES_PIPELINE_DIR/tokenizer/to_malt.py

OPTIONS="-token -lemma -sgml -quiet"

TOKENIZER_BIN=$ES_PIPELINE_DIR/tokenizer/nltk_stokenizer.py

MWL=$TREE_TAGGER_CMD/mwl-lookup.perl
TAGGER=$TREE_TAGGER_BIN/tree-tagger
PARFILE=$TREE_TAGGER_LIB/spanish-utf8.par
MWLFILE=$TREE_TAGGER_LIB/spanish-mwls-utf8

if [ -d "$2" ]; then
    $TOKENIZER_BIN --sentid 1 --normquotes 1 < "${1:-/dev/stdin}" |
        tee $2/tokenizer_o.txt |
        $MWL -f $MWLFILE |
        $TAGGER $OPTIONS $PARFILE |
        tee $2/tagger_o.txt |
        $MALT_IFORMAT
else
    $TOKENIZER_BIN --sentid 1 --normquotes 1 < "${1:-/dev/stdin}" |
        $MWL -f $MWLFILE |
        $TAGGER $OPTIONS $PARFILE |
        $MALT_IFORMAT
fi
