#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Contributors:
# - Ekaterina Ovchinnikova <katya@isi.edu>, 2012
# - Jonathan Gordon <jgordon@isi.edu>, 2014

# English LF converter, processing Boxer[1] output and returning Henry[2]
# input logical forms with nonmerge constraints.
#  [1]: http://svn.ask.it.usyd.edu.au/trac/candc/wiki/boxer
#  [2]: https://github.com/naoya-i/henry-n700

# In order to see options, run
#   ./Boxer2Henry.py -h

# The converter only runs on the output produced by the subversion of Boxer,
# using the '--semantics tacitus' option.

import argparse
import sys
import re
import os
import json
from collections import defaultdict

id2args = defaultdict(list)
id2prop = defaultdict(list)
pred2farg = defaultdict(list)


# Add word IDs mapped to first args of corresponding propositions.
def add_id2prop(id_str, arg):
    ids = id_str.split(',')
    for id in ids:
        id2prop[id].append(arg)


# Generate nonmerge constraints, so that propositions with the same word IDs
# could not be unified.
def generate_sameID_nm():
    nm = ''
    for id in id2prop.keys():
        if len(id2prop[id]) > 1:
            nm += ' (!='
            for arg in id2prop[id]:
                nm += ' ' + arg
            nm += ')'
    return nm


def generate_samename_nm():
    nm = ''
    for id in id2args.keys():
        if len(id2args[id]) > 1:
            arity = None
            for args in id2args[id]:
                l = len(args)
                if arity is None:
                    arity = l
                elif arity != l:
                    arity = None
            if arity is not None:
                neqSets = apply(zip, id2args[id])
                for neq in neqSets:
                    nm += ' (!='
                    for arg in neq:
                        nm += ' ' + arg
                    nm += ')'
    return nm


# Generate nonmerge constraints, so that frequent predicates could not be
# unified.
def generate_freqPred_nm():
    nm = ''
    for pred in pred2farg.keys():
        if len(pred2farg[pred]) > 1:
            nm += ' (!='
            for arg in pred2farg[pred]:
                nm += ' ' + arg
            nm += ')'
    return nm


# English preposition list
prepositions = set([
    'abaft', 'aboard', 'about', 'above', 'absent', 'across', 'afore',
    'after', 'against', 'along', 'alongside', 'amid', 'amidst', 'among',
    'amongst', 'around', 'as', 'aside', 'astride', 'at', 'athwart', 'atop',
    'barring', 'before', 'behind', 'below', 'beneath', 'beside', 'besides',
    'between', 'betwixt', 'beyond', 'but', 'by', 'concerning', 'despite',
    'during', 'except', 'excluding', 'failing', 'following', 'for', 'from',
    'given', 'in', 'including', 'inside', 'into', 'lest', 'like', 'minus',
    'modulo', 'near', 'next', 'of', 'off', 'on', 'onto', 'opposite', 'out',
    'outside', 'over', 'pace', 'past', 'plus', 'pro', 'qua', 'regarding',
    'round', 'sans', 'save', 'since', 'than', 'through', 'throughout',
    'till', 'times', 'to', 'toward', 'towards', 'under', 'underneath',
    'unlike', 'until', 'up', 'upon', 'versus', 'via', 'vice', 'with',
    'within', 'without', 'worth'])


# Check if a predicate is a preposition
def check_prep(pred):
    if pred in prepositions:
        return pred + '-in'
    return pred


