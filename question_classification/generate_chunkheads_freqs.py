#!/usr/bin/python2
# -*- coding: UTF-8 -*-
from collections import namedtuple

import requests
import time
from bs4 import BeautifulSoup

SLEEP_TIME = 0.05

SEND_ADDR = 'http://clarin-pl.eu/synat/ws/chunker/send.php'
CHECK_ADDR = 'http://clarin-pl.eu/synat/ws/chunker/check.php'
RESULTS_ADDR = 'http://clarin-pl.eu/synat/ws/chunker/results.php'

chunk_head = namedtuple("chunk_head", "orth lemma chunk_type".split())

class IOBBIERWSWrapper:
    def call_wcrft(self, sentence):
        args = {'input': 'text',
                'output': 'ccl',
                'content': sentence,
                'guesser': False,
                'ambiguity': False,
                'chunks': False
        }
        done = False
        # print "FRIST"
        while not done:
            time.sleep(SLEEP_TIME)
            token_resp = requests.post(SEND_ADDR, data=args)
            try:
                # print token_resp.json()
                token = token_resp.json()
                done = True
            except ValueError:
                # print token_resp
                # print token_resp.content
                # print('ve')
                pass
        done = False
        time.sleep(SLEEP_TIME)
        # print "SEKOND"
        while not done:
            res = requests.post(CHECK_ADDR, data=token)
            # print res.json()
            done = True if res.json()[u'status'] == u'READY' else False
            time.sleep(SLEEP_TIME)
        args = {'token': token[u'token'], 'output': 'plain'}
        res = requests.post(RESULTS_ADDR, data=args)
        print res.json()[u"xml"]
        return res.json()

    def is_head(self, ann):
        return self.is_attr_set(ann, "head")

    def is_attr_set(self, tag, attr, v="1"):
        try:
            return tag[attr]==v
        except:
            return False

    def is_disamb(self, lex):
        return self.is_attr_set(lex, "disamb")

    def flatten(self, l):
        return reduce(lambda x, y: x+y, l, [])

    def get_chunk_heads(self, sentence):
        head_tokens = filter(
            lambda t: #token
            len(
                 filter(
                     self.is_head,
                     t.find_all("ann")
                 )
            ),
            BeautifulSoup(self.call_wcrft(sentence)[u"xml"]).find_all("tok")
        )
        out = []
        for ht in head_tokens:
            for lex in ht.find_all("lex"):
                if self.is_disamb(lex):
                    for ann in ht.find_all("ann"):
                        if (self.is_head(ann)):
                            out.append(chunk_head(unicode(ht.orth.string), unicode(list(lex.strings)[0]), unicode(ann[u"chan"])))
        return out

def main(args=[]):
    print IOBBIERWSWrapper().get_chunk_heads(u"Dlaczego ludzie się od siebie uzależniają?")