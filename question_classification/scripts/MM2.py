#!/usr/bin/python2
# -*- coding: UTF-8 -*-
import codecs
import os
from pybrain.datasets import ClassificationDataSet
from question_classification.classifier import classify
from question_classification.model import Record


data_root = os.path.join(os.path.dirname(__file__),
                         "../data/../../data/plain_data")

classes = u'''QC_CAUSE QC_DECISION QC_DEF QC_DIRECT QC_LOC QC_NONPER QC_PER QC_PROCEDURE QC_QUANTITY QC_STATE QC_TEMP
'''.strip().split()

true = 0
false = 0

for c in classes:
    with codecs.open(os.path.join(data_root, c+".txt"), 'r', 'utf8') as f:
        for line in f:
            r = Record("11", line, c, "").lematized()
            clazz = classify(r.txt)
            if clazz == r.qc:
                true += 1
            else:
                false += 1
                print line, r.qc, clazz
print true, false, 1.0 * true/(true+false)
