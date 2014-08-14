# English Knowledge Bases
Jonathan Gordon, 2014-08-14

This directory contains the knowledge bases of English axioms for
metaphor recognition and interpretation.

en-sources.txt and en-targets.txt are the latest revision of the
manually authored axioms.

en-examples.txt are axioms learned automatically from the example
sentences in the development set.

en-wordnet.txt gives synonymy axioms from WordNet that expand the
coverage of other KBs. (This is out of date and should not currently be
used.)

To recompile the current highest-precision KB (English_compiled_KB.da),
run:

    henry -m compile_kb -o English_compiled_KB.da \
    en-examples.txt
