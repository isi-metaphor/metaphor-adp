#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import optparse
import logging
import tempfile
import re


def to_sents(infile):
    words = []
    sentence = []
    full_sents = []
    all_words = []
    sent_count = 1
    id_flag = False
    for line in infile:
        line = line.strip().split("\t")
        if len(line) > 1:
            word_id = int(line[0])
            word_text = line[1]
            word_lemma = line[2]
            word_pos = line[3]
            word_head = int(line[6])
            word_rel = line[7]
            long_id = "%0*d" % (3, word_id)
            out_id = word_id
            if id_flag:
                newIter += IDiter
                out_id += newIter
            if date.match(word_lemma):
                word_lemma = word_text
            elif word_lemma == "<unknown>":
                word_lemma = word_text
            info = [
                long_id,
                word_text,
                word_lemma,
                word_pos,
                word_head,
                word_rel,
                word_id,
                sent_count
            ]
            sentence.append(word_text)
            words.append(info)
        elif sentence and words:
            full_sents.append(sentence)
            all_words.append(words)
            if sentence != ["."] and not sent_id_re.search(sentence[0]):
                sent_count += 1
            sentence = []
            words = []
            id_flag = False
    infile.close()
    return full_sents, all_words


def createLongID(word_id, token):
    if token.count("_") == 0:
        long_id = "%0*d" % (3, word_id)
        id_flag = False
    else:
        all_ids = []
        for _ in token.split("_"):
            single_id = "%0*d" % (3, word_id)
            word_id += 1
            all_ids.append(single_id)
        long_id = ",".join(all_ids)
        id_flag = True
    return long_id, id_flag, token.count("_")


def prop_to_dict(props, e_count, x_count, u_count):
    sent_dict = {}
    new_prop_sent = []
    question = False
    # Loop over stored list of words and save initial props
    for prop in props:
        new_prop = []
        ID = prop[0]
        token = prop[1]
        lemma = prop[2]
        pos = prop[3]
        head = prop[4]
        rel = prop[5]
        short_id = prop[6]
        sent_count = prop[7]
        if re.search(",", ID):
            multiple = ID.split(",")
            joined_ids = []
            for oneID in multiple:
                single_id = str(sent_count) + str(oneID)
                joined_ids.append(single_id)
            prop_id = ",".join(joined_ids)
        if not re.search(",", ID):
            prop_id = str(sent_count) + str(ID)
        if prop_tags.match(pos):
            args, tag, e_count, x_count, u_count, question = build_predicate(
                pos, e_count, x_count, u_count, lemma, question, token
            )
            entry = [token, lemma, pos, head, rel, short_id, args, tag, prop_id]
            new_prop.extend(entry)
            sent_dict[short_id] = entry
            new_prop_sent.append(new_prop)
        elif token == "¿":
            args = ["R", "R"]
            tag = ""
            entry = [token, lemma, pos, head, rel, short_id, args, tag, prop_id]
            new_prop.extend(entry)
            sent_dict[short_id] = entry
            new_prop_sent.append(new_prop)
            question = True
    return new_prop_sent, sent_dict, e_count, x_count, u_count


