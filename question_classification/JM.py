#!/usr/bin/python2
# -*- coding: UTF-8 -*-

from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SupervisedDataSet, ClassificationDataSet
from pybrain.structure import TanhLayer, SoftmaxLayer



ds = SupervisedDataSet(2, 1)

for i in range(1):
    ds.addSample((0, 0), (0,))
    ds.addSample((0, 1), (1,))
    ds.addSample((1, 0), (1,))
    ds.addSample((1, 1), (0,))
for input, trg in ds:
    print input, trg
    print int(trg[0])


# ds = ClassificationDataSet(2, nb_classes=2)
# for i in range(1):
#    ds.appendLinked((0, 0), (0,))
#    ds.appendLinked((0, 1), (1,))
#    ds.appendLinked((1, 0), (1,))
#    ds.appendLinked((1, 1), (0,))
#
# for i in ds:
#     print i
# ds._convertToOneOfMany([0, 1])
# for i in ds:


#net = buildNetwork(ds.indim, 3, ds.outdim, bias=True, hiddenclass=TanhLayer, outclass=SoftmaxLayer)
# net = buildNetwork(ds.indim, 3, ds.outdim, bias=True, hiddenclass=TanhLayer)
#
# trainer = BackpropTrainer(net, ds, momentum=0.5, verbose=False)
# # BackpropTrainer(module, dataset=None, learningrate=0.01, lrdecay=1.0, momentum=0.0, verbose=False, batchlearning=False, weightdecay=0.0)
#
# trainer.trainUntilConvergence(maxEpochs=100)
# # trainUntilConvergence(dataset=None, maxEpochs=None, verbose=None, continueEpochs=10, validationProportion=0.25)
#
# print net.activate((0, 0))
# print net.activate((0, 1))
# print net.activate((1, 0))
# print net.activate((1, 1))
#
# #trainer.testOnData(ds, verbose=True)
#
#
# #tstdata, trndata = alldata.splitWithProportion( 0.25 )
# #podzial datasetu na uczace i testowe, losowy

