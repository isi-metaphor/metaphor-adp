# English Semantic Parsing Pipeline

English semantic parsing pipeline based on the Boxer semantic parser.

- `Boxer_pipeline.py`: run tokenizer, CCG parser, and Boxer sematic parser

```
usage: Boxer_pipeline.py [-h] [--input INPUT] [--outputdir OUTPUTDIR] [--tok]
                         [--fname FNAME]

Boxer pipeline.

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         The input file to be processed.
  --outputdir OUTPUTDIR The output directory.
  --tok                 Tokenize input text.
  --fname FNAME         File prefix for intermediate output.

```

Alternative: `run_English.sh` runs the full processing pipeline for
tokenizing and parsing English text:

```
./run_English.sh [<path to input file> [<path to output dir]]
```