def main():
    parser = argparse.ArgumentParser(description='Boxer2Henry converter.')
    parser.add_argument('--input', help='Input file', default=None)
    parser.add_argument('--output', help='Output file', default=None)
    parser.add_argument('--nonmerge', help='Add nonmerge constraints. '
                        'Values: samepred (args of a pred cannot be merged), '
                        'sameid (first arg of preds with same id cannot be '
                        'merged), samename (ALL args of preds with same name '
                        'cannot be merged), freqpred (args of frequent preds '
                        'cannot be merged)',
                        nargs='+', default=[])
    parser.add_argument('--cost', help='Input observation costs.', type=int,
                        default=1)

    pa = parser.parse_args()

    # Set nonmerge options
    samepred = 'samepred' in pa.nonmerge
    sameid = 'sameid' in pa.nonmerge
    samename = 'samename' in pa.nonmerge
    freqpred = 'freqpred' in pa.nonmerge
    # Read input
    lines = open(pa.input, 'r') if pa.input else sys.stdin

    # Set output file
    ofile = open(pa.output, 'w') if pa.output else sys.stdout

    output_str = ''
    sent_id = ''
    prop_id_counter = 0

    # Pattern for parsing: [word id list]:pred_name(args)
    id_prop_args_pattern = re.compile(r'\[([^\]]*)\]:([^\[\(]+)(\((.+)\))?')
    # Pattern for parsing: pred_name_base-postfix
    prop_name_pattern = re.compile('(.+)-([nvarp])$')
    # Pattern for parsing: id(sentence_id,..)
    sent_id_pattern = re.compile(r'id\((.+),.+\)')

    for line in lines:
        # Ignore commented strings
        if line.startswith('%'):
            continue
        # Define sentence id
        elif line.startswith('id('):
            SIDmatchObj = sent_id_pattern.match(line)
            if SIDmatchObj:
                sent_id = SIDmatchObj.group(1)
                ofile.write('(O (name ' + sent_id + ') (^')
            # else: print 'Strange sent id: ' + line
        # Ignore lemmatized word list
        elif line[0].isdigit():
            continue
        # Parse propositions
        elif line.strip():
            props = line.split(' & ')
            for prop in props:
                matchObj = id_prop_args_pattern.match(prop)
                if matchObj:
                    prop_id_counter += 1

                    # Define word id string
                    if matchObj.group(1):
                        word_id_str = matchObj.group(1)
                    else:
                        word_id_str = 'ID' + str(prop_id_counter)

                    # Normalize predicate name
                    prop_name = matchObj.group(2)
                    prop_name = re.sub(r"[\s_:./]+", '-', prop_name)

                    # Don't include predicates not containing letters or
                    # numbers.
                    if not bool(re.search('[a-z0-9]', prop_name,
                                          re.IGNORECASE)):
                        continue

                    propMatchObj = prop_name_pattern.match(prop_name)

                    # Set predicate name to which nonmerge constraints are
                    # applied
                    pred4nm = None
                    # Predicate name contains postfix
                    if propMatchObj:
                        pname = propMatchObj.group(1)
                        postfix = propMatchObj.group(2)
                        # Normalize postfixes
                        if postfix == 'n':  # Noun
                            postfix = 'nn'
                        elif postfix == 'v':  # Verb
                            postfix = 'vb'
                        elif postfix == 'a':  # Adjective
                            postfix = 'adj'
                        elif postfix == 'p':  # Preposition
                            postfix = 'in'
                            # It can be a subject
                            # to nonmerge constraints
                            pred4nm = pname+'-'+postfix
                        elif postfix == 'r':
                            postfix = 'rb'  # Adverb
                        prop_name = pname+'-'+postfix
                    else:
                        # Boxer sometimes does not mark prepositions.
                        # Fixing it.
                        prop_name = check_prep(prop_name)
                        # It can be a subject
                        # to nonmerge constraints
                        pred4nm = prop_name

                    # Set nonmerge constraints
                    nm = ''
                    # Proposition has arguments
                    if matchObj.group(4):
                        prop_args = matchObj.group(4)
                        prop_args = ' ' + prop_args.replace(',', ' ')
                        # Arguments of the same predicate cannot be unified
                        if samepred:
                            nm = ' (!=' + prop_args + ')'
                        if sameid or samename or freqpred:
                            args = prop_args.split()
                            # Add first arg of this proposition to dict id2prop
                            if sameid and matchObj.group(1):
                                add_id2prop(word_id_str, args[0])
                            if samename:
                                id2args[prop_name].append(args)
                            # Frequent predicates cannot be unified
                            if freqpred and pred4nm:
                                if args[0] not in pred2farg[pred4nm]:
                                    pred2farg[pred4nm].append(args[0])
                    # Proposition has no arguments
                    else:
                        prop_args = ''

                    # Write Henry representation of the proposition into output
                    ofile.write(' (' + prop_name + prop_args + ' :' +
                                str(pa.cost) + ':' + sent_id + '-' +
                                str(prop_id_counter) + ':[' + word_id_str +
                                '])')
                    # Write nonmerge constraints for 'samepred' into output
                    if samepred:
                        ofile.write(nm)
                # else: print 'Strange proposition: ' + prop + '\n'

            # Write nonmerge constraints for 'sameid' into output
            if sameid:
                ofile.write(generate_sameID_nm())
            if samename:
                ofile.write(generate_samename_nm())
            # Write nonmerge constraints for 'freqpred' into output
            if freqpred:
                ofile.write(generate_freqPred_nm())

            ofile.write('))\n')

            prop_id_counter = 0
            id2prop.clear()
            pred2farg.clear()

    ofile.close()


if __name__ == '__main__':
    main()
