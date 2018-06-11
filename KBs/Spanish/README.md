# Spanish Knowledge Bases
Jonathan Gordon, 2018-06-04

This directory contains the knowledge bases of Spanish axioms for
metaphor recognition and interpretation.

`es-sources.txt` and `es-targets.txt` are the latest revision of the
manually authored axioms.

`es-examples.txt` are axioms learned automatically from the example
sentences in the development set.

To recompile the current highest-precision KB (`Spanish_compiled_KB.da`),
run:

    henry -m compile_kb -o Spanish_compiled_KB.da \
        es-sources.txt es-targets.txt es-examples.txt
