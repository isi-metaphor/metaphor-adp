# README: KBs/Scripts/from-examples
Jonathan Gordon, 2014-08-14

These are scripts to generate axioms from the example sentences in the
development set. To use:

- Set 'language' in parse-examples
- ./parse-examples EN.dev > en.dev.parsed
- ./from-examples en.dev.parsed > en-examples.kb
