#!/bin/bash

PLATFORM=$(uname -s | tr '[:upper:]' '[:lower:]')

RU_PIPELINE_DIR=$METAPHOR_DIR/pipelines/Russian

TREE_TAGGER_BIN=$METAPHOR_DIR/external-tools/tree-tagger-3.2/$PLATFORM/bin
TREE_TAGGER_OPT="-lemma -token -sgml -quiet"
TAGGER_BIN=$TREE_TAGGER_BIN/tree-tagger

TOKENIZER_BIN=$RU_PIPELINE_DIR/tokenizer/nltk_rtokenizer.py
TAGGER_PAR=$RU_PIPELINE_DIR/tokenizer/russian.par
LEMMATIZER_BIN=$RU_PIPELINE_DIR/tokenizer/lemmatiser.pl
MALT_IFORMAT=$RU_PIPELINE_DIR/tokenizer/make-malt.pl

CURRENT_DIR=$(pwd)
cd $RU_PIPELINE_DIR/tokenizer

if [ -d "$2" ]; then
    python2.7 $TOKENIZER_BIN --sentid 1 --normquotes 1 \
        --wptokenizer 0 < "${1:-/dev/stdin}" |
    tee $2/tokenizer_o.txt |
    $TAGGER_BIN $TREE_TAGGER_OPT $TAGGER_PAR |
    tee $2/tagger_o.txt |
    $LEMMATIZER_BIN -l $RU_PIPELINE_DIR/tokenizer/msd-ru-lemma.lex.gz \
        -p $RU_PIPELINE_DIR/tokenizer/wform2011.ptn1 \
        -c $RU_PIPELINE_DIR/cstlemma |
    tee $2/lemmatizer_o.txt |
    $MALT_IFORMAT > /dev/stdout
else
    python2.7 $TOKENIZER_BIN --sentid 1 --normquotes 1 \
        --wptokenizer 0 < "${1:-/dev/stdin}" |
    $TAGGER_BIN $TREE_TAGGER_OPT $TAGGER_PAR |
    $LEMMATIZER_BIN -l $RU_PIPELINE_DIR/tokenizer/msd-ru-lemma.lex.gz \
        -p $RU_PIPELINE_DIR/tokenizer/wform2011.ptn1 \
        -c $RU_PIPELINE_DIR/tokenizer/cstlemma |
    $MALT_IFORMAT > "${2:-/dev/stdout}"
fi

cd $CURRENT_DIR
