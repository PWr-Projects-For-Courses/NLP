#!/usr/bin/python
# -*- coding: utf-8 -*-

from question_classification.wcrfws_wrapper import WCRFTWSWrapper
from question_classification.wcrft_wrapper import WCRFTWrapper
from question_classification.chunker import IOBBIERWSWrapper
from question_classification import wordnet_wrapper

lematizer = WCRFTWrapper()
chunker = IOBBIERWSWrapper()
wordnet = wordnet_wrapper

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
od
nazywać
można
zrobić
skąd
o
móc
należeć'''.splitlines()