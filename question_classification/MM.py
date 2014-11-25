#!/usr/bin/python2
# -*- coding: UTF-8 -*-

from pybrain import TanhLayer
from pybrain.datasets import ClassificationDataSet
from pybrain.supervised import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork
from question_classification.model import Record, Corpus

defs = u'''Co to jest mirra?
Co to jest ACTA?
Co to jest Litwa?
Kto to jest kompozytor?
Co to jest projekt denko?
Co to jest Sampler?
Kim jest Robert Lewandowski?
Co to jest przebiegunowanie Ziemi?
Kto to jest Jarosław Kaczyński?
Co to jest Austriacka Szkoła Ekonomii?
O co chodzi w nowej promocji Coca Coli?
Co to jest tablet?
Co to Rynek Niedźwiedzia?
Kto to jest Papież?
Co to jest światło?
Co oznacza literka "D" w grupie krwi A rHD +?
Co to są święta Bożego Narodzenia?
"Co to za piosenka: ""o nie, nie, nie, nie mam czasu pisać tych wszystkich bzdur... których pełno masz w swoim koszu""?"
Co to jest żadziol?
Kim jest Sienkiewicz?
Co to są cewki zapłonowe?
Co to jest okres?
Kim jest Orłoś?
Kim był Kopernik?'''.splitlines()
pers = u'''Przez kogo zostały zniszczone Pompeje?
Kogo pracodawca nie może zwolnić?
Kto zabił Osamę bin Ladena?
Kto był pierwszym prezydentem Polski?
Z kogo składa się rada ministrów?
Kogo nazywamy człowiekiem renesansu?
Kto wygrał wybory?
Do kogo pasują rude włosy?
Przez kogo Bóg zawarł z nami przymierze?
Kogo beatyfikował Jan Paweł II?
Kto wynalazł szachy?
Kto je ślimaki?
Kto zagra Kurta Cobaina?
Do kogo adresować list motywacyjny?
Przez kogo do lecznictwa zostały wprowadzone tabletki?
Kto kandyduje na szefa SLD?
Z kim będzie walczył Pudzian?
Kogo można powołać do służby stałej w korpusie oficerów zawodowych wojska polskiego?
Kto zabił Kennedy'ego?
Kogo powołuje sejm?
Kto zabił Lecha Kaczyńskiego?
Z kim będzie walczył Adamek?
Kto jest prezydentem Niemiec?
Przez kogo są powoływani sędziowie?'''.splitlines()
i = 0
records = []
for l in defs:
    records.append(Record(str(i), l, "def", ""))
    i += 1
for l in pers:
    records.append(Record(str(i), l, "per", ""))
    i += 1

feats = [ "kto", "co", "z", u"być"]

c = Corpus(["def", "per"], [""], feats)
Corpus.current_corpus = c
ds = ClassificationDataSet(len(feats), nb_classes=2)
for r in records:
    ds.appendLinked(r.features(), [r.class_idx()])
ds._convertToOneOfMany([0, 1])

net = buildNetwork(ds.indim, 3, ds.outdim, bias=True, hiddenclass=TanhLayer)

trainer = BackpropTrainer(net, ds, momentum=0.5, verbose=False)
# BackpropTrainer(module, dataset=None, learningrate=0.01, lrdecay=1.0, momentum=0.0, verbose=False, batchlearning=False, weightdecay=0.0)

trainer.trainUntilConvergence(maxEpochs=100)

x = Record("ugachaka", "Co to jest seks?", "def", "")

print net.activate(x.features())