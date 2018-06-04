# Abductive Discourse Processing Pipeline

## Scripts

- `NLPipeline_MULT_stdinout.py`
- `NLPipeline_MULT_stdinout_CM.py`

These are the abductive discourse processing pipeline scripts, with and
without conceptual metaphor identification.

Which use:
- `extract_CMs_from_hypotheses.py`
  Generate the conceptual metaphor file (*.cm)
- `IntParser2Henry.py`
  Convert logical forms of sentences into Henry input, adding nonmerge
  constraints. This is used for Spanish, Farsi, and Russian;
  `Boxer2Henry.py` is used for English.


## Description

Multilingual (English, Spanish, Farsi, Russian) abductive discourse
processing pipeline.

* `NLPipeline_MULT_stdinout_CM.py` – Run tokenizer, lemmatizer, parser,
logical form converter, abductive reasoner, proof graph generator,
conceptual metaphor output

```
Usage: NLPipeline_MULT_stdinout_CM.py [-h] [--lang LANG] [--input INPUT]
                                   [--outputdir OUTPUTDIR] [--parse] [--henry]
                                   [--kb KB] [--kbcompiled KBCOMPILED]
                                   [--graph GRAPH] [--CMoutput]
optional arguments:
  -h, --help            show this help message and exit
  --lang LANG           Input language: EN, ES, FA, RU.
  --input INPUT         Input file: plain text (possibly with text ids),
                        observation file, henry file.
  --outputdir OUTPUTDIR
                        Output directory. If input file defined, then default
                        is input file dir. Otherwise its TMP_DIR.
  --parse               Tokenize and parse text, produce logical forms,
                        convert to observations.
  --henry               Process observations with Henry.
  --kb KB               Path to noncompiled knowledge base.
  --kbcompiled KBCOMPILED
                        Path to compiled knowledge base.
  --graph GRAPH         ID of text/sentence to visualize. Possible value:
                        allN, where N is number of sentences to visualize.
  --CMoutput            Conceptual metaphor output.
```

## Components

* [English semantic parsing pipeline](https://github.com/isi-metaphor/Metaphor-ADP/tree/master/pipelines/English)
* [Spanish semantic parsing pipeline](https://github.com/isi-metaphor/Metaphor-ADP/tree/master/pipelines/Spanish)
* [Russian semantic parsing pipeline](https://github.com/isi-metaphor/Metaphor-ADP/tree/master/pipelines/Russian)
* [Farsi semantic parsing pipeline](https://github.com/isi-metaphor/Metaphor-ADP/tree/master/pipelines/Farsi)
* [Henry abductive reasoner](https://github.com/naoya-i/henry-n700)
