#!/usr/bin/python2
# -*- coding: UTF-8 -*-
import codecs
import os
from question_classification.config import chunker, wordnet, classes
from collections import defaultdict

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
HYPERONYM_OFFSETS = [1, 2, 3, -1, -2]

def make_dirs():
    for offset in HYPERONYM_OFFSETS:
        # for c in classes:
            p = os.path.join(DATA_DIR, "hyper_freq", str(offset))#, c)
            if not os.path.exists(p):
                os.makedirs(p)

def by_hyperonyms_for_lemmas(offset, path):
    '''
    Counts occurences of each hyperonyms of given offset  for lemma of each chunks head.
    :param offset: hyperonym offset
    :param path: path to file with question of given class per line
    :return: pair: (dict lemma -> counts, sum of counts)
    '''
    result = defaultdict(lambda: 0)
    s = 0
    with codecs.open(path, encoding="utf8") as f:
        for line in f:
            chunk_heads = chunker.get_chunk_heads(line)
            for ch in chunk_heads:
                for x in wordnet.get_hyponyms_paths(ch.lemma):
                    for h in x[offset]:
                        result[h]+=1
                        s +=1
    return result, s

def main(args=[]):
    make_dirs()
    for offset in HYPERONYM_OFFSETS:
        print "="*80
        print "OFFSET:", offset
        for c in classes:
            print "-"*40
            print "CLASS:", c
            freqs, s = by_hyperonyms_for_lemmas(offset, os.path.join(DATA_DIR, "plain_data", c+".txt"))
            order = sorted(freqs.keys(), key=freqs.__getitem__)
            with codecs.open(os.path.join(DATA_DIR, "hyper_freq", str(offset), c+".txt"), "w", encoding="utf8") as f:
                for h in order:
                    print >> f, '"'+h+'";'+unicode(freqs[h])+";"+unicode(1.0*freqs[h]/s)
