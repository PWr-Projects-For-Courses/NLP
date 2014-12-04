#!/usr/bin/python2
# -*- coding: UTF-8 -*-
from collections import namedtuple
import pylev

import requests

APIS_BASE = "http://plwordnet.pwr.wroc.pl/wordnet/api"

sense = namedtuple("sense", "id lemma lang".split())

def call_clarin(service, path_arg):
    resp = requests.get("/".join([APIS_BASE, service, path_arg]))
    resp.raise_for_status()
    return resp.json()

def get_senses(word, lang=u"pl_PL"):
    return [ sense(s[u"sense_id"], s[u"lemma"], s[u"language"]) for s in call_clarin("lexemes", word) if s[u"language"]==lang ]

def get_sense(word, lang=u"pl_PL"):
    return min(get_senses(word, lang), key=lambda x: pylev.levenshtein(x, word))

def get_hyponyms_paths(word, lang=u"pl_PL"):
    s = get_sense(word, lang)
    return [ [ sense(el[u"id"], el[u"lemma"], lang) for el in path ] for path in call_clarin("hyponyms", s.id) ]

def main(args=[]):
    print get_hyponyms_paths("matka")[0][-2]