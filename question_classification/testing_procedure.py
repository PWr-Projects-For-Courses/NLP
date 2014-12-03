#!/usr/bin/python2
# -*- coding: UTF-8 -*-
import codecs

import os
from pybrain import TanhLayer, SoftmaxLayer, SigmoidLayer, GaussianLayer
from pybrain.datasets import ClassificationDataSet, SupervisedDataSet
from pybrain.supervised import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork
from question_classification.model import Corpus, Record
from question_classification.config import classes, feats


class EvalResult:

    def __init__(self, clazz):
        self.clazz = clazz
        self.tp = 0
        self.tn = 0
        self.fp = 0
        self.fn = 0
        self.count = 0

    def getRecall(self):
        return 1.0* self.tp / (self.tp + self.fn)

    def getPrecision(self):
        return 1.0 * self.tp / (self.tp + self.fp)

    def getAccuracy(self):
        return 1.0 * (self.tp + self.tn) / (self.tp + self.tn + self.fp + self.fn)

    def getFMeasure(self):
        return (2.0 *self.tp) / (2 * self.tp + self.fp + self.fn)


class Evaluation:

    def getAllCount(self):
        sum = 0
        for eval in self.evals:
            sum += eval.count
        return sum

    def getWeightedRecall(self):
        sum = 0.0
        for eval in self.evals:
            sum += eval.getRecall() * eval.count
        return sum / self.getAllCount()

    def getWeightedPrecision(self):
        sum = 0.0
        for eval in self.evals:
            sum += eval.getPrecision() * eval.count
        return sum / self.getAllCount()

    def getWeightedAccuracy(self):
        sum = 0.0
        for eval in self.evals:
            sum += eval.getAccuracy() * eval.count
        return sum / self.getAllCount()

    def getWeightedFMeasure(self):
        sum = 0.0
        for eval in self.evals:
            sum += eval.getFMeasure() * eval.count
        return sum / self.getAllCount()


data_root = os.path.join(os.path.dirname(__file__), "../data/lematized_data")


c = Corpus(classes, "", feats)
Corpus.current_corpus = c


def getSeparateDataSets(testSize = 0.2):
    trnDs = ClassificationDataSet(len(feats), nb_classes=len(classes))
    tstDs = SupervisedDataSet(len(feats), 1)
    for c in classes:
        with codecs.open(os.path.join(data_root, c+".txt"), 'r', 'utf8') as f:
            lines = f.readlines()
            breakpoint = (1.0 - testSize) * len(lines)
            for i in range(len(lines)):
                r = Record("11", lines[i], c, "")
                if i < breakpoint:
                    trnDs.appendLinked(r.features(), [r.class_idx()])
                else:
                    tstDs.appendLinked(r.features(), [r.class_idx()])
    trnDs._convertToOneOfMany([0, 1])
    return trnDs, tstDs

def addResult(eval, res, expected):
    if res == expected:
        for i, evalRes in enumerate(eval.evals):
            if i == res:
                evalRes.tp += 1
                evalRes.count += 1
            else:
                evalRes.tn += 1
    else:
        for i, evalRes in enumerate(eval.evals):
            if i == res:
                evalRes.fp += 1
            elif i == expected:
                evalRes.fn += 1
                evalRes.count += 1
            else:
                evalRes.tn += 1

def evaluate(net, tstData):
    out = Evaluation()
    out.evals = []
    for i in range(len(classes)):
        out.evals.append(EvalResult(classes[i]))
    for input, target in tstData:
        probs = net.activate(input)
        res = max(xrange(len(classes)), key= lambda x: probs[x])
        addResult(out, res, int(target[0]))
    return out

detailed = False

def main(args=[__file__]):
    trnDs, tstDs = getSeparateDataSets()
    net = buildNetwork(trnDs.indim, int((trnDs.indim + trnDs.outdim)/2), trnDs.outdim, bias=True, hiddenclass=TanhLayer, outclass=SoftmaxLayer)
    trainer = BackpropTrainer(net, trnDs, momentum=0.75, verbose=True, learningrate=0.05)
    trainer.trainUntilConvergence(maxEpochs=200, validationProportion=0.1)
    eval = evaluate(net, tstDs)
    print "accuracy:", eval.getWeightedAccuracy()
    print "recall:", eval.getWeightedRecall()
    print "precision:", eval.getWeightedPrecision()
    print "F-measure:", eval.getWeightedFMeasure()

    if detailed:
        for evalRes in eval.evals:
            print "Class:", evalRes.clazz
            print "Accuracy:", evalRes.getAccuracy()
            print "Recall:", evalRes.getRecall()
            print "Precision:", evalRes.getPrecision()
            print "F-measure:", evalRes.getFMeasure()
            print '-'*35

    print '-'*70

if __name__ == '__main__':
    main()