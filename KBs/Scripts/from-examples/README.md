# README: KBs/Scripts/from-examples
Jonathan Gordon, 2018-07-25

These are scripts to generate axioms from the example sentences in the
development set.

Parse the examples:

    ./parse-examples -l EN -u 'http://localhost:8000' \
        en.2014-11-10.dev.tsv > en.dev.parse

Then generate axioms from these parses:

    ./from-examples en.dev.parse | sort | uniq > en-examples.txt

To use these axioms, compile with Henry:

    henry -m compile_kb -o English_compiled_KB.da en-examples.txt

These axioms learned from examples can be combined with manually
enumerated knowledge, such as that in the `Metaphor-ADP/KBs` directories
by passing multiple source files to Henry.
