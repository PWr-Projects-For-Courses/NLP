#!/usr/bin/python2
# -*- coding: UTF-8 -*-

# Taken from:
# https://gist.github.com/bxt/5195500
# and then slightly modified

# Originally from http://sharebear.co.uk/blog/2009/09/17/very-simple-python-caching-proxy/
#
# Usage:
# A call to http://localhost:80000/example.com/foo.html will cache the file
# at http://example.com/foo.html on disc and not redownload it again. 
# To clear the cache simply do a `rm *.cached`. To stop the server simply
# send SIGINT (Ctrl-C). It does not handle any headers or post data. 

import BaseHTTPServer
from multiprocessing import Process
import os
import urllib2

class CacheHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        cache_filename = self.path.replace("/", "_")+".cached"
        cache_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "cache_data", cache_filename))
        if os.path.exists(cache_path):
            print "Cache hit"
            data = open(cache_path).readlines()
        else:
            print "Cache miss"
            data = urllib2.urlopen("http:/" + self.path).readlines()
            open(cache_path, 'wb').writelines(data)
        self.send_response(200)
        self.end_headers()
        self.wfile.writelines(data)

def serve():
    server_address = ('', 11111)
    httpd = BaseHTTPServer.HTTPServer(server_address, CacheHandler)
    httpd.serve_forever()

processes = []

def run():
    cache_dir = os.path.join(os.path.dirname(__file__), "cache_data")
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    processes.append(Process(target=serve))
    processes[0].start()


def stop():
    processes[0].terminate()
    processes[0].join()