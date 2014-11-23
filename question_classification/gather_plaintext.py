#!/usr/bin/python2
# -*- coding: UTF-8 -*-

import os
from question_classification.model import Record
import codecs

def read_record(txt, qid_idx, txt_idx, qc_idx, eat_idx, separator=u";"):
    '''
    Zamień pojedynczy wiersz na rekord.
    :param txt: unicode, treść wiersza
    :param qid_idx: index qid w wierszu
    :param txt_idx: analogicznie
    :param qc_idx: analogicznie
    :param eat_idx: analogicznie
    :param separator: separator CSV
    :return: Record
    '''
    parts = txt.split(separator)
    return Record(*map(unicode.strip, [parts[qid_idx], parts[txt_idx], parts[qc_idx], parts[eat_idx]]))

def read_file(path, qid_idx, txt_idx, qc_idx, eat_idx, separator=u";", encoding="utf8"):
    '''
    Wczytaj wszystkie rekordy z pliku; argumenty intuicyjnie lub analogicznie jak w read_record
    :return:
    '''
    out = []
    with codecs.open(path, encoding=encoding) as f:
        for line in f:
            out.append(read_record(line, qid_idx, txt_idx, qc_idx, eat_idx, separator))
    return out

def dump_plaintext(path, records, encoding="utf8"):
    with codecs.open(path, "w", encoding=encoding) as f:
        for r in records:
            plain = r.__unicode__()
            print >> f, plain[1:-1]

def main(args=[__file__]):
    config = (0, 1, 2, 3)
    path = "./data/data.csv"
    out_root = os.path.join(os.path.dirname(__file__), "../data/plain_data")
    records = read_file(path, *config)
    classes = {}
    for r in records:
        keys = ['ALL']
        if ':' in r.qc:
            keys.append(r.qc.partition(":")[0])
        keys.append(r.qc)
        for key in keys:
            if key not in classes:
                classes[key] = []
            classes[key].append(r)
    for clazz in classes:
        out_path = os.path.join(out_root, clazz.replace('"', '') + ".txt")
        dump_plaintext(out_path, classes[clazz])