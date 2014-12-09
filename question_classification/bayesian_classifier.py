#!/usr/bin/python2
# -*- coding: UTF-8 -*-
import math

from question_classification.hyper_loader import load_all
from question_classification.chunker import IOBBIERWSWrapper
from question_classification.wordnet_wrapper import get_hyponyms_paths
from functools import partial

FREQS = load_all()
chunker = IOBBIERWSWrapper()
LEVEL = -1

def find_oto_phrase(sentence, qc):
    heads = chunker.get_chunk_heads(sentence)
    heads = [head.lemma for head in heads]
    likelihood_foo = partial(likelihood, qc=qc)
    return max(heads, key=likelihood_foo)


def likelihood(token, qc):
    out = 0.0
    hyponyms = get_hyponyms_paths(token)
    #print hyponyms                 # take a look here, sometimes we get only one path with one level
    for path in hyponyms:
        freq = get_freq(path[LEVEL].lemma, qc, LEVEL)      # wtf, something is not right
        #freq = get_freq(hyponyms[path][LEVEL], qc, LEVEL)
        if freq > 0:
            out += math.log(freq, 2)
    return out

def get_freq(token, qc, level):
    try:
        return FREQS[qc][level][token]['relative']
    except KeyError:
        return 0

def main(args):
    print find_oto_phrase(u'Dlaczego mamy sny?', 'QC_CAUSE')

#wynik[x][y] oznacza ścieżke x, poziom y) - na razie hardkoduj poziom 1

#znajdz_wskaznik_oto(sentence):
#　　heads = find_chunk_heads(sentence)
#　　return max(heads, key=pseudo_prob)
#
#pseudo_prob(token):
#　　out = 0.0
#　　for H <- each hyperonym of level X of token:
#　　　　helper = freq[H]
#　　　　if helper>0:
#　　　　　　out += log(helper)
#　　return out