def replace_args(prop_sent, sent_dict):
    prop_dict = {}
    # Loop over propositions, fill in variables, and print
    position = 0
    for prop in prop_sent:
        # token = prop[0]
        lemma = prop[1]
        pos = prop[2]
        head = prop[3]
        rel = prop[4]
        word_id = prop[5]
        predicate = prop[6]
        tag = prop[7]
        prop_id = prop[8]
        if lemma in thing_pronouns and real_head(sent_dict, head):
            sent_dict = det_to_pr(head, word_id, sent_dict)
        if (((rel == "suj") or (rel == "spec"))
            and (tag != "NULL")
            and (real_head(sent_dict, head))
        ):
            sent_dict = insert_subj(head, word_id, sent_dict)
        if tag == "vb" and real_head(sent_dict, head) and rel in inheriting_vbs:
            sent_dict = inherit_args(head, word_id, sent_dict)
            sent_dict = insert_prep_v_comp(head, word_id, sent_dict)
        # Look for auxiliary verbs (passive)
        if ((tag == "vb" and rel == "v" and lemma in passives_list)
            and real_head(sent_dict, head)
            and int(sent_dict[head][8]) == int(sent_dict[word_id][8]) + 1
        ):
            sent_dict = process_passive(head, word_id, sent_dict)
        if (rel == "v" and lemma not in passives_list and tag != ""
            and real_head(sent_dict, head)
        ):
            sent_dict = process_aux(head, word_id, sent_dict)
        if rel in prep_rels and pos == "s" and real_head(sent_dict, head):
            sent_dict = insert_prepHead(head, word_id, sent_dict)
        if (rel == "sn" or rel == "spec") and predicate[-1] != "R" and \
           real_head(sent_dict, head):
            # or rel == "grup.nom" - taken from first if
            sent_dict = insert_sn(head, word_id, sent_dict)
        if rel == "grup.nom" and predicate[-1] != "R" and \
           real_head(sent_dict, head):
            sent_dict = insert_grup_nom(head, word_id, sent_dict)
        if ((rel in adjective_rels and (pos == "a")) or
                (lemma in quantifiers)) and real_head(sent_dict, head):
            sent_dict = insert_adj_head(head, word_id, sent_dict)
        if rel == "cc" and pos == "r" and lemma not in wh_words and \
           real_head(sent_dict, head):
            sent_dict = insert_cc(head, word_id, sent_dict)
        if rel == "cd" and predicate[-1] != "R" and real_head(sent_dict, head):
            sent_dict = insert_cd(head, word_id, sent_dict)
        if rel == "ci" and predicate[-1] != "R" and real_head(sent_dict, head):
            sent_dict = insert_ci(head, word_id, sent_dict)
        if rel == "atr" and real_head(sent_dict, head):
            sent_dict = inherit_atr(head, word_id, sent_dict)
        if rel == "morfema.pronominal" and pos == "p" and \
           real_head(sent_dict, head):
            sent_dict = insert_m_p(head, word_id, sent_dict)
        if tag == "in" and real_head(sent_dict, head):
            sent_dict = insert_prepHead(head, word_id, sent_dict)
        if tag == "card" and real_head(sent_dict, head):
            sent_dict = insert_adj_head(head, word_id, sent_dict)
        if rel == "cpred" and real_head(sent_dict, head):
            sent_dict = insert_cpred(head, word_id, sent_dict)
        if tag == "rb" and (rel == "spec" or rel == "mod") and \
           real_head(sent_dict, head):
            sent_dict = insert_rb_spec(head, word_id, sent_dict)
        if tag in pronoun_tags and (rel == "spec") and real_head(sent_dict, head):
            sent_dict = insert_pro_spec(head, word_id, sent_dict)
        if lemma in sub_con_list and real_head(sent_dict, head) and \
           len(predicate) > 2:
            sent_dict = insert_subCon_head(head, word_id, sent_dict)
        if lemma == "no" and real_head(sent_dict, head):
            sent_dict = handle_negation(head, word_id, sent_dict)
        if ((tag == "wh") or (tag == "whq")) and real_head(sent_dict, head):
            sent_dict = handle_wh(head, word_id, sent_dict)
    for _, prop in sent_dict.items():
        position += 1
        token = prop[0]
        lemma = prop[1]
        pos = prop[2]
        head = prop[3]
        rel = prop[4]
        word_id = prop[5]
        predicate = prop[6]
        tag = prop[7]
        prop_id = prop[8]
        if lemma == "@card@":
            lemma = ""
            tag = "card"
        if "R" in predicate:
            predicate = []
        if len(predicate) > 0:
            prop_dict[prop_id] = [prop_id, lemma.lower(), tag, predicate, head]
    return prop_dict


def real_head(sent_dict, head):
    return head in sent_dict


def handle_negation(head, word_id, sent_dict):
    sent_dict[word_id][7] = "not"
    if sent_dict[head][7] == "nn":
        sent_dict[word_id][6][1] = sent_dict[head][6][1]
    else:
        sent_dict[word_id][6][1] = sent_dict[head][6][0]
    return sent_dict


def handle_wh(head, word_id, sent_dict):
    """Handle all wh words"""
    extra = determine_wh_helper(sent_dict[word_id][1])
    sent_dict[word_id][1] = ""
    #first_key = int(re.split("[a-z]", str(sorted(sent_dict.items())[0][0]))[0])
    if sent_dict[head][7] == "vb" or sent_dict[head][7] == "in":
        head_head = sent_dict[head][3]
        if head_head == 0:
            sent_dict[head][6][2] = sent_dict[word_id][6][0]
            for _, values in sent_dict.items():
                # Look for the direct object with the same head as the
                # current word
                if (values[4] == "cd") and (values[3] == sent_dict[word_id][3]):
                    if values[7] == "vb":
                        sent_dict, _ = add_new_entry(
                            sent_dict, extra, sent_dict[word_id][6][1],
                            sent_dict[values[5]][6][0], sent_dict[word_id][8])
                    else:
                        sent_dict, new_key = add_new_entry(
                            sent_dict, extra, sent_dict[word_id][6][1],
                            sent_dict[head][6][0], sent_dict[word_id][8])
                    return sent_dict
            sent_dict, new_key = add_new_entry(
                sent_dict, extra, sent_dict[word_id][6][1],
                sent_dict[head][6][0], sent_dict[word_id][8])
            return sent_dict
        elif real_head(sent_dict, head_head):
            if sent_dict[head_head][7] == "vb" or \
               sent_dict[head_head][7] == "in":
                sent_dict[head_head][6][2] = sent_dict[word_id][6][0]
                sent_dict, new_key = add_new_entry(
                    sent_dict, extra, sent_dict[word_id][6][1],
                    sent_dict[head][6][0], sent_dict[word_id][8])
                return sent_dict
            elif (sent_dict[head_head][7] == "nn" and
                  real_head(sent_dict, head_head)):
                sent_dict[word_id][6].append("R")
                sent_dict, _ = add_new_entry(
                    sent_dict, extra, sent_dict[head_head][6][1],
                    sent_dict[head][6][0], sent_dict[word_id][8])
                return sent_dict
    return sent_dict


