#!/bin/bash

# Parse Russian

TAGGED_INPUT_FILE="${1:-/dev/stdin}"
PARSED_FILE_NAME="${2:-/dev/stdout}"

MALT_PARSER_DIR=$METAPHOR_DIR/external-tools/malt-1.5

cat $TAGGED_INPUT_FILE | \
java -Xmx16g -cp $MALT_PARSER_DIR/dist/malt/malt.jar:$MALT_PARSER_DIR \
     MaltParserWrap -c rus-test.mco -m parse -w $MALT_PARSER_DIR \
     -lfi parser-ru.log > $PARSED_FILE_NAME
