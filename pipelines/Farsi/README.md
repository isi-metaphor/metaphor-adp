# Farsi Semantic Parsing Pipeline

A pipeline that tokenizes, POS tags, parses, and creates logical forms for
Farsi sentences.

## Running

Tokenizing, tagging, parsing and LF generation can be invoked individually
or altogether in a sequence using the LF_Pipeline module. It is also
possible to pipe the output of each module to the next module.

### Running the Pipeline

It is necessary to set the environmental variabe `METAPHOR_DIR` to the
root folder of the Metaphor-ADP project, e.g.:

```
export METAPHOR_DIR=/adp
```

Then run `LF_Pipeline`:

```
./LF_Pipeline [<input file>] [<output file>]
```

If input and/or output files are not given as arguments, they are read
from standard stream. Input file should be given as absolute paths.

Example commands:

```
./LF_Pipeline $METAPHOR_DIR/pipelines/Farsi/samples/sentence.txt \
    $METAPHOR_DIR/pipelines/Farsi/samples/lf.txt

< $METAPHOR_DIR/pipelines/Farsi/samples/sentence.txt \
    ./LF_Pipeline > $METAPHOR_DIR/pipelines/Farsi/samples/lf.txt
```

### Running Individual Modules

Again it is necessary to have `METAPHOR_DIR` point to the root folder of
the Metaphor-ADP project and use absolute paths for input files.

Running tokenizer:
```
./tokenize [<input file>] [<output file>]
```

Running tagger:
```
./tag [<input file>] [<output file>]
```

Running parser:
```
./parse [<input file>] [<output file>]
```

Running logical form generator:
```
./createLF [<input file>] [<output file>]
```

## External Tools & Resources

## Tokenizing

We use
[utf-8 tokenizer](http://corpus.leeds.ac.uk/tools/utf8-tokenize.pl))
by Helmut Schmid, IMS, University of Stuttgart


### Training Data

The tagger and the parser are trained on the
[Persian dependency treebank](http://dadegan.ir/en), which
has approx. 27,000 sentences. About 24,000 of the sentences are used for
training and the 3000 for testing.

Papers:

1. Rasooli, Mohammad Sadegh, et al. "A syntactic valency lexicon for
   Persian verbs: The first steps towards Persian dependency treebank." 5th
   Language & Technology Conference (LTC): Human Language Technologies as a
   Challenge for Computer Science and Linguistics. 2011.
2. Rasooli, Mohammad, Heshaam Faili, and Behrouz Minaei-Bidgoli.
   "Unsupervised identification of Persian compound verbs." Advances in
   Artificial Intelligence (2011): 394-406.


### Tagging

The POS tagger is
[Stanford's tagger](http://nlp.stanford.edu/software/tagger.shtml)

Papers:
1. Kristina Toutanova and Christopher D. Manning. 2000. Enriching the
   Knowledge Sources Used in a Maximum Entropy Part-of-Speech Tagger. In
   Proceedings of the Joint SIGDAT Conference on Empirical Methods in Natural
   Language Processing and Very Large Corpora (EMNLP/VLC-2000), pp. 63-70.
2. Kristina Toutanova, Dan Klein, Christopher Manning, and Yoram Singer.
   2003. Feature-Rich Part-of-Speech Tagging with a Cyclic Dependency
   Network. In Proceedings of HLT-NAACL 2003, pp. 252-259.

Here are POS tagging results:
- Total sentences right: 2050 (68.356119%); wrong: 949 (31.643881%).
- Total tags right: 47627 (97.281343%); wrong: 1331 (2.718657%).
- Unknown words right: 1800 (87.933561%); wrong: 247 (12.066439%).


## Parsing

[MaltParser 1.5](http://www.maltparser.org)

1. Nivre, J. (2003). An Efficient Algorithm for Projective Dependency
   Parsing. In Proceedings of the 8th International Workshop on
   Parsing Technologies (IWPT 03), Nancy, France, 23-25 April 2003,
   pp. 149-160.
2. Nivre, J., J. Hall and J. Nilsson (2004). Memory-Based Dependency
   Parsing. In Ng, H. T. and Riloff, E. (eds.) Proceedings of the Eighth
   Conference on Computational Natural Language Learning (CoNLL), May 6-7,
   2004, Boston, Massachusetts, pp. 49-56.

Here are the results we get for the parser:
- Labeled   attachment score: 36977 / 44377 * 100 = 83.32 %
- Unlabeled attachment score: 38799 / 44377 * 100 = 87.43 %
- Label accuracy score:       38099 / 44377 * 100 = 85.85 %
