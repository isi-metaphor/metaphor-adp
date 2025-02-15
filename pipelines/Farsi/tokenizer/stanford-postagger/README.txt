Stanford POS Tagger, v3.1.3 - 2012-07-09
Copyright (c) 2002-2012 The Board of Trustees of
The Leland Stanford Junior University. All Rights Reserved.

Original tagger author: Kristina Toutanova
Code contributions: Christopher Manning, Dan Klein, William Morgan,
Huihsin Tseng, Anna Rafferty, John Bauer
Major rewrite for version 2.0 by Michel Galley.
Current release prepared by: John Bauer

This package contains a Maximum Entropy part of speech tagger.

A Part-Of-Speech Tagger (POS Tagger) is a piece of software that reads
text in some language and assigns parts of speech to each word (and
other tokens), such as noun, verb, adjective, etc. Generally
computational applications use more fine-grained POS tags like
'noun-plural'. This software is a Java implementation of the log-linear
part-of-speech (POS) taggers described in:

Kristina Toutanova and Christopher D. Manning. 2000. Enriching the
Knowledge Sources Used in a Maximum Entropy Part-of-Speech
Tagger. Proceedings of the Joint SIGDAT Conference on Empirical Methods
in Natural Language Processing and Very Large Corpora (EMNLP/VLC-2000),
Hong Kong.

Kristina Toutanova, Dan Klein, Christopher Manning, and Yoram
Singer. 2003. Feature-Rich Part-of-Speech Tagging with a Cyclic
Dependency Network. In Proceedings of HLT-NAACL 2003 pages 252-259.

The system requires Java 1.6+ to be installed. About 60 MB of memory is
required to run a trained tagger, depending on the OS, tagging model
chosen, etc.  (i.e., you may need to give to java an option like java
-mx120m). Plenty of memory is needed to train a tagger. It depends on
the complexity of the model but at least 1GB is recommended (java
-mx1g). Two trained tagger models for English are included with the
tagger, along with some caseless versions, and we provide models for
some other languages. The tagger can be retrained on other languages
based on POS-annotated training text.

If you really want to use this software under Java 1.4, look into RetroWeaver:

  http://retroweaver.sourceforge.net/


QUICKSTART
-----------------------------------------------

The Stanford POS Tagger is designed to be used from the command line or
programmatically via its API.  

There is a GUI interface, but it is for
demonstration purposes only; most features of the tagger can only be
accessed via the command line. To run the demonstration GUI you should
be able to use any of the following 3 methods:

1)
java -mx200m -classpath stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTaggerGUI models/left3words-wsj-0-18.tagger

2)
Providing your system gives java enough memory by default, you can also
run it by either double-clicking the stanford-postagger.jar file, or
giving the command: 
    java -jar stanford-postagger.jar

3) Running the appropriate script for your operating system:
    stanford-postagger-gui.bat
    ./stanford-postagger-gui.sh

To run the tagger from the command line, you can start with the provided
script appropriate for you operating system:
    ./stanford-postagger.sh models/left3words-wsj-0-18.tagger sample-input.txt
    stanford-postagger models\left3words-wsj-0-18.tagger sample-input.txt
The output should match what is found in sample-output.txt

The tagger has three modes: tagging, training, and testing.  Tagging
allows you to use a pretrained model (two English models are included)
to assign part of speech tags to unlabeled text.  Training allows you to
save a new model based on a set of tagged data that you provide.
Testing allows you to see how well a tagger performs by tagging labeled
data and evaluating the results against the correct tags.

Many options are available for training, tagging, and testing.  These
options can be set using a properties file.  To start, you can generate a
default properties file by:

java -classpath stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -genprops > myPropsFile.prop

This will create the file myPropsFile.prop with descriptions of each
option for the tagger and the default values for these options
specified.  Any properties you can specify in a properties file can be
specified on the command line or vice versa.  For further information,
please consult the Javadocs (start with the entry for MaxentTagger,
which includes a table of all options which may be set to configure the
tagger and descriptions of those options).


To tag a file using the pre-trained bidirectional model
=======================================================

java -mx300m -classpath stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/bidirectional-distsim-wsj-0-18.tagger -textFile sample-input.txt > sample-tagged.txt

Tagged output will be printed to standard out, which you can redirect as above.

To train a simple model
=======================

java -classpath stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -prop propertiesFile -model modelFile -trainFile trainingFile

To test a model
===============

java -classpath stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -prop propertiesFile -model modelFile -testFile testFile



