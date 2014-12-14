#!/usr/bin/python2
# -*- coding: UTF-8 -*-

from question_classification.web import main
import sys
from question_classification.http_get_cache_proxy import run, stop

if __name__ == "__main__":
    #try:
    # run()
    main(sys.argv)
    # stop()
    #except BaseException, e:
    #    print e.message
    #    raise e