def det_to_pr(head, word_id, sent_dict):
    # head_head = sent_dict[head][3]
    if (sent_dict[word_id][1] in thing_pronouns
        and sent_dict[head][7] != "nn"
        and sent_dict[word_id][2] != "p"
    ):
        sent_dict[word_id][7] = "thing"
        sent_dict[word_id][2] = "p"
        last_e = int(find_last_e(sent_dict))
        newE = "e" + str(last_e + 1)
        newX = "x" + str(last_e + 1)
        sent_dict[word_id][6] = [newE, newX]
        last_key = int(re.split("[a-z]",
                                str(sorted(sent_dict.items())[-1][0]))[0])
        new_key = str(last_key) + "b"
        if new_key in sent_dict:
            new_key = str(last_key + 1) + "b"
        args = [newE, newX, "R"]
        prop_id = str(word_id) + "b"
        sent_dict[new_key] = ["", "", "", 0, "", 0, args, "", prop_id]
    return sent_dict


def find_last_e(sent_dict):
    for entry in reversed(sent_dict.items()):
        if re.search("e", entry[1][6][0]):
            return entry[1][6][0].split("e")[1]


def determine_wh_helper(lemma):
    if lemma == "dónde" or lemma == "donde":
        return "loc"
    if lemma == "cómo":
        return "manner"
    if lemma == "cuando" or lemma == "cuándo":
        return "time"
    if lemma == "por_qué":
        return "reason"
    if lemma == "quién" or lemma == "Quién":
        return "person"
    if lemma == "qué":
        return "thing"


def insert_subj(head, word_id, sent_dict):
    """Insert the subject of a verb as its first argument"""
    if sent_dict[word_id][4] == "spec" and \
       sent_dict[word_id][1] not in thing_pronouns:
        return sent_dict
    if sent_dict[word_id][4] == "spec" and sent_dict[head][7] != "vb":
        return sent_dict
    if sent_dict[head][7] == "vb" and sent_dict[word_id][2] in nominals:
        sent_dict[head][6][1] = sent_dict[word_id][6][1]
    elif (sent_dict[head][7] == "vb" and sent_dict[word_id][7] != "nn" and
          sent_dict[word_id][6][0] != "R"):
        sent_dict[head][6][1] = sent_dict[word_id][6][0]
    return sent_dict


def process_passive(head, word_id, sent_dict):
    """Remove the passive verb, and move the subject to the object place
    (second arg) in the head verb"""
    sent_dict[word_id][6].append("R")
    if noun_arg.search(sent_dict[head][6][1]) and sent_dict[head][7] == "vb":
        replace = sent_dict[head][6][2]
        sent_dict[head][6][2] = sent_dict[head][6][1]
        sent_dict[head][6][1] = replace
    return sent_dict


def process_aux(head, word_id, sent_dict):
    """Deal with verbs designated auxiliary by the parser"""
    if sent_dict[head][7] == "vb" and sent_dict[word_id][7] == "vb":
        sent_dict[word_id][6][2] = sent_dict[head][6][0]
    return sent_dict


def inherit_args(head, word_id, sent_dict):
    """Inherit the arguments of a head verb"""
    # If the current verb doesn't already have a subject
    if sent_dict[head][7] == "vb" and \
       not noun_arg.search(sent_dict[word_id][6][1]):
        previous = sent_dict[word_id][6][1]
        # Inherit the subject of the head
        sent_dict[word_id][6][1] = sent_dict[head][6][1]
        # hack to replace subject of linked verbs that occur previously,
        # since my code is slop
        if variable_arg.search(previous):
            for key, values in sent_dict.items():
                if values[6][1] == previous:
                    values[6][1] = sent_dict[head][6][1]
        # If the current word doesn't already have an object
        # taken out 2012-04-12 after talking with Katya
        # if not noun_arg.search(sent_dict[word_id][6][2]) and \
        #    noun_arg.search(sent_dict[head][6][2]):
        #     # inherit the object of the head
        #     sent_dict[word_id][6][2] = sent_dict[head][6][2]

    # Removed following block 2012-06-12; it seemed to hurt more than help.
    #
    # # if the current word has a clause deprel
    # if sent_dict[word_id][4] == "S":
    #     for key, values in sent_dict.items():
    #         # look for a conjunction with the same head as the current word
    #         if ((values[4] == "conj") and (values[3] == sent_dict[word_id][3])
    #                 and values[1] in and_or):
    #             conj_head = values[3]
    #             head_head = sent_dict[conj_head][3]
    #             if head_head != 0 and sent_dict[head_head][7]:
    #                 sent_dict = add_new_verb(
    #                     sent_dict, sent_dict[head_head][1],
    #                     sent_dict[head_head][7], sent_dict[head_head][6],
    #                     sent_dict[word_id][6][0], sent_dict[head_head][8],
    #                     sent_dict[head][8], word_id, head)
    #             # If the conjuction is "o" add an "or" proposition
    #             if (values[1] == "o"):
    #                 sent_dict, new_key = add_new_entry(
    #                     sent_dict, "or", sent_dict[head][6][0],
    #                     sent_dict[word_id][6][0], sent_dict[word_id][8])
    return sent_dict


