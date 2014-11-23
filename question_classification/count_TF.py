#!/usr/bin/python2
# -*- coding: UTF-8 -*-

import os
import operator
import codecs
import xml.etree.ElementTree as ET

stoplist = ['"',
            "'",
            ',',
            '?',
            '.',
            '-',
            '+']

def dump_dict(terms, path, encoding = "utf8"):
    terms = sorted(terms.items(), key=operator.itemgetter(1), reverse=True)
    with codecs.open(path, "w", encoding=encoding) as f:
        for k, v in terms:
            print >> f, k + " : " + str(v)

def main(args=[__file__]):
    tagged_root = os.path.join(os.path.dirname(__file__), "../data/tagged_data")
    tf_root = os.path.join(os.path.dirname(__file__), "../data/tf_data")
    for fn in os.listdir(tagged_root):
        path = os.path.join(tagged_root, fn)
        tree = ET.parse(path)
        root = tree.getroot()
        terms = {}
        for tok in root.iter('tok'):
            lex = tok.find("lex")
            lemat = lex.find('base').text
            if lemat not in stoplist:
                if lemat in terms:
                    terms[lemat] += 1
                else:
                    terms[lemat] = 1
        outpath = os.path.join(tf_root, fn[0:-3]+"txt")
        dump_dict(terms, outpath)