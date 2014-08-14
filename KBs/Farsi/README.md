# Farsi Knowledge Bases
Jonathan Gordon, 2014-08-14

This directory contains the knowledge bases of Farsi (Persian) axioms for
metaphor recognition and interpretation.

fa-sources.txt and fa-targets.txt are the latest revision of the
manually authored axioms.

fa-examples.txt are axioms learned automatically from the example
sentences in the development set.

fa-wordnet.txt gives synonymy axioms from Open MultiWordNet that expand
the coverage of other KBs. (This is out of date and should not currently
be used.)

To recompile the current highest-precision KB (Farsi_compiled_KB.da),
run:

    henry -m compile_kb -o Farsi_compiled_KB.da \
    fa-examples.txt
