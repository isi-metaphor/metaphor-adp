To generate axioms from annotated data:

Parse the examples:

    ./parse-examples -l EN -u 'http://colo-vm19.isi.edu:8080' \
    en.2014-11-10.dev.tsv > en.2014-11-10.dev-new.parse

This output should match en.2014-11-10.dev.parse.

Then generate axioms from these parses:

    ./from-examples en.2014-11-10.dev-new.parse | sort | uniq \
    > en.2014-11-10.dev-new.kb

The resulting file of axioms should match en.2014-11-10.dev.kb.

To use these axioms, compile with Henry:

    henry -m compile_kb -o English_compiled_KB.da en.2014-11-10.dev-new.kb

These axioms learned from examples can be combined with manually
enumerated knowledge, such as that in the Metaphor-ADP/KBs directories by
specifying multiple source files to Henry, e.g.,

    henry -m compile_kb -o English_compiled_KB.da en.2014-11-10.dev-new.kb\
    Metaphor-ADP/KBs/English/en-sources.txt
