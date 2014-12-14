#!/usr/bin/python2
# -*- coding: UTF-8 -*-
from collections import namedtuple
import pylev

import requests

# remove "localhost:8000/" to stop caching
# APIS_BASE = "http://localhost:11111/plwordnet.pwr.wroc.pl/wordnet/api"
APIS_BASE = "http://plwordnet.pwr.wroc.pl/wordnet/api"

sense = namedtuple("sense", "id lemma lang".split())

counter = [0]

def call_clarin(service, path_arg):
    p = "/".join([APIS_BASE, service, path_arg])
    print p
    resp = requests.get(p)
    print resp.status_code
    resp.raise_for_status()
    return resp.json()

def get_senses(word, lang=u"pl_PL"):
    return [ sense(s[u"sense_id"], s[u"lemma"], s[u"language"]) for s in call_clarin("lexemes", word) if s[u"language"]==lang ]

def get_sense(word, lang=u"pl_PL"):
    senses = get_senses(word, lang)
    counter[0] += 1
    if counter[0] % 100 == 0:
        print "sense", counter[0]
    return min(senses, key=lambda x: pylev.levenshtein(x, word)) if senses else None



def get_hyponyms_paths(word, lang=u"pl_PL"):
    out = []
    s = get_sense(word, lang)
    if s is not None:
        paths = call_clarin("hyponyms", s.id)
        if paths:
            for path in paths:
                out.append([ sense(el[u"id"], el[u"lemma"], lang) for el in path ])
    return out
    # return [ [  for el in path ] for path in  ]
    # return reduce(lambda x, y: x+y, [  for path in call_clarin("hyponyms", s.id) ], []) \
    #             if s is not None \
    #             else []

def main(args=[]):
    counter[0] = 0
    print get_hyponyms_paths("matka")[0][-2]