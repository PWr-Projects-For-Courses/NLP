#!/usr/bin/python
# -*- coding: utf-8 -*-

from question_classification.model import Record


class BaselineClassifier:
    def classify(self, sentence):
        r = Record("", sentence, "", "").lematized()
        if r.feature(u"dlaczego"):
            return "QC_CAUSE"
        elif r.feature(u"czy"):
            return "QC_DECISION"
        elif r.feature(u"co") and r.feature(u"to"):
            return "QC_DEF"
        elif r.feature(u"jaki"):
            return "QC_DIRECT"
        elif r.feature(u"gdzie"):
            return "QC_LOC"
        elif r.feature(u"kto"):
            return "QC_PER"
        elif r.feature(u"ile"):
            return "QC_QUANTITY"
        elif r.feature(u"jak"):
            if r.feature(u"być") or r.feature(u"mieć"):
                return "QC_STATE"
            else:
                return "QC_PROCEDURE"
        elif r.feature(u"kiedy"):
            return "QC_TEMP"
        return "QC_NONPER" #it is weirdest class, we use it as fallback

if __name__=="__main__":
    print BaselineClassifier().classify(u"Kto wrobil krolika Rogera?")
    print BaselineClassifier().classify(u"Jak dojść na dworzec?")