#!/usr/bin/python2
# -*- coding: UTF-8 -*-

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
        return self.qid == other.qid and self.txt == other.txt and self.qc == other.qc and self.eat == other.eat