def inherit_atr(head, word_id, sent_dict):
    if (sent_dict[head][7] == "vb"
        and not noun_arg.search(sent_dict[word_id][6][1])
    ):
        sent_dict[word_id][6][1] = sent_dict[head][6][1]
    if sent_dict[head][1] in copula_list:
        head_head = sent_dict[head][3]
        if sent_dict[word_id][7] == "adj":
            sent_dict[head][6].append("R")
        if sent_dict[word_id][7] == "nn":
            sent_dict[head][6].append("R")
            sent_dict, new_key = add_new_entry(
                sent_dict, "equal", sent_dict[head][6][1],
                sent_dict[word_id][6][1], sent_dict[word_id][8])
            sent_dict = replace_old_args(
                sent_dict, sent_dict[head][6][0], new_key)
        if sent_dict[word_id][7] == "vb":
            sent_dict[head][6].append("R")
            sent_dict, new_key = add_new_entry(
                sent_dict, "be", sent_dict[head][6][1],
                sent_dict[word_id][6][0], sent_dict[word_id][8])
    return sent_dict


def replace_old_args(sent_dict, headE, new_key):
    """If a copula has been removed and replaced with 'equal', replace any
    arguments based on the copula entity with the new equal entity """
    newE = sent_dict[new_key][6][0]
    for key, values in sent_dict.items():
        for i in range(len(values[6])):
            if values[6][i] == headE:
                values[6][i] = newE
    return sent_dict


def add_new_entry(sent_dict, tag, arg1, arg2, curr_id):
    """Add a new entry to the sentence dictionary for items that aren't
    explicit in the surface form"""
    last_key = int(re.split("[a-z]", str(sorted(sent_dict.items())[-1][0]))[0])
    last_e = int(find_last_e(sent_dict))
    newE = "e" + str(last_e + 1)
    if tag == "person":
        args = [newE, arg1]
    else:
        args = [newE, arg1, arg2]
    prop_id = curr_id + "b"
    new_key = str(last_key) + "b"
    if new_key in sent_dict:
        new_key = str(last_key + 1) + "b"
    sent_dict[new_key] = ["", "", "", 0, "", 0, args, tag, prop_id]
    return sent_dict, new_key


def add_new_verb(sent_dict, token, tag, hhargs, arg2, verb_id, curr_id, word_id,
                 head):
    """Add a new verb entry to the sentence dictionary for items that aren't
    explicit in the surface form"""
    last_key = int(re.split("[a-z]", str(sorted(sent_dict.items())[-1][0]))[0])
    last_e = int(find_last_e(sent_dict))
    # int(sorted(sent_dict.items())[-1][1][6][0].split("e")[1])
    newE = "e" + str(last_e+1)
    arg1 = hhargs[1]
    args = [newE, arg1, arg2]
    if tag == "vb":
        args.append(hhargs[3])
    new_key = str(last_key) + "b"
    newID = curr_id + "b"
    if new_key in sent_dict:
        new_key = str(last_key + 1) + "b"
    head_head = sent_dict[head][3]
    if sent_dict[head_head][1] == "ser":
        sent_dict, new_key = add_new_entry(
            sent_dict, "equal", arg1, arg2, sent_dict[word_id][8])
    else:
        sent_dict[new_key] = [
            token, token, "", verb_id, "", 0, args, tag, newID
        ]
    return sent_dict


def insert_cd(head, word_id, sent_dict):
    """Insert the direct object as the head verb's second argument"""
    if sent_dict[word_id][2] in nominals and sent_dict[head][7] == "vb":
        sent_dict[head][6][2] = sent_dict[word_id][6][1]
    if sent_dict[word_id][2] == "v" and sent_dict[head][7] == "vb" and \
       not noun_arg.search(sent_dict[head][6][2]) and \
       not noun_arg.search(sent_dict[word_id][6][1]):
        if not entity_arg.search(sent_dict[head][6][2]):
            sent_dict[head][6][2] = sent_dict[word_id][6][0]
        sent_dict[word_id][6][1] = sent_dict[head][6][1]
    return sent_dict


def insert_ci(head, word_id, sent_dict):
    """Insert the indirect object as the head verb's third argument"""
    if sent_dict[word_id][2] in nominals and sent_dict[head][7] == "vb":
        sent_dict[head][6][3] = sent_dict[word_id][6][1]
    if sent_dict[word_id][2] == "v" and sent_dict[head][7] == "vb":
        sent_dict[head][6][2] = sent_dict[word_id][6][0]
    return sent_dict


