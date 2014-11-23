#!/usr/bin/python2
# -*- coding: UTF-8 -*-

import os
import subprocess

def main(args=[__file__]):
    plain_root = os.path.join(os.path.dirname(__file__), "../data/plain_data")
    tagged_root = os.path.join(os.path.dirname(__file__), "../data/tagged_data")
    for fn in os.listdir(plain_root):
        inpath = os.path.join(plain_root, fn)
        outpath = os.path.join(tagged_root, fn[0:-3]+"xml")
        subprocess.call("wcrft-app nkjp_e2.ini -i text "+inpath+" -O "+outpath, shell=True)
