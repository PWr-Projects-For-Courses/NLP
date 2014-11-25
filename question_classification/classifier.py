#!/usr/bin/python2
# -*- coding: UTF-8 -*-
import codecs
import os
from pybrain import TanhLayer, SoftmaxLayer
from pybrain.datasets import ClassificationDataSet
from pybrain.supervised import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork
from pybrain.tools.xml import NetworkReader, NetworkWriter
from question_classification.model import Corpus, Record

net = []

data_root = os.path.join(os.path.dirname(__file__), "../data/plain_data")

NET_FILE = os.path.join(os.path.dirname(__file__), "net.xml")

classes = u'''QC_CAUSE QC_DECISION QC_DEF QC_DIRECT QC_LOC QC_NONPER QC_PER QC_PROCEDURE QC_QUANTITY QC_STATE QC_TEMP
'''.strip().split()

feats = u'''być
w
CO
jak
jaki
to
się
z
czy
co
kto
gdzie
na
ile
dlaczego
do
mieć
kiedy
po
który
od'''.splitlines()

c = Corpus(classes, "", feats)
Corpus.current_corpus = c

def build_net():
    if os.path.exists(NET_FILE):
        return NetworkReader.readFrom(NET_FILE)
    ds = ClassificationDataSet(len(feats), nb_classes=len(classes))
    for c in classes:
        print c
        with codecs.open(os.path.join(data_root, c+".txt"), 'r', 'utf8') as f:
            for line in f:
                r = Record("11", line, c, "").lematized()
                ds.appendLinked(r.features(), [r.class_idx()])
    ds._convertToOneOfMany([0, 1])
    net = buildNetwork(ds.indim, int((ds.indim + ds.outdim)/2), ds.outdim, bias=True, hiddenclass=TanhLayer, outclass=SoftmaxLayer)
    trainer = BackpropTrainer(net, ds, momentum=0.5, verbose=True)
    trainer.trainUntilConvergence(maxEpochs=50)
    NetworkWriter.writeToFile(net, NET_FILE)
    return net

def get_probabilities(sentence):
    if len(net) == 0:
        net.append(build_net())
    n = net[0]
    r = Record("", sentence, "", "").lematized()
    return n.activate(r.features())

def classify(sentence):
    res = get_probabilities(sentence)
    return classes[max(xrange(len(classes)), key= lambda x: res[x])]
if __name__ == '__main__':
    res = classify(u"Ile masz piłek")
    print res

