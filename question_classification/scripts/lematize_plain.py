#!/usr/bin/python2
# -*- coding: UTF-8 -*-
import codecs

import os

from wcrft_wrapper import lematize


def main(args=[__file__]):

    plain_root = os.path.join(os.path.dirname(__file__),
                              "../data/../../data/plain_data")
    lemat_root = os.path.join(os.path.dirname(__file__),
                              "../data/../../data/lematized_data")

    for fn in os.listdir(plain_root):
        inpath = os.path.join(plain_root, fn)
        outpath = os.path.join(lemat_root, fn)
        with codecs.open(inpath, 'r', 'utf8') as f:
            with codecs.open(outpath, 'w', 'utf8') as outf:
                for line in f:
                    outf.write(lematize(line) + "\n")


if __name__ == '__main__':
    main()
