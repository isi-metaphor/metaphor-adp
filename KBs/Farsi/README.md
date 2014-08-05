# Farsi Knowledge Bases
Jonathan Gordon, 2014-08-04

This directory contains the knowledge bases of Farsi (Persian) axioms for
metaphor recognition and interpretation.

fa-sources.txt and fa-targets.txt are the latest revision of the
manually authored axioms.

fa-wordnet.txt gives synonymy axioms from Open MultiWordNet that expand
the coverage of other KBs.

To recompile the KB (Farsi_compiled_KB.da), run:

    henry -m compile_kb -o Farsi_compiled_KB.da \
    fa-sources.txt fa-targets.txt fa-wordnet.txt \
    ../common/economic_inequality_ontology.txt
