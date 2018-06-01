#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import re
import optparse

# I/O
usage = "usage: %prog [options] <input_file>"
parser = optparse.OptionParser(usage=usage)
parser.add_option("-i", "--input", dest="input",
                  action="store", help="read from FILE", metavar="FILE")
(options, args) = parser.parse_args()

LineNumber = 1
metaTagFlag = True


def malter(LINE_OBJECT):
    """Formats lines for MaltParser in CoNLL format."""
    global LineNumber
    global metaTagNumber

    if len(LINE_OBJECT) == 1:
        return '\t'.join(['1', LINE_OBJECT[0], LINE_OBJECT[0], 'f', 'f', '0',
                          '0', 'ROOT', '-'])

    # Lemma
    Token = LINE_OBJECT[0].strip().split()
    tokenString = "_".join(Token)
    # Use twice: POS and CPOS
    tPOS = LINE_OBJECT[1].strip()
    aPOS = replace_tag(tPOS, LINE_OBJECT[2].strip())
    Lemma = determineLemma(LINE_OBJECT[2].strip(), tokenString)
    malt_line = '\t'.join(['1', tokenString, Lemma, aPOS, aPOS, '0', '0',
                           'ROOT', '-'])

    """
    if metaTagNumber == True:
        LineNumber = 1
        #metaTagNumber = False
    else:
        LineNumber += 1
    """
    return malt_line


def determineLemma(original, token):
    if original == "<unknown>":
        lemma = token
    elif optional_lemma.search(original):
        lemma = original.split("|")[0]
    else:
        lemma = original.replace("~", "_")
    if lemma == "":
        lemma = token
    return lemma


def reform(infile):
    malt_lines = []
    for line in infile:
        line = line.rstrip()
        listed = line.split("\t")
        try:
            if re.search("%%", line):
                pass
            else:
                malt = malter(listed)
                malt_lines.append(malt)
        except IndexError:
            malt_lines.append(line)
    return malt_lines
    file_object.close()


def replace_tag(tag, lemma):
    if treeAdj.match(tag):
        return "a"
    elif treeConj.match(tag):
        return "c"
    elif treeDet.match(tag):
        return "d"
    elif treePunct.match(tag):
        return "f"
    elif treeInter.match(tag):
        return "i"
    elif treeNoun.match(tag):
        return "n"
    elif treePro.match(tag):
        return "p"
    elif treeAdv.match(tag):
        return "r"
    elif treePrep.match(tag):
        return "s"
    elif treeVerb.match(tag):
        return "v"
    # elif treeDate.match(tag):
    #     return "w"
    elif treeNum.match(tag):
        return "z"
    elif tag == "CODE":
        if lemma == "@card@":
            return "z"
        else:
            return "n"
    else:
        return tag


treeAdj = re.compile("ADJ")
treeConj = re.compile("CC.*|CQUE|CSUBX")
treeDet = re.compile("ART|DM|QU")
treePunct = re.compile("BACKSLASH|CM|COLON|DASH|DOTS|LP|PERCT|QT|" +
                       "RP|SEMICOLON|SLASH|SYM")
# ^also FS for full stop - but need this to sepatate sents
treeInter = re.compile("ITJN|PNC")
treeNoun = re.compile("NMEA|NMON|NC|NP|ALF*|ACRNM|PE|UMMX")
treePro = re.compile("INT|PPC|PPO|PPX|REL|SE")
treeAdv = re.compile("CSUBF|ADV|NEG")
treePrep = re.compile("PREP|CSUBI|PAL|PDEL|PREP/DEL")
treeVerb = re.compile("^V.*")
# treeDate = re.compile("")
treeNum = re.compile("CARD|FO|ORD")
optional_lemma = re.compile(r"\w\|\w")

sentID = re.compile("<{{{.*}}}!!!>")


def main():
    global LineNumber
    global metaTagFlag
    lines = open(options.input, "r") if options.input else sys.stdin
    printable = reform(lines)
    for line in printable:
        line_list = line.split('\t')
        try:
            token = line_list[1]
            pos = line_list[3]
            if pos == 'fs' or (pos == 'FS' and token != "¿") or \
               sentID.search(token):
                line_list[3] = "f"
                line_list[4] = "f"
                if metaTagFlag is False:
                    line_list[0] = str(LineNumber)
                    LineNumber = 1
                sys.stdout.write("\t".join(line_list)+'\n\n')
            else:
                metaTagFlag = False
                if token == "¿":
                    line_list[3] = "f"
                    line_list[4] = "f"
                line_list[0] = str(LineNumber)
                LineNumber += 1
                sys.stdout.write("\t".join(line_list)+'\n')
        except IndexError:
            sys.stdout.write(line)
    if pos != 'fs' and pos != 'FS':
        sys.stdout.write("\n")
    sys.stdout.write("END\n")


if __name__ == "__main__":
    main()