def insert_prepHead(head, word_id, sent_dict):
    """Insert the head of a preposition as its first argument"""
    if sent_dict[head][7] == "vb":
        if sent_dict[head][1] == "estar":
            sent_dict[word_id][6][1] = sent_dict[head][6][1]
            sent_dict[head][6][3] = "R"
        else:
            sent_dict[word_id][6][1] = sent_dict[head][6][0]
    if sent_dict[head][7] == "nn" and head < word_id:
        sent_dict[word_id][6][1] = sent_dict[head][6][1]
    if sent_dict[head][7] == "nn" and head > word_id:
        sent_dict[word_id][6][2] = sent_dict[head][6][1]
    if sent_dict[head][7] == "rb" or sent_dict[head][7] == "adj":
        sent_dict[word_id][6][1] = sent_dict[head][6][0]
    if sent_dict[head][7] == "in":
        sent_dict[word_id][6][1] = sent_dict[head][6][0]
    return sent_dict


def insert_subCon_head(head, word_id, sent_dict):
    """Find the head of a subconjugating conjunction"""
    if sent_dict[head][7] == "vb" and sent_dict[head][4] not in root_list:
        # (sent_dict[head][4] == "cd" or sent_dict[head][4] == "ao"):
        if sent_dict[head][1] == "estar":
            sent_dict[word_id][6][2] = sent_dict[head][6][1]
            sent_dict[head][6][3] = "R"
        else:
            sent_dict[word_id][6][2] = sent_dict[head][6][0]
        head_head = sent_dict[head][3]
        if real_head(sent_dict, head_head) and sent_dict[head_head][7] == "vb":
            sent_dict[word_id][6][1] = sent_dict[head_head][6][0]
        if (sent_dict[head][7] == "vb") and sent_dict[head][4] in root_list:
            sent_dict[word_id][6][1] = sent_dict[head][6][0]
    return sent_dict


def insert_sn(head, word_id, sent_dict):
    if sent_dict[word_id][4] == "spec" and \
       sent_dict[word_id][1] not in thing_pronouns:
        return sent_dict
    if sent_dict[word_id][4] == "spec" and sent_dict[head][7] != "in":
        return sent_dict
    if sent_dict[head][7] == "in" and sent_dict[word_id][7] == "nn":
        sent_dict[head][6][2] = sent_dict[word_id][6][1]
    if sent_dict[head][7] == "in" and sent_dict[word_id][7] != "nn":
        sent_dict[head][6][2] = sent_dict[word_id][6][0]
    elif sent_dict[head][7] == "vb":
        sent_dict[head][6][2] = sent_dict[word_id][6][1]
    elif (sent_dict[head][7] == "nn" and sent_dict[word_id][7] == "nn") and \
         (int(sent_dict[head][8]) == int(sent_dict[word_id][8]) + 1):
        if int(sent_dict[head][6][1].split("x")[1]) == \
           int(sent_dict[word_id][6][1].split("x")[1]) - 1:
            sent_dict[word_id][6][1] = sent_dict[head][6][1]
        for key, values in sent_dict.items():
            # Look for a conjunction with the same head as the current word
            if (values[4] == "conj") and (values[3] == sent_dict[word_id][3]):
                conj_head = values[3]
                head_head = sent_dict[conj_head][3]
                if real_head(sent_dict, head_head):  # != 0:
                    sent_dict = add_new_verb(
                        sent_dict, sent_dict[head_head][1],
                        sent_dict[head_head][7], sent_dict[head_head][6],
                        sent_dict[word_id][6][1], sent_dict[head_head][8],
                        sent_dict[head][8], word_id, head)
                # If the conjunction is "o" add an "or" proposition
                if values[1] == "o":
                    sent_dict, new_key = add_new_entry(
                        sent_dict, "or", sent_dict[head][6][0],
                        sent_dict[word_id][6][0], sent_dict[word_id][8])
    return sent_dict


def insert_grup_nom(head, word_id, sent_dict):
    if sent_dict[word_id][4] == "spec" and \
       sent_dict[word_id][1] not in thing_pronouns:
        return sent_dict
    if sent_dict[word_id][4] == "spec" and sent_dict[head][7] != "in":
        return sent_dict
    if sent_dict[head][7] == "in" and sent_dict[word_id][7] == "nn":
        sent_dict[head][6][2] = sent_dict[word_id][6][1]
    if sent_dict[head][7] == "in" and sent_dict[word_id][7] != "nn":
        sent_dict[head][6][2] = sent_dict[word_id][6][0]
    elif sent_dict[head][7] == "vb":
        sent_dict[head][6][2] = sent_dict[word_id][6][1]
    elif sent_dict[head][7] == "nn" and sent_dict[word_id][7] == "nn":
        for key, values in sent_dict.items():
            # Look for a conjunction with the same head as the current word
            if (values[4] == "conj") and (values[3] == sent_dict[word_id][3]):
                conj_head = values[3]
                head_head = sent_dict[conj_head][3]
                if real_head(sent_dict, head_head):  # head_head != 0:
                    sent_dict = add_new_verb(
                        sent_dict, sent_dict[head_head][1],
                        sent_dict[head_head][7], sent_dict[head_head][6],
                        sent_dict[word_id][6][1], sent_dict[head_head][8],
                        sent_dict[head][8], word_id, head)
                # If the conjuction is "o" add an "or" proposition
                if (values[1] == "o"):
                    sent_dict, new_key = add_new_entry(
                        sent_dict, "or", sent_dict[head][6][0],
                        sent_dict[word_id][6][0], sent_dict[word_id][8])
    return sent_dict