CONTENTS
-----------------------------------------------
README.txt

  This file.

LICENSE.txt

  Stanford POS Tagger is licensed under the GNU General Public License (v2+).

stanford-postagger.jar
stanford-postagger-YYYY-MM-DD.jar

  This is a JAR file containing all the Stanford classes necessary to
  run the Stanford POS Tagger.  The two jar files are identical.  You can use
  either the one with a version (date) indication or without, as you prefer.

src

  A directory containing the Java 1.5 source code for the Stanford POS
  Tagger distribution.

build.xml, Makefile

  Files for building the distribution (with ant and make, respectively)

models

  A directory containing trained POS taggers; the taggers end in ".tagger"
  and the props file used to make the taggers end in ".props". The
  ".props" files cannot be directly used on your own machine as they use
  paths on the Stanford NLP machines, but they may serve as examples for
  your own properties files. Included in the full version are other
  English taggers, a German tagger, an Arabic tagger, and a Chinese
  tagger. If you chose to download the smaller version of the tagger,
  you have only two English taggers (left3words is faster but slightly
  less accurate than bidirectional-distsim) - feel free to download any
  other taggers you need from the POS tagger website. More information
  about the models can be found in the README-Models.txt file in this
  directory. 

sample-input.txt

  A sample text file that you can tag to demonstrate the tagger.

sample-output.txt

  Tagged output of the tagger (using the left3words model)

stanford-postagger-gui.sh
stanford-postagger-gui.bat

  Scripts for invoking the GUI demonstration version of the tagger.

stanford-postagger.sh
stanford-postagger.bat

  Scripts for running the command-line version of the tagger.

javadoc

  Javadocs for the distribution.  In particular, look at the javadocs
  for the class edu.stanford.nlp.tagger.maxent.MaxentTagger.

TaggerDemo.java

  A sample file for how to call the tagger in your own program.  You
  should be able to compile and run it with:

  javac -cp stanford-postagger.jar TaggerDemo.java
  java -cp ".:stanford-postagger.jar" TaggerDemo models/left3words-wsj-0-18.tagger sample-input.txt

  (If you are on Windows, you need to replace the ":" with a ";" in the
  -cp argument, and should use a "\" in place of the "/" in the filename....)

THANKS
-----------------------------------------------

Thanks to the members of the Stanford Natural Language Processing Lab
for great collaborative work on Java libraries for natural language
processing.

  http://nlp.stanford.edu/javanlp/

CHANGES
-----------------------------------------------

2012-07-09    3.1.3     Minor bug fixes 

2012-05-22    3.1.2     Updated for compatibility with other releases

2012-03-09    3.1.1     Caseless models added

2012-01-06    3.1.0     French tagger added, tagging speed improved

2011-09-14    3.0.4     Updated for compatibility with other releases

2011-06-15    3.0.3     Updated for compatibility with other releases

2011-05-15    3.0.2     Can read training files in TSV format

2011-04-17    3.0.1     Improved German and Arabic models
                        Compatible with other Stanford releases

2010-05-21    3.0.0     Re-entrant

LICENSE
-----------------------------------------------

 Stanford POS Tagger
 Copyright (c) 2002-2010 The Board of Trustees of
 The Leland Stanford Junior University. All Rights Reserved.

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; either version 2
 of the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

 For more information, bug reports, fixes, contact:
    Christopher Manning
    Dept of Computer Science, Gates 1A
    Stanford CA 94305-9010
    USA
    Support/Questions: java-nlp-user@lists.stanford.edu
	Licensing: java-nlp-support@lists.stanford.edu
    http://www-nlp.stanford.edu/software/tagger.shtml


CONTACT
-----------------------------------------------

For questions about the Stanford POS tagger, please feel free to contact
the Stanford JavaNLP user community at the mailing list
java-nlp-user@lists.stanford.edu.  You need to be a member of this
mailing list to be able to post to it.  Join the list either by emailing
java-nlp-user-join@lists.stanford.edu (leave the subject and message
body empty) or by using the web interface at:

       https://mailman.stanford.edu/mailman/listinfo/java-nlp-user

This is the best list to post to in order to ask questions, make
announcements, or for discussion among Stanford JavaNLP tool users. We
provide assistance on a best-effort basis. You can also look at the list
archives via https://mailman.stanford.edu/pipermail/java-nlp-user/. For
licensing questions, please see the tagger webpage or contact Stanford
JavaNLP at java-nlp-support@lists.stanford.edu.

