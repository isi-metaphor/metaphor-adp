# Russian Knowledge Bases
Jonathan Gordon, 2014-12-22

This directory contains the knowledge bases of Russian axioms for
metaphor recognition and interpretation.

ru-sources.txt and ru-targets.txt are the latest revision of the
manually authored axioms.

ru-examples.txt are axioms learned automatically from the example
sentences in the development set.

To compiled the current highest-precision KB (Russian_compiled_KB.da),
run:

    henry -m compile_kb -o Russian_compiled_KB.da \
    ru-examples.txt
