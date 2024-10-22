# Spanish Semantic Parsing Pipeline

This file describes the Spanish semantic parsing pipeline. It has directions
for running the pipeline, as well as descriptions of the scripts, tools, and
resources used within the pipeline.


### Running the pipeline

```
./run-es.sh [<absolute path to input> [<absolute path to output>]]
```

To run the pipeline, call `run-es.sh` with the absolute path to the
input file as an argument. By default the system outputs the logical forms
of the sentences in the input file to stdout. The second (optional)
argument can be a file or a directory. If the optional argument is a file,
the system output will be redirected there. If it is a directory, the
intermediate files (tokenized, tagged, etc.) will be put into that
directory, and the final output will go to stdout.


### Scripts

- `tokenizer/to_malt.py`: Create conll style output. Input file should
  be output from treetagger. Outputs to stdout. To run:

```
./tokenizer/to_malt.py -i [input_file]
```

- `parse-to-lf/malt_to_prop.py`: Create logical form output. Input file
  should be output from MaltParser. Outputs to stdout. To run:

```
./parse-to-lf/malt_to_prop.py -i [input_file]
```

### External Tools & Resources

- Tokenization
 - `nltk_tokenize.py`: Written by Vladamir Zaytsev
   - uses nltk.tokenize (PunktSentenceTokenizer, WordPunctTokenizer, and
     TreebankWordTokenizer)
- POS Tagging
 - treetagger 3.2 (http://www.ims.uni-stuttgart.de/projekte/corplex/TreeTagger)
   - Spanish parameter file available from the same page
- Parsing
  - MaltParser 1.5 (http://www.maltparser.org/download.html)
     - training corpus: Ancora (http://clic.ub.edu/corpus/en)


**Preprocessing for Dependency Parsing**

NOTE: These steps do not need to be re-run.

1. Created conll-style file using instances from the Ancora corpus >
   ancora.malt

2. Made MaltParser model with maltparse1.5 using ancora.malt > ancora.model
