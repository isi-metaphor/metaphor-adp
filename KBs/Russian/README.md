# Russian Knowledge Bases
Jonathan Gordon, 2014-08-14

This directory contains the knowledge bases of Russian axioms for
metaphor recognition and interpretation.

ru-sources.txt and ru-targets.txt are the latest revision of the
manually authored axioms.

ru-examples.txt are axioms learned automatically from the example
sentences in the development set.

WordNet synonymy axioms are not currently available for Russian.

To compiled the current highest-precision KB (Russian_compiled_KB.da),
run:

    henry -m compile_kb -o Russian_compiled_KB.da \
    ru-examples.txt
