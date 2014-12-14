#!/usr/bin/python2
# -*- coding: UTF-8 -*-

from question_classification.model import Record, Corpus
import codecs
from question_classification.config import classes, feats

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

def main(args=[__file__]):
    config = (0, 1, 2, 3)
    path = "./data/data.csv"
    out_file = "./data/data.arff"
    records = read_file(path, *config)

    c = Corpus(classes, "", feats)
    Corpus.current_corpus = c

    with codecs.open(out_file, 'w', encoding="utf8") as f:
        print >> f, "@RELATION questions"
        for feat in feats:
            print >> f, "@ATTRIBUTE", feat, "{0, 1}"
        clazzez = [str(clazz) for clazz in classes]
        arffclasses = str(clazzez).strip("[]")
        arffclasses = "{" + arffclasses + "}"

        print >> f, "@ATTRIBUTE class", arffclasses
        print >> f, "@DATA"
        for r in records:
            features = r.lematized().features()
            features = [1 if feat else 0 for feat in features]
            row = str(features).strip("[]")
            if r.qc in classes:
                qc = r.qc
            else:
                qc = r.qc.partition(":")[0]
            row += ", " + qc
            print >> f, row

if __name__ == '__main__':
    main()