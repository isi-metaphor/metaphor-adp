# English Knowledge Bases
Jonathan Gordon, 2018-06-04

This directory contains the knowledge bases of English axioms for
metaphor recognition and interpretation.

`en-sources.txt` and `en-targets.txt` are the latest revision of the
manually authored axioms.

`en-examples.txt` are axioms learned automatically from the example
sentences in the development set.

To recompile the current highest-precision KB (`English_compiled_KB.da`),
run:

    henry -m compile_kb -o English_compiled_KB.da \
        en-examples.txt en-sources.txt en-targets.txt
