#!/usr/bin/python2
# -*- coding: UTF-8 -*-
from question_classification import wcrft_wrapper


class Corpus:
    current_corpus = None
    corpus_stack = []

    def __init__(self, class_set, eat_set, feature_words):
        self.class_set = list(class_set)
        self.eat_set = list(eat_set)
        self.feature_words = list(feature_words)

    def class_idx(self, record):
        return self.class_set.index(record.qc)

    def eat_idx(self, record):
        return self.eat_set.index(record.eat)

    def __enter__(self):
        Corpus.corpus_stack.append(Corpus.current_corpus)
        Corpus.current_corpus = self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Corpus.current_corpus = Corpus.corpus_stack.pop()


#todo: memoize the hell out of this
class Record:
    '''
    Atrybuty (wszystkie typu unicode):
    * qid - question id
    * txt - treść pytania
    * qc - question class
    * eat - expected answer type
    '''
    def __init__(self, qid, txt, qc, eat):
        self.qid = qid
        self.txt = txt
        self.qc = qc
        self.eat = eat

    def __str__(self):
        return self.txt.decode("ascii", "ignore")

    def __unicode__(self):
        return self.txt

    def urepr(self):
        return u"<Record id: "+ self.qid+ \
                u"; txt: "+ self.__unicode__()+ \
                u"; qc: "+ self.qc + \
                u"; eat: "+self.eat+u">"


    def to_csv_row(self, separator=u";"):
        return separator.join(map(lambda x : u'"'+x+u'"', [self.qid, self.txt, self.qc, self.eat]))

    @staticmethod
    def from_csv_row(row, separator=u";"):
        '''
        :param row: unicode
        :return: Record
        '''
        parts = row.split(separator)
        assert len(parts) == 4
        return Record(*parts)

    def __eq__(self, other):
        return self.txt == other.txt and self.qc == other.qc and self.eat == other.eat

    def __hash__(self):
        return self.txt.__hash__() * 3 + self.qc.__hash__() * 7 + self.eat.__hash__() * 11

    def class_idx(self):
        return Corpus.current_corpus.class_idx(self)

    def eat_idx(self):
        return Corpus.current_corpus.eat_idx(self)

    def lematized(self):
        return Record(self.qid+"-lemma", wcrft_wrapper.lematize(self.txt), self.qc, self.eat)

    def words(self):
        return self.txt.split()

    def features(self):
        return [ feat_word in self.words() for feat_word in Corpus.current_corpus.feature_words ]


if __name__=="__main__":
    c = Corpus(u"K1 K2 K3".split(), u"E1 E2".split(), u"mieć być chcieć umieć".split())
    r = Record("id", u"Chcę móc Ci pomóc, ale nie umiem.", "K1", "E2")
    with c:
        assert r.class_idx() == 0
        assert r.eat_idx() == 1
        assert r.features() == [False]*4
        assert r.lematized().features() == [False, False, True, True]