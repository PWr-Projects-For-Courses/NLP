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
from question_classification.config import classes, feats

class QCClassifier:

    net = None

    data_root = os.path.join(os.path.dirname(__file__), "../data/lematized_data")

    NET_FILE = os.path.join(os.path.dirname(__file__), "net.xml")


    # this was moved to model
    # c = Corpus(classes, "", feats)
    # Corpus.current_corpus = c

    def build_net(self):
        if os.path.exists(self.NET_FILE):
            return NetworkReader.readFrom(self.NET_FILE)
        ds = ClassificationDataSet(len(feats), nb_classes=len(classes))
        for c in classes:
            print c
            with codecs.open(os.path.join(self.data_root, c+".txt"), 'r', 'utf8') as f:
                for line in f:
                    r = Record("11", line, c, "")
                    ds.appendLinked(r.features(), [r.class_idx()])
        ds._convertToOneOfMany([0, 1])
        net = buildNetwork(ds.indim, int((ds.indim + ds.outdim)/2), ds.outdim, bias=True, hiddenclass=TanhLayer, outclass=SoftmaxLayer)
        trainer = BackpropTrainer(net, ds, momentum=0.75, verbose=True)
        trainer.trainUntilConvergence(maxEpochs=300)
        NetworkWriter.writeToFile(net, self.NET_FILE)
        return net

    def get_probabilities(self, sentence):
        if self.net is None:
            self.net = self.build_net()
        r = Record("", sentence, "", "").lematized()
        return self.net.activate(r.features())

    def classify(self, sentence):
        res = self.get_probabilities(sentence)
        return classes[max(xrange(len(classes)), key= lambda x: res[x])]


if __name__ == '__main__':
    classifier = QCClassifier()
    res = classifier.classify(u"Ile masz piłek")
    print res

