# English Knowledge Bases
Jonathan Gordon, 2014-08-04

This directory contains the knowledge bases of English axioms for
metaphor recognition and interpretation.

en-sources.txt and en-targets.txt are the latest revision of the
manually authored axioms.

en-wordnet.txt gives synonymy axioms from WordNet that expand the
coverage of other KBs.

To recompile the KB (English_compiled_KB.da), run:

    henry -m compile_kb -o English_compiled_KB.da \
    en-sources.txt en-targets.txt en-wordnet.txt \
    ../common/economic_inequality_ontology.txt
