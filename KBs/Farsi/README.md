# Farsi Knowledge Bases
Jonathan Gordon, 2018-06-04

This directory contains the knowledge bases of Farsi (Persian) axioms for
metaphor recognition and interpretation.

`fa-sources.txt` and `fa-targets.txt` are the latest revision of the
manually authored axioms.

`fa-examples.txt` are axioms learned automatically from the example
sentences in the development set.

To recompile the current highest-precision KB (`Farsi_compiled_KB.da`),
run:

    henry -m compile_kb -o Farsi_compiled_KB.da \
        fa-examples.txt
