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

def dump_csv(path, records, separator=u";", encoding="utf8"):
    '''
    :param records: lista rekordów
    :return: nuffin
    '''
    with codecs.open(path, "w", encoding=encoding) as f:
        for r in records:
            print >>f, r.to_csv_row()

def main(args=[__file__]):
    out_path = "./data/data.csv"
    if len(args)>1:
        out_path = args[0]
    raw_data_dir = os.path.join(os.path.dirname(__file__), "../../../raw_data")

    # records = {} # słownik, żeby deduplikować rekordy
    records = set([])

    for (path, config) in [
        ("hipisek/hipi.csv", (0, 1, 3, 2)),
        ("pytki/pytki.csv", (0, 1, 6, 5)),
        ("razem/razem_eval.csv", (0, 1, 5, 4)),
        ("razem/razem_test.csv", (0, 1, 5, 4)),
        ("wyszukiwarki/wyszukiwarki.csv", (0, 1, 5, 4))
    ]:
        new_records = read_file(os.path.abspath(os.path.join(raw_data_dir, path)), *config)
        for r in new_records:
            # if r.qid in records:
            #     if not r == records[r.qid]:
            #         dir_name = path.partition("/")
            #         r.qid = unicode(dir_name)+r.qid
            #         if r.qid in records:
            #             raise LookupError(u"Was: "+records[r.qid].urepr()+u" ; is: "+r.urepr()+u" in file "+unicode(path))
            # else:
            #     records[r.qid] = r
            records.add(r)
    print len(records)
    dump_csv(out_path, records)