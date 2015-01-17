#!/usr/bin/python
# -*- coding: utf-8 -*-


def feature(vector, name):
    return vector[Corpus.current_corpus.feature_words.index(name)]>0

def classify(feature_vector):
    if feature(feature_vector, u"dlaczego"):
        return "QC_CAUSE"
    elif feature(feature_vector, u"czy"):
        return "QC_DECISION"
    elif feature(feature_vector, u"co") and feature(feature_vector, u"to"):
        return "QC_DEF"
    elif feature(feature_vector, u"jaki"):
        return "QC_DIRECT"
    elif feature(feature_vector, u"gdzie"):
        return "QC_LOC"
    elif feature(feature_vector, u"kto"):
        return "QC_PER"
    elif feature(feature_vector, u"ile"):
        return "QC_QUANTITY"
    elif feature(feature_vector, u"jak"):
        if feature(feature_vector, u"być") or feature(feature_vector, u"mieć"):
            return "QC_STATE"
        else:
            return "QC_PROCEDURE"
    elif feature(feature_vector, u"kiedy"):
        return "QC_TEMP"
    return "QC_NONPER" #it is weirdest class, we use it as fallback

if __name__=="__main__":
    from question_classification.model import Record, Corpus

    print classify(Record("", u"Kto wrobil krolika Rogera?", "", "").lematized().features())
    print classify(Record("", u"Jak dojść na dworzec?", "", "").lematized().features())