# Farsi Knowledge Bases
Jonathan Gordon, 2014-07-23

This directory contains the knowledge bases of Farsi (Persian) axioms for
metaphor recognition and interpretation.

To recompile the KB (Farsi_compiled_KB.da), run:

    henry -m compile_kb -o Farsi_compiled_KB.da \
    fa-sources.txt fa-targets.txt \
    ../common/economic_inequality_ontology.txt