def insert_prep_v_comp(head, word_id, sent_dict):
    if sent_dict[head][7] == "in":
        sent_dict[head][6][2] = sent_dict[word_id][6][0]
    return sent_dict


def insert_cag(head, word_id, sent_dict):
    if sent_dict[head][7] == "vb":
        sent_dict[word_id][6][1] = sent_dict[head][6][0]
    return sent_dict


def insert_cpred(head, word_id, sent_dict):
    if sent_dict[head][7] == "vb" and sent_dict[word_id][7] != "nn":
        sent_dict[word_id][6][1] = sent_dict[head][6][0]
    return sent_dict


def insert_adj_head(head, word_id, sent_dict):
    # When the head is a noun, simply insert the first argument of the head
    if sent_dict[head][7] == "nn":
        sent_dict[word_id][6][1] = sent_dict[head][6][1]
    elif sent_dict[head][7] == "card":
        sent_dict[word_id][6][1] = sent_dict[head][6][0]
        # When the head is an adj, insert the first argument of the head of
        # the head
    elif sent_dict[head][2] == "a":
        sent_dict[word_id][6][1] = sent_dict[head][6][1]
    elif sent_dict[word_id][7] == "card":
        sent_dict[word_id][1] = ""
        sent_dict[word_id][8] = sent_dict[head][8] + "b"
    elif sent_dict[head][7] == "in":
        sent_dict[head][6][2] = sent_dict[word_id][6][0]
    else:
        sent_dict[word_id][6].append("R")
    return sent_dict


def insert_atr(head, word_id, sent_dict):
    if sent_dict[head][7] == "vb":
        sent_dict[head][6][2] = sent_dict[word_id][6][0]
    return sent_dict


def insert_rb_spec(head, word_id, sent_dict):
    sent_dict[word_id][6][1] = sent_dict[head][6][0]
    return sent_dict


def insert_pro_spec(head, word_id, sent_dict):
    if sent_dict[word_id][0] in possessive_pronouns:
        if sent_dict[head][7] == "nn":
            sent_dict, new_key = add_new_entry(
                sent_dict, "of-in", sent_dict[head][6][1],
                sent_dict[word_id][6][1], sent_dict[word_id][8])
        else:
            sent_dict, new_key = add_new_entry(
                sent_dict, "of-in", sent_dict[head][6][1],
                sent_dict[word_id][6][0], sent_dict[word_id][8])
    return sent_dict


def insert_cc(head, word_id, sent_dict):
    if sent_dict[head][7] == "vb":
        sent_dict[word_id][6][1] = sent_dict[head][6][0]
    return sent_dict


def insert_m_p(head, word_id, sent_dict):
    if sent_dict[head][7] == "vb":
        sent_dict[head][6][2] = sent_dict[head][6][1]
    return sent_dict


def build_predicate(pos, e_count, x_count, u_count, lemma, question, token):
    pred = []
    tag = ""
    if not re.search("\w", lemma):
        return ["R", "R"], "", e_count, x_count, u_count, question
    if lemma in wh_words:
        if not question:
            tag = "wh"
            pos = "wh"
        else:
            tag = "whq"
            pos = "whq"
            question = False
        pred.append("e" + str(e_count))
        e_count += 1
        pred.append("x" + str(x_count))
        x_count += 1
        return pred, tag, e_count, x_count, u_count, question
    if question:
        if lemma == "qué":
            tag = "whq"
            pos = "wh"
            pred.append("e" + str(e_count))
            e_count += 1
            pred.append("x" + str(x_count))
            x_count += 1
            question = False
            return pred, tag, e_count, x_count, u_count, question
    if verb_tag.match(pos):
        tag = "vb"
        pred.append("e" + str(e_count))
        e_count += 1
        pred.append("u" + str(u_count))
        u_count += 1
        pred.append("u" + str(u_count))
        u_count += 1
        pred.append("u" + str(u_count))
        u_count += 1
        return pred, tag, e_count, x_count, u_count, question
    if noun_tag.match(pos):
        tag = "nn"
        pred.append("e" + str(e_count))
        e_count += 1
        pred.append("x" + str(x_count))
        x_count += 1
        return pred, tag, e_count, x_count, u_count, question
    if pronoun_tag.match(pos):
        tag = pronoun_tag(lemma)
        if tag != "NULL":
            pred.append("e" + str(e_count))
            e_count += 1
            pred.append("x" + str(x_count))
            x_count += 1
        else:
            pred.append("u" + str(u_count))
            u_count += 1
            pred.append("u" + str(u_count))
            u_count += 1
            pred.append("R")
        return pred, tag, e_count, x_count, u_count, question
    if adjective_tag.match(pos):
        tag = "adj"
        pred.append("e" + str(e_count))
        e_count += 1
        pred.append("u" + str(u_count))
        u_count += 1
        return pred, tag, e_count, x_count, u_count, question
    if lemma in sub_con_list:
        tag = "in"
        pred.append("e" + str(e_count))
        e_count += 1
        pred.append("u" + str(u_count))
        u_count += 1
        pred.append("u" + str(u_count))
        u_count += 1
        return pred, tag, e_count, x_count, u_count, question
    if adverb_tag.match(pos):
        tag = "rb"
        pred.append("e" + str(e_count))
        e_count += 1
        pred.append("u" + str(u_count))
        u_count += 1
        return pred, tag, e_count, x_count, u_count, question
    if preposition_tag.match(pos):
        tag = "in"
        pred.append("e" + str(e_count))
        e_count += 1
        pred.append("u" + str(u_count))
        u_count += 1
        pred.append("u" + str(u_count))
        u_count += 1
        return pred, tag, e_count, x_count, u_count, question
    if card_tag.match(pos):
        tag = "card"
        if lemma == "@card@":
            lemma = token
        pred.append("e" + str(e_count))
        e_count += 1
        pred.append("u" + str(u_count))
        u_count += 1
        number = cardinal_number(lemma)
        pred.append(number)
        return pred, tag, e_count, x_count, u_count, question
    if det_tag.match(pos) and lemma in quantifiers:
        tag = "adj"
        pred.append("e" + str(e_count))
        e_count += 1
        pred.append("u" + str(u_count))
        u_count += 1
        return pred, tag, e_count, x_count, u_count, question
    if conj_tag.match(pos) and lemma not in no_prop_conjunctions:
        tag = "in"
        pred.append("e" + str(e_count))
        e_count += 1
        pred.append("u" + str(u_count))
        u_count += 1
        pred.append("u" + str(u_count))
        u_count += 1
        return pred, tag, e_count, x_count, u_count, question
    else:
        return ["R", "R"], "", e_count, x_count, u_count, question


