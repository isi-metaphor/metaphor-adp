# Russian Knowledge Bases
Jonathan Gordon, 2014-08-04

This directory contains the knowledge bases of Russian axioms for
metaphor recognition and interpretation.

ru-sources.txt and ru-targets.txt are the latest revision of the
manually authored axioms.

WordNet synonymy axioms are not currently available for Russian.

To compiled the current KB:

    henry -m compile_kb -o Russian_compiled_KB.da \
    ru-sources.txt ru-targets.txt \
    ../common/economic_inequality_ontology.txt
