#!/usr/bin/python
# -*- coding: utf-8 -*-

import tempfile
import os
import subprocess

WCRFT_COMMAND = "wcrft-app"
MODEL = "nkjp_e2"
INP_FORMAT = "txt"
OUT_FORMAT = "plain"
ENCODING = "utf8"

TEMP_DIR = tempfile.gettempdir()

def call_wcrft(sentence):
    path = os.path.join(TEMP_DIR, "sentence"+str(hash(sentence))+".txt")
    with open(path, "w") as f:
        print >> f, sentence.encode(ENCODING)
    out = subprocess.check_output([WCRFT_COMMAND, MODEL, "-i", INP_FORMAT, path, "-o", OUT_FORMAT]).decode(ENCODING)
    os.remove(path)
    return out

def parse(res):
    lines = res.strip().splitlines()
    for line in lines:
        if line.startswith("\t"):
            line = line.strip().split()
            yield line[0]


def lematize(sentence):
    result = call_wcrft(sentence)
    return " ".join(parse(result))

if __name__=="__main__":
    assert lematize(u"Kopnąłem Alę w nos.") == u"kopnąć być Ala w nos ."