def cardinal_number(lemma):
    if lemma in card_dict:
        lemma = card_dict[lemma]
    return lemma


def pronoun_tag(lemma):
    if lemma in he_pronouns:
        return "male"
    elif lemma in she_pronouns:
        return "female"
    elif lemma in person_pronouns:
        return "person"
    elif lemma in thing_pronouns:
        return "thing"
    # elif lemma in reflex_pronouns:
    #     return "reflexive"
    else:
        return "NULL"

    # if tagset == "ancora":


noun_tag = re.compile("^n$")
verb_tag = re.compile("^v$")
adjective_tag = re.compile("^a$")
adverb_tag = re.compile("^r$")
preposition_tag = re.compile("^s$")
pronoun_tag = re.compile("^p$")
card_tag = re.compile("^z$")
det_tag = re.compile("^d$")
conj_tag = re.compile("^c$")
prop_tags = re.compile("^(n|v|a|r|s|p|z|c|d)$")

card_dict = {}
card_dict["uno"] = "1"
card_dict["dos"] = "2"
card_dict["tres"] = "3"
card_dict["cuatro"] = "4"
card_dict["cinco"] = "5"
card_dict["seis"] = "6"
card_dict["siete"] = "7"
card_dict["ocho"] = "8"
card_dict["nueve"] = "9"
card_dict["diez"] = "10"

# "he" (ESP: el, lo, se) -> male(e1,x1)
# "she" (ESP: ella, la, sua) -> female(e1,x1)
# "it" -> neuter(e1,x1)
# "I" (ESP: yo, me) -> person(e1,x1)
# "we" (ESP: nosotros, nos) -> person(e1,x1) & typelt(e2,x1,s)
# "you"(ESP: usted, ustedes) -> person(e1,x1)
# "they"(ESP: ellos, ellas) -> thing(e1,x1) & typelt(e2,x1,s)

he_pronouns = set(["el", "lo"])

she_pronouns = set(["ella", "la"])

person_pronouns = set([
    "yo",
    "me",
    "nos",
    "nosotros",
    "usted",
    "ustedes",
    "mi",
    "mis",
    "su",
    "sus",
    "suyo",
    "nuestro",
    "nuestros",
    "nuestra",
    "nuestras",
    "quién",
    "tu",
    "tú",
    "quien",
    "tus",
    "mío"
])

thing_pronouns = set(["ellos", "ellas", "él", "este", "ese", "suyo", "aquel"])

reflex_pronouns = set(["se"])

possessive_pronouns = set([
    "mi",
    "mis",
    "tu",
    "tus",
    "su",
    "sus",
    "nuestro",
    "nuestros",
    "nuestra",
    "nuestras",
    "suyo",
    "mío"
])

pronoun_tags = set(["male", "female", "person", "thing"])

quantifiers = set(["todo", "poco", "otro"])

no_prop_conjunctions = set(["y", "o", "ni", "que"])

and_or = set(["y", "o"])

nominals = set(["n", "p"])

no_token_list = ["male", "female", "person", "thing", "reflexive"]
insert_list = ["equal", "card", "or", "be", "loc", "manner", "time", "nn",
              "reason", "of-in", "person"]
