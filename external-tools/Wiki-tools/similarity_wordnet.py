#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# similarity_wordnet.py
# similarity measurement tool using WordNet incorporated with
# Derivationally-Related-Form (DRF)
# supports languages: EN, FA, ES, RU
#
# Author: Xing Shi
# contact: xingshi@usc.edu
#
# see demo() for help
# outside modules should call path_similarity(word1, pos1, word2, pos2) to
# calculate similarity


from nltk.corpus import wordnet as wn
from collections import deque
import pickle


loaded = False


def extract_pos_offset(fileName):
    with open(fileName, 'w') as f:
        items = wn._lemma_pos_offset_map.items()
        pos_offset_map = set()
        for item in items:
            # lemma = item[0]
            for pos in item[1]:
                offsets = item[1][pos]
                for offset in offsets:
                    pos_offset_map.add((pos, offset))
        for pair in pos_offset_map:
            f.write(pair[0] + ' ' + str(pair[1]) + '\n')
    print len(pos_offset_map)


def loadAll():
    global loaded
    if loaded:
        return
    index = wn._lemma_pos_offset_map
    print 'Loading WordNet into cache... '
    cache = wn._synset_offset_cache
    with open('pos_offset.txt', 'r') as f:
        for line in f:
            ll = line.split()
            pos = ll[0]
            offset = int(ll[1])
            wn._synset_from_pos_and_offset(pos, offset)
        print 'Done: ' + str(sum([len(cache[x]) for x in cache])) \
            + '/' + str(len(index))
    loaded = True


def print2file(synset, array, fathers, fileName):
    with open(fileName, 'w') as fout:
        for i in xrange(len(array)):
            s = array[i]
            fout.write(str(synset.offset) + '\t' + str(s[0].offset) +
                       '\t' + str(s[1]) + '\t')
            # Get father chain
            father = fathers[i]
            while father[0] != -1:
                fout.write(str(array[father[0]][0].offset) + '-' +
                           father[1] + ' ')
                father = fathers[father[0]]
            fout.write('\n')


def pickleResult(synsets, fathers):
    offsets = [(s[0].offset, s[1]) for s in synsets]
    pickle.dump((offsets, fathers), 'list.pickle')


def lemmas_property(syn, func):
    lemmas = syn.lemmas
    result = []
    for l in lemmas:
        result += [ll.synset for ll in func(l)]
    return result


def getNeighboursL(syn):
    neighbours = []
    # hyper:e / hypon:o / drf:d / similar to:s / antonym: a
    # verb / noun
    # hypernyms / hyponyms / derivationally related form
    if syn.pos == wn.VERB or syn.pos == wn.NOUN:
        neighbours += [(syn.hypernyms(), 'e')]
        neighbours += [(syn.hyponyms(), 'o')]
        neighbours \
            += [(lemmas_property(syn,
                                 lambda l: l.derivationally_related_forms()),
                 'd')]
    # adj
    # similar to / antonyms / derivationally related form
    elif syn.pos == wn.ADJ or syn.pos == wn.ADJ_SAT:
        neighbours += [(syn.similar_tos(), 's')]
        neighbours += [(lemmas_property(syn, lambda l: l.antonyms()), 'a')]
        neighbours \
            += [(lemmas_property(syn,
                                 lambda l: l.derivationally_related_forms()),
                 'd')]
    # adv
    # antonyms / there is no derivationally related form
    elif syn.pos == wn.ADV:
        neighbours += [(lemmas_property(syn, lambda l: l.antonyms()), 'a')]

    return neighbours


# provide all the neighbours around a certain synset
#
# Input:
#   synset: the root synset
#   my_max: the limitation of depth
# Output:
#   candidates: the neighbours
#   fathers: a array to record the path from synset to the neighbour.
# should call print2file(synset, candidates, fathers, 'file.txt') to get the
# formatted output to file.txt
def min_path_range(synset, my_max):
    seen = {}
    queue = deque([synset])
    lqueue = deque([0])
    temp_fathers = deque([(-1, 'r')])

    old = 0
    new = 0

    candidates = []
    fathers = []

    while len(queue) != 0:
        new = lqueue[0]
        if new != old:
            # print new, len(queue)
            old = new

        if lqueue[0] >= my_max:
            return (candidates, fathers)
        else:
            seen[queue[0]] = 1
            c = queue[0]
            cl = lqueue[0]
            f = temp_fathers[0]

            queue.popleft()
            lqueue.popleft()
            temp_fathers.popleft()

            candidates.append((c, cl))
            fathers.append(f)

            neighbours = getNeighboursL(c)
            for series in neighbours:
                ns = series[0]
                relation = series[1]
                for n in ns:
                    if n in seen:
                        continue
                    seen[n] = 1
                    queue.append(n)
                    lqueue.append(cl + 1)
                    temp_fathers.append((len(candidates) - 1, relation))

    return (candidates, fathers)


def min_path_synsets(synsets1, synsets2, my_max):
    length = -1
    seen = {}
    queue = deque(synsets1)
    lqueue = deque([0] * len(synsets1))
    temp_fathers = deque([(-1, 'r') for _ in synsets1])
    old = 0
    new = 0

    candidates = []
    fathers = []

    while len(queue) != 0:
        new = lqueue[0]
        if new != old:
            # print new, len(queue)
            old = new

        if lqueue[0] >= my_max:
            break
        else:
            seen[queue[0]] = 1
            c = queue[0]
            cl = lqueue[0]
            f = temp_fathers[0]

            queue.popleft()
            lqueue.popleft()
            temp_fathers.popleft()

            candidates.append((c, cl))
            fathers.append(f)

            if c in synsets2:
                length = cl
                break

            neighbours = getNeighboursL(c)
            for series in neighbours:
                ns = series[0]
                relation = series[1]
                for n in ns:
                    if n in seen:
                        continue
                    seen[n] = 1
                    queue.append(n)
                    lqueue.append(cl + 1)
                    temp_fathers.append((len(candidates) - 1, relation))

    # Return the length and path information
    father = fathers[-1]
    path = [(candidates[-1][0].name(), '_')]
    while father[0] != -1:
        path.append((candidates[father[0]][0].name(), father[1]))
        father = fathers[father[0]]
    path.reverse()

    return (length, path)


def min_path_words(word1, pos1, word2, pos2, my_max):
    synsets1 = wn.synsets(word1, pos1)
    synsets2 = wn.synsets(word2, pos2)
    if len(synsets1) == 0 or len(synsets2) == 0:
        return None
    else:
        return min_path_synsets(synsets1, synsets2, my_max)


# outside module should call this function
def path_similarity(word1, pos1, word2, pos2):
    global loaded
    if loaded is False:
        loadAll()

    r = min_path_words(word1, pos1, word2, pos2, 1000)
    if r is None or r[0] == -1:
        return None
    else:
        return 1.0 / (r[0] + 1)


def demo():
    # Load all synsets into RAM
    loadAll()

    # Similarity between two words:
    print min_path_words('water', 'n', 'liquid', 'a', 1000)

    # Similarity between two synset:
    water = wn.synsets('water', 'n')[0]
    liquid = wn.synsets('liquid', 'n')[0]
    print min_path_synsets(water, liquid, 1000)

    # Similarity between one synset and the rest synsets
    print min_path_range(water, 1000)


if __name__ == '__main__':
    demo()
