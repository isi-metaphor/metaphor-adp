# Abduction-based Discourse Processing System

This is a repository of the ISI metaphor project team, in which we store
all the resources and tools constituting our natural language
understanding system based on abductive reasoning, implemented for four
languages:

- English
- Spanish
- Russian
- Farsi

The system is largely based on ideas summarized in [[Hobbs, 1993]](http://www.isi.edu/~hobbs/interp-abduct-ai.pdf).

Our abductive Natural Language Understanding pipeline is shown below.

![Fig.](https://raw.github.com/isi-metaphor/Metaphor-ADP/master/docs/pics/pipeline-pic.png)

Text fragments are given as input to the pipeline. The text fragments are
parsed. For Russian and Spanish tagging, we use
[TreeTagger](http://www.ims.uni-stuttgart.de/projekte/corplex/TreeTagger/).
For Farsi tagging, we use the [Stanford NLP
tagger](http://nlp.stanford.edu/software/tagger.shtml). For parsing, we
use the dependency parser [Malt](http://www.maltparser.org) for Spanish,
Russian, and Farsi. For English, the whole processing is performed by
the [Boxer](http://svn.ask.it.usyd.edu.au/trac/candc/wiki/boxer)
semantic parser.

The parses are input to the module converting them into logical forms. A
logical form (LF) is a conjunction of propositions, which have
generalized eventuality arguments that can be used for showing
relationships among the propositions. We use logical representations of
natural language texts as described in [[Hobbs,
1995]](http://www.isi.edu/~hobbs/op-acl85.pdf). For Spanish, Russian,
and Farsi, we have developed logical form converters. For English, we
use the LF converter built in the Boxer semantic parser.

Logical forms and a knowledge base are input to the [abductive
reasoner](http://code.google.com/p/henry-n700/) based on Integer Linear
Programming [[Inoue et al.,
2012]](http://www.cl.ecei.tohoku.ac.jp/~naoya-i/resources/jelia2012_paper.pdf).
The reasoner produces flat first order logic interpretations in the
textual format and proof graphs in the PDF format.

More details about each component can be found
[here](https://github.com/isi-metaphor/Metaphor-ADP/blob/master/pipelines/README.md).


## Installation and running

- Clone Metaphor-ADP repository

```
git clone https://github.com/isi-metaphor/Metaphor-ADP
```

- Install external packages and software; see instructions [here](https://github.com/isi-metaphor/Metaphor-ADP/tree/master/installation)

- Run the system; see instructions [here](https://github.com/isi-metaphor/Metaphor-ADP/blob/master/pipelines/common/README.md)


## System Requirements

- Linux or macOS
- at least 4 cores CPU
- at least 8GB RAM


## Related Publications

- Jonathan Gordon, Jerry R. Hobbs, Jonathan May, Michael Mohler,
  Fabrizio Morbini, Bryan Rink, Marc Tomlinson, and Suzanne Wertheim.
  2015. [A Corpus of Rich Metaphor
  Annotation](https://doi.org/10.6084/m9.figshare.6179210.v2).
  In *Proceedings of the Third Workshop on Metaphor in NLP*.
  [Data](https://doi.org/10.6084/m9.figshare.6179210.v2)

- Jonathan Gordon, Jerry R. Hobbs, Jonathan May, and Fabrizio Morbini.
  2015. [High-Precision Abductive Mapping of Multilingual
  Metaphors](https://doi.org/10.3115/v1/W15-1406). In
  Proceedings of the Third Workshop on Metaphor in NLP.

- Naoya Inoue, Ekaterina Ovchinnikova, Kentaro Inui, and Jerry R.
  Hobbs. 2014. Weighted Abduction for Discourse Processing Based on
  Integer Linear Programming. In Sukthankar et al. (eds.): *Plan,
  Activity, and Intent Recognition*, pp. 33-55.

- Ekaterina Ovchinnikova, Ross Israel, Suzanne Wertheim, Vladimir Zaytsev,
  Niloofar Montazeri, and Jerry R. Hobbs. 2014. [Abductive Inference for
  Interpretation of Metaphors](https://doi.org/10.3115/v1/W14-2305). In
  *Proceedings of the ACL 2014 Workshop on Metaphor in NLP*. Baltimore,
  MD.

- Ekaterina Ovchinnikova, Niloofar Montazeri, Theodore Alexandrov, Jerry
  R. Hobbs, Michael C. McCord, and Rutu Mulkar-Mehta. 2013.
  [Abductive Reasoning with a Large Knowledge Base for Discourse
  Processing](http://ovchinnikova.me/papers/IWCS-bookchap-final3.pdf). In
  Hunt, H., Bos, J. and Pulman, S. (eds.): *Computing Meaning*, vol. 4,
  pp. 104-24.

- Ekaterina Ovchinnikova. 2012. [*Integration of World Knowledge for Natural
  Language Understanding*](https://www.springer.com/us/book/9789491216527).
  Atlantis Press, Springer.

- Naoya Inoue, Ekaterina Ovchinnikova, Kentaro Inui, and Jerry R. Hobbs.
  2012. [Coreference Resolution with ILP-based Weighted
  Abduction](http://www.aclweb.org/anthology/C12-1079). In *Proceedings
  of COLING*, pp.1291-1308.

- Ekaterina Ovchinnikova, Niloofar Montazeri, Theodore Alexandrov, Jerry
  R. Hobbs, Michael C. McCord, and Rutu Mulkar-Mehta. 2011. [Abductive
  Reasoning with a Large Knowledge Base for Discourse
  Processing](http://www.aclweb.org/anthology/W/W11/W11-0124.pdf). In
  *Proceedings the 9th International Conference on Computational Semantics
  (IWCS'11)*, pp. 225-234.
