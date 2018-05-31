#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Multilingual abductive discourse processing pipeline
# Ekaterina Ovchinnikova <katya@isi.edu>, 2012
# Jonathan Gordon <jgordon@isi.edu>, 2014

# External tools used:
# - English NLP pipeline (Metaphor-ADP/pipelines/English)
# - Spanish NLP pipeline (Metaphor-ADP/pipelines/Spanish)
# - Farsi NLP pipeline (Metaphor-ADP/pipelines/Farsi)
# - Russian NLP pipeline (Metaphor-ADP/pipelines/Russian)
# - Henry abductive reasoner (https://github.com/naoya-i/henry-n700)

# This script requires the environment variables METAPHOR_DIR, HENRY_DIR,
# and TMP_DIR to be set.

# To see options, run
#   ./NLPipeline_MULT_stdinout.py -h

import sys
import os
import argparse
import re

from subprocess import Popen, PIPE, STDOUT


METAPHOR_DIR = os.environ['METAPHOR_DIR']
HENRY_DIR = os.environ['HENRY_DIR']
TMP_DIR = os.environ['TMP_DIR']

BOXER2HENRY = "%s/pipelines/English/Boxer2Henry.py" % METAPHOR_DIR
PARSER2HENRY = "%s/pipelines/common/IntParser2Henry.py" % METAPHOR_DIR

EN_PIPELINE = "%s/pipelines/English/Boxer_pipeline.py" % METAPHOR_DIR
ES_PIPELINE = "%s/pipelines/Spanish/run_spanish.sh" % METAPHOR_DIR
FA_PIPELINE = "%s/pipelines/Farsi/LF_Pipeline" % METAPHOR_DIR
RU_PIPELINE = "%s/pipelines/Russian/run_russian.sh" % METAPHOR_DIR


def generate_proofgraph(id, fname, graph_input, henry_output, outputdir):
    viz = 'python2.7 ' + HENRY_DIR + '/tools/proofgraph.py' + graph_input + \
        ' --graph ' + id + ' | dot -T pdf > ' + \
        os.path.join(outputdir, fname + '_' + id + '.pdf')
    graphical_proc = Popen(viz, shell=True, stdin=PIPE, stdout=PIPE,
                           stderr=None, close_fds=True)

    # Use Henry output as input
    if henry_output:
        graphical_proc.communicate(input=henry_output)
    # Use input file as input
    else:
        graphical_proc.communicate()


