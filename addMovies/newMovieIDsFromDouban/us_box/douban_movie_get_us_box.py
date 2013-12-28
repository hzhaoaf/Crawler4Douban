#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Pull Douban Movie US Box
'''

import urllib2
import socket
import time

basicUrl = 'http://api.douban.com/v2/movie/us_box'

def get_items():
    try:
        reqUrl = basicUrl;
        print 'Now requesting: %s'  % (reqUrl)
        req = urllib2.Request(reqUrl)
        response = urllib2.urlopen(req, timeout = 60)
        #print(response.read())

        # Save to file
        jsonData = response.read()

        jsonFileName = 'us_box.json'
        print "Now saving to file: %s" % (jsonFileName)
        with open(jsonFileName, "wb") as jsonWriter:
            jsonWriter.write(jsonData)

    except Exception as e:
        print 'Exception: %s' % (e)

print 'Start Work...'
# Get to work
get_items()
print 'Done!'
