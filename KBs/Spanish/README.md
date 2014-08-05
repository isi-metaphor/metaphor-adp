# Spanish Knowledge Bases
Jonathan Gordon, 2014-08-04

This directory contains the knowledge bases of Spanish axioms for
metaphor recognition and interpretation.

es-sources.txt and es-targets.txt are the latest revision of the
manually authored axioms.

es-wordnet.txt gives synonymy axioms from WordNet that expand the
coverage of other KBs.

To recompile the KB (Spanish_compiled_KB.da), run:

    henry -m compile_kb -o Spanish_compiled_KB.da \
    es-sources.txt es-targets.txt es-wordnet.txt \
    ../common/economic_inequality_ontology.txt
