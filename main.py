#!/usr/bin/python2
# -*- coding: UTF-8 -*-

# from question_classification.generate_arff import main
from question_classification.generate_chunkheads_freqs import main
import sys

if __name__ == "__main__":
    #try:
    main(sys.argv)
    #except BaseException, e:
    #    print e.message
    #    raise e
