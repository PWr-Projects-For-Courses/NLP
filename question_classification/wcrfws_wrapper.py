#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import time

SLEEP_TIME = 0.05

SEND_ADDR = 'http://clarin-pl.eu/synat/ws/tagger/send.php'
CHECK_ADDR = 'http://clarin-pl.eu/synat/ws/tagger/check.php'
RESULTS_ADDR = 'http://clarin-pl.eu/synat/ws/tagger/results.php'

class WCRFTWSWrapper:

    def call_wcrft(self, sentence):
        args = {'input': 'text',
                'output': 'plain',
                'content': sentence,
                'guesser': False,
                'ambiguity': False,
                'chunks': False
                }
        done = False
        while not done:
            time.sleep(SLEEP_TIME)
            token_resp = requests.post(SEND_ADDR, data=args)
            try:
                print token_resp.json()
                token = token_resp.json()
                done = True
            except ValueError:
                print token_resp
                print token_resp.content
                print('ve')
        done = False
        time.sleep(SLEEP_TIME)
        while not done:
            res = requests.post(CHECK_ADDR, data=token)
            done = True if res.json()[u'status'] == u'READY' else False
            time.sleep(SLEEP_TIME)
        args = {'token': token[u'token'], 'output': 'plain'}
        res = requests.post(RESULTS_ADDR, data=args)
        return res.json()[u'xml']

    def parse(self, res):
        lines = res.strip().splitlines()
        for line in lines:
            if line.startswith("\t"):
                line = line.strip().split()
                yield line[0]

    def lematize(self, sentence):
        result = self.call_wcrft(sentence)
        return " ".join(self.parse(result))

if __name__=="__main__":
    assert WCRFTWSWrapper().lematize(u"Kopnąłem Alę w nos.") == u"kopnąć być Ala w nos ."