inheriting_vbs = ["S", "v"]
adjective_rels = ["s.a", "cn", "grup.a", "S"]
root_list = ["ROOT", "sentence"]
prep_rels = ["sp", "cn"]
wh_words = ["dónde", "cómo", "donde", "cuando", "cuándo", "por_qué", "quién",
           "Quién"]
sub_con_list = ["porque", "mientras_que", "siempre_que", "puesto_que",
              "ya_que", "pues"]

passives_list = ["haber", "deber", "tener", "estar"]
copula_list = ["ser", "estar"]

noun_arg = re.compile("x\d")
entity_arg = re.compile("e\d")
variable_arg = re.compile("u\d")

noun_pred = re.compile("nn\(e\d*,[ux]\d*\)")
pronoun_pred = re.compile("p\(e\d*,[ux]\d*\)")
date = re.compile("\[\?\?\:\?\?\/\?\?\/\d\d\d\d\:\?\?\.\?\?\]")
puncts = re.compile("[\.,\?\!{}()\[\]:;¿¡\"]")

sent_id_re = re.compile("{{{.*}}}!!!")


def next_meta(next_sentence_w1):
    if sent_id_re.search(next_sentence_w1):
        return True
    return False


def to_print(prop_dict, sent):
    prop_count = 0
    printable = ""
    for _, prop in sorted(prop_dict.items()):
        prop_count += 1
        if prop[1] == "" and prop[2] in insert_list:
            printable += (prop[2] + "(" + ",".join(prop[3]) + ")")
        elif prop[2] in no_token_list:
            printable += ("[" + prop[0] + "]" + ":" + prop[2] +
                          "(" + ",".join(prop[3]) + ")")
        elif prop[2] == "not" or prop[2] == "wh" or prop[2] == "whq":
            printable += ("[" + prop[0] + "]" + ":" + prop[2] +
                          "(" + ",".join(prop[3]) + ")")
        elif re.search("[a-z]", prop[0]):
            printable += ("[" + prop[4] + "]" + ":" + prop[1] + "-" +
                          prop[2] + "(" + ",".join(prop[3]) + ")")
        else:
            printable += ("[" + prop[0] + "]" + ":" + prop[1] + "-" +
                          prop[2] + "(" + ",".join(prop[3]) + ")")
        if prop_count < len(prop_dict.items()):
            printable += (" & ")
    return printable


def main():
    # I/O
    usage = "usage: %prog [options] <input_file>"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option(
        "-i",
        "--inFile",
        dest="input",
        action="store",
        help="Read from FILE",
        metavar="FILE"
    )
    options, _ = parser.parse_args()

    lines = open(options.input, "r") if options.input else sys.stdin

    _, logfile_name = tempfile.mkstemp(dir="/tmp/")
    logging.basicConfig(filename=logfile_name, level=logging.DEBUG)

    full_sents, all_words = to_sents(lines)

    sent_count = 0
    parse_count = 0
    meta_found = False
    metastring = "meta"
    meta_sentences = []
    meta_props = []
    e_count = 1
    x_count = 1
    u_count = 1
    for sent, words in zip(full_sents, all_words):
        parse_count += 1
        if sent_id_re.search(sent[0]):
            metastring = str(re.sub("\W", "", sent[0]))
            if meta_sentences != []:
                print "% " + " ".join(meta_sentences)
                print "id(" + str(prevmetastring) + ")."
                print " & ".join(meta_props)
                print ""
                e_count = 1
                x_count = 1
                u_count = 1
            meta_sentences = []
            meta_props = []
            meta_found = True
            prevmetastring = metastring

        if meta_found and not sent_id_re.search(sent[0]) and (sent != ["."]):
            try:
                meta_sentences.append(" ".join(sent))
                prop_sent, prop_dict, e_count, x_count, u_count \
                    = prop_to_dict(words, e_count, x_count, u_count)
                prop_dict = replace_args(prop_sent, prop_dict)
                printable_props = to_print(prop_dict, sent)
                meta_props.append(printable_props)
            except Exception, err:
                logging.exception(" ".join(sent))
                logging.exception(str(err))

        if metastring != "meta" and parse_count == len(full_sents):
            print "% " + " ".join(meta_sentences)
            print "id(" + str(prevmetastring) + ")."
            print " & ".join(meta_props)
            print ""
            e_count = 1
            x_count = 1
            u_count = 1

        if (not sent_id_re.search(sent[0])) and (not meta_found) and \
           (sent != ['.']):
            sent_count += 1
            print "% " + " ".join(sent)
            print "id(" + str(sent_count) + ")."
            try:
                prop_sent, prop_dict, e_count, x_count, u_count \
                    = prop_to_dict(words, e_count, x_count, u_count)
                prop_dict = replace_args(prop_sent, prop_dict)
                print to_print(prop_dict, sent)
                print ""
            except Exception, err:
                logging.exception(" ".join(sent))
                logging.exception(str(err))
            e_count = 1
            x_count = 1
            u_count = 1


if __name__ == "__main__":
    main()
