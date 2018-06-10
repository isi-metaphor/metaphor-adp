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
#   ./NLPipeline_MULT_stdinout_CM.py -h

import sys
import os
import argparse
import re

from subprocess import Popen, PIPE, STDOUT

import extract_CMs_from_hypotheses
from extract_CMs_from_hypotheses import *


METAPHOR_DIR = os.environ['METAPHOR_DIR']
HENRY_DIR = os.environ['HENRY_DIR']
TMP_DIR = os.environ.get('TMP_DIR', '/tmp')

BOXER2HENRY = METAPHOR_DIR + "/pipelines/English/parse-to-lf/Boxer2Henry.py"
PARSER2HENRY = METAPHOR_DIR + "/pipelines/common/IntParser2Henry.py"

EN_PIPELINE = METAPHOR_DIR + "/pipelines/English/run-en.sh"
ES_PIPELINE = METAPHOR_DIR + "/pipelines/Spanish/run-es.sh"
FA_PIPELINE = METAPHOR_DIR + "/pipelines/Farsi/run-fa.sh"
RU_PIPELINE = METAPHOR_DIR + "/pipelines/Russian/run-ru.sh"

# Compiled knowledge bases
EN_KBPATH = "%s/KBs/English/English_compiled_KB.da" % METAPHOR_DIR
ES_KBPATH = "%s/KBs/Spanish/Spanish_compiled_KB.da" % METAPHOR_DIR
FA_KBPATH = "%s/KBs/Farsi/Farsi_compiled_KB.da" % METAPHOR_DIR
RU_KBPATH = "%s/KBs/Russian/Russian_compiled_KB.da" % METAPHOR_DIR


def extract_hypotheses(inputString):
    output_struct = []
    hypothesis_found = False
    p = re.compile('<result-inference target="(.+)"')
    target = ''
    hypothesis = ''
    unification = False
    explanation = False

    for line in inputString.splitlines():
        output_struct_item = {}
        match_obj = p.match(line)

        if match_obj:
            target = match_obj.group(1)

        elif line.startswith('<hypothesis'):
            hypothesis_found = True

        elif line.startswith('</hypothesis>'):
            hypothesis_found = False

        elif hypothesis_found:
            hypothesis = line

        elif line.startswith('<unification'):
            unification = True

        elif line.startswith('<explanation'):
            explanation = True

        elif line.startswith('</result-inference>'):
            output_struct_item = extract_CM_mapping(target, hypothesis, '',
                                                    '', None)
            # print json.dumps(hypothesis, ensure_ascii=False)
            # print json.dumps(output_struct_item, ensure_ascii=False,
            #                  indent=4)

            output_struct.append(output_struct_item)
            target = ""
            hypothesis = ""

    # print json.dumps(output_struct, ensure_ascii=False)
    return output_struct


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
    parser.add_argument('--CMoutput', action='store_true', default=False,
                        help='Conceptual metaphor output.')

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
            PARSER_PIPELINE = EN_PIPELINE
            LF2HENRY = BOXER2HENRY
            KBPATH = EN_KBPATH
        elif pa.lang == 'ES':
            PARSER_PIPELINE = ES_PIPELINE
            LF2HENRY = PARSER2HENRY
            KBPATH = ES_KBPATH
        elif pa.lang == 'FA':
            PARSER_PIPELINE = FA_PIPELINE
            LF2HENRY = PARSER2HENRY
            KBPATH = FA_KBPATH
        elif pa.lang == 'RU':
            PARSER_PIPELINE = RU_PIPELINE
            LF2HENRY = PARSER2HENRY
            KBPATH = RU_KBPATH

        if pa.input:
            PARSER_PIPELINE += ' ' + pa.input + ' ' + outputdir

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
        LF2HENRY += NONMERGE_OPTIONS

        # Convert logical forms to henry input (observations)
        lf2h_proc = Popen(LF2HENRY, shell=True, stdin=PIPE, stdout=PIPE,
                          stderr=None, close_fds=True)
        nl_output = lf2h_proc.communicate(input=parser_output)[0]

        # Save observations
        with open(os.path.join(outputdir, fname + ".obs"), "w") as f_lf2h:
            f_lf2h.write(nl_output)

    # Henry processing
    if pa.henry:
        henry_input = ''
        if pa.kb:
            henry_input += ' ' + pa.kb
            if pa.parse:
                henry_input += ' ' + os.path.join(outputdir,
                                                  fname + ".obs")
            elif pa.input:
                henry_input += ' ' + pa.input
        elif (not pa.parse) and pa.input:
            henry_input += ' ' + pa.input

        if OS == 'linux':
            HENRY = HENRY_DIR + '/bin/henry -m infer' + henry_input + ' -e ' \
                    + HENRY_DIR + '/models/h93.py -d 5 -t 4 ' + \
                    '-O proofgraph,statistics -T 60'
        elif OS == 'darwin':
            HENRY = HENRY_DIR + '/bin/henry -m infer -d 3 -t 4 ' + \
                    '-O proofgraph,statistics -T 60 -e  ' + HENRY_DIR + \
                    '/models/h93.py ' + henry_input

        if pa.kbcompiled:
            HENRY += ' -b ' + pa.kbcompiled

        henry_proc = Popen(HENRY, shell=True, stdin=PIPE, stdout=PIPE,
                           stderr=None, close_fds=True)

        # Noncompiled kb specified; it is used as input parameter along with
        # input observation file
        if pa.kb:
            henry_output = henry_proc.communicate()[0]
        # Noncompiled KB not specified; parsing done; parsing output is used
        # as input
        elif pa.parse:
            henry_output = henry_proc.communicate(input=nl_output)[0]
        # Noncompiled KB not specified; parsing not done; input file is used
        # as input parameter
        elif pa.input:
            henry_output = henry_proc.communicate()[0]
        # Noncompiled KB not specified; parsing not done; input file not
        # specified; stdin used as input
        else:
            henry_output = henry_proc.communicate(input=sys.stdin.readline())[0]

        # Save Henry output
        with open(os.path.join(outputdir, fname + ".hyp"), "w") as f_henry:
            f_henry.write(henry_output)

    # Graphical output
    if pa.graph:
        # Parse possible 'allN' value
        matchObj = re.match(r'all(\d+)', pa.graph, re.M | re.I)

        # Henry inference done then use henry output as input
        if not pa.henry and pa.input:
            graph_input = ' --input ' + pa.input
            henry_output = None
        else:
            graph_input = ''

        # Generate proofgraphs for all sentences/texts with ids ranging
        # from 1 to N
        if matchObj:
            for i in range(1, int(matchObj.group(1)) + 1):
                generate_proofgraph(str(i), fname, graph_input, henry_output,
                                    outputdir)
        # Generate proofgraph for specific sentence/text
        else:
            generate_proofgraph(pa.graph, fname, graph_input, henry_output,
                                outputdir)

    # Conceptual metaphor output
    if pa.CMoutput:
        if not pa.henry and pa.input:
            with open(pa.input, "r") as fh:
                henry_output = fh.read()
        hypotheses = extract_hypotheses(henry_output)
        with open(os.path.join(outputdir, fname + ".cm"), "w") as f_cm:
            f_cm.write(json.dumps(hypotheses, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
