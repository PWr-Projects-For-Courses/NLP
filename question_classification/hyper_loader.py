#!/usr/bin/python2
# -*- coding: UTF-8 -*-

import os
import codecs
import csv

ROOT = os.path.join(os.path.dirname(__file__), "../data/hyper_freq")
LEVELS = [-1, -2, 1, 2, 3]
CLASSES = classes = u'''QC_CAUSE QC_DECISION QC_DEF QC_DIRECT QC_LOC QC_NONPER QC_PER QC_PROCEDURE QC_QUANTITY QC_STATE QC_TEMP
'''.strip().split()


def load(level, clazz):
    '''
    Loads the given level of hyperonyms for the given class.
    It returns a dict which keys are the hyperonyms. Under every key you can find a dict
    with keys 'relative' and 'absolute', giving the relative and absolute frequencies
    '''
    path = os.path.join(ROOT, os.path.join(str(level), clazz + '.txt'))
    if not os.path.exists(path):
        print "There's not data for class", clazz, "at level:", level
        return None
    out = {}
    with codecs.open(path, 'r', 'utf8') as f:
        for line in f:
            row = line.split(";")
            out[row[0].strip('"')] = {'absolute': int(row[1]), 'relative': float(row[2])}
    return out

def load_all():
    '''
    Loads all class at all levels.
    It returns a dict with class names as keys. Inside there's a dict with
    possible levels. Venture further and you'll find a dict like the one returned
    from load() - hyperonyms as keys with dicts of frequencies inside
    '''
    out = {}
    for c in CLASSES:
        out[c] = {}
        for l in LEVELS:
            out[c][l] = load(l, c)
    return out


if __name__ == '__main__':
    print load_all()