def main():
    parser = argparse.ArgumentParser(description='Multilingual abductive '
                                     'discourse processing pipeline.')
    parser.add_argument('--lang', default='EN',
                        help='Input language: EN, ES, FA, RU.')
    parser.add_argument('--input', default=None,
                        help='Input file: plain text (possibly with text '
                        'IDs), observation file, Henry file.')
    parser.add_argument('--outputdir', default=None,
                        help='Output directory. If input file defined, then '
                        'default is input file dir. Otherwise it\'s TMP_DIR.')
    parser.add_argument('--parse', action='store_true', default=False,
                        help='Tokenize and parse text, produce logical forms, '
                        'convert to observations.')
    parser.add_argument('--henry', action='store_true', default=False,
                        help='Process observations with Henry.')
    parser.add_argument('--kb', default=None,
                        help='Path to noncompiled knowledge base.')
    parser.add_argument('--kbcompiled', default=None,
                        help='Path to compiled knowledge base.')
    parser.add_argument('--graph', default=None,
                        help='ID of text/sentence to visualize. Possible '
                        'value: allN, where N is number of sentences to '
                        'visualize.')
    parser.add_argument('--textid', action='store_true', default=False,
                        help='Meta text IDs.')

    pa = parser.parse_args()

    # Set file name prefix for output files.
    fname = os.path.splitext(os.path.basename(pa.input))[0] \
        if pa.input else 'output'

    # Set output directory.
    if pa.outputdir:
        outputdir = pa.outputdir
    elif pa.input:
        outputdir = os.path.dirname(pa.input)
    else:
        outputdir = TMP_DIR

    # Set operating system.
    if sys.platform.lower().startswith('linux'):
        OS = 'linux'
    elif sys.platform.lower().startswith('darwin'):
        OS = 'darwin'
    else:
        print 'Unknown operating system: ' + sys.platform + '\n'
        return

    PARSER_PIPELINE = ''
    LF2HENRY = ''
    NONMERGE_OPTIONS = ' --nonmerge sameid freqpred'

    # Parser pipeline
    if pa.parse:
        # Parsing and generating logical forms
        if pa.lang == 'EN':
            PARSER_PIPELINE = 'python2.7 ' + EN_PIPELINE + \
                ' --tok --outputdir ' + outputdir + ' --fname ' + fname
            if pa.input:
                PARSER_PIPELINE += ' --input ' + pa.input
            LF2HENRY = 'python2.7 ' + BOXER2HENRY
        elif pa.lang == 'ES':
            PARSER_PIPELINE = ES_PIPELINE
            if pa.input:
                PARSER_PIPELINE += ' ' + pa.input + ' ' + outputdir
            LF2HENRY = 'python2.7 ' + PARSER2HENRY
        elif pa.lang == 'FA':
            PARSER_PIPELINE = FA_PIPELINE
            if pa.input:
                PARSER_PIPELINE += ' ' + pa.input + ' ' + outputdir
            LF2HENRY = 'python2.7 ' + PARSER2HENRY
        elif pa.lang == 'RU':
            PARSER_PIPELINE = RU_PIPELINE
            if pa.input:
                PARSER_PIPELINE += ' ' + pa.input + ' ' + outputdir
            LF2HENRY = 'python2.7 ' + PARSER2HENRY

        parser_proc = Popen(PARSER_PIPELINE, shell=True, stdin=PIPE,
                            stdout=PIPE, stderr=None, close_fds=True)
        # If there is an input file, it is passed as a parameter to the
        # parsing pipeline.
        if pa.input:
            parser_output = parser_proc.communicate()[0]
        # If there is no input file, parsing pipeline reads from stdin.
        else:
            parser_output = parser_proc.communicate(input=sys.stdin.read())[0]

        # Save logical forms output by the parsing pipeline.
        with open(os.path.join(outputdir, fname + ".par"), "w") as f_par:
            f_par.write(parser_output)

        # Add LF2PARSER options
        if pa.textid:
            LF2HENRY += ' --textid'
        LF2HENRY += NONMERGE_OPTIONS

        # Convert logical forms to Henry input (observations).
        lf2h_proc = Popen(LF2HENRY, shell=True, stdin=PIPE, stdout=PIPE,
                          stderr=None, close_fds=True)
        nl_output = lf2h_proc.communicate(input=parser_output)[0]

        # Save observations.
        with open(os.path.join(outputdir, fname + ".obs"), "w") as f_l2h:
            f_lf2h.write(nl_output)

    # Henry processing
    if pa.henry:
        henry_input = ''
        if pa.kb:
            henry_input += ' ' + pa.kb
            if pa.parse:
                henry_input += ' ' + os.path.join(outputdir, fname + ".obs")
            elif pa.input:
                henry_input += ' ' + pa.input
        elif (not pa.parse) and pa.input:
            henry_input += ' ' + pa.input

        if OS == 'linux':
            HENRY = HENRY_DIR + '/bin/henry -m infer' + henry_input + ' -e ' \
                + HENRY_DIR + '/models/h93.py -d 3 -t 4 ' + \
                '-O proofgraph,statistics -T 60'
        elif OS == 'darwin':
            HENRY = HENRY_DIR + '/bin/henry -m infer -d 3 -t 4 ' + \
                '-O proofgraph,statistics -T 60 -e  ' + HENRY_DIR + \
                '/models/h93.py ' + henry_input

        if pa.kbcompiled:
            HENRY += ' -b ' + pa.kbcompiled

        henry_proc = Popen(HENRY, shell=True, stdin=PIPE, stdout=PIPE,
                           stderr=None, close_fds=True)

        # Noncompiled KB specified; it is used as input parameter along with
        # input observation file.
        if pa.kb:
            henry_output = henry_proc.communicate()[0]
        # Noncompiled KB not specified; parsing done; parsing output is used
        # as input.
        elif pa.parse:
            henry_output = henry_proc.communicate(input=nl_output)[0]
        # Noncompiled KB not specified; parsing not done; input file is used
        # as input parameter.
        elif pa.input:
            henry_output = henry_proc.communicate()[0]
        # Noncompiled KB not specified; parsing not done; input file not
        # specified; stdin used as input.
        else:
            henry_output = henry_proc.communicate(input=sys.stdin.readline())[0]

        # Save Henry output.
        with open(os.path.join(outputdir, fname + ".hyp"), "w") as f_henry:
            f_henry.write(henry_output)

    # Graphical output
    if pa.graph:
        # Parse possible 'allN' value
        matchObj = re.match(r'all(\d+)', pa.graph, re.M | re.I)

        # Henry inference done then use Henry output as input
        if not pa.henry and pa.input:
            graph_input = ' --input ' + pa.input
            henry_output = None
        else:
            graph_input = ''

        # Generate proofgraphs for all sentences/texts with IDs ranging
        # from 1 to N
        if matchObj:
            for i in range(1, int(matchObj.group(1)) + 1):
                generate_proofgraph(str(i), fname, graph_input,
                                    henry_output, outputdir)
        # Generate proofgraph for specific sentence/text
        else:
            generate_proofgraph(pa.graph, fname, graph_input,
                                henry_output, outputdir)


if __name__ == '__main__':
    main()
