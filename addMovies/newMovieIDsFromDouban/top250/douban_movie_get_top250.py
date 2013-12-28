#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Pull Douban Movie Top 250
'''

import urllib2
import socket
import time
import datetime
import json

basicUrl = 'http://api.douban.com/v2/movie/top250'
top250IDFile = 'top250ID-' + str(datetime.date.today())

def get_items(start, count):
    try:
        reqUrl = basicUrl + '?start=' + str(start) + '&count=' + str(count)
        print 'Now requesting %s ' % (reqUrl)
        req = urllib2.Request(reqUrl)
        response = urllib2.urlopen(req, timeout = 60)
        #print(response.read())

        # Save to file
        print "Success pull items from " + str(start) + " to " + str(start + count - 1)
        jsonData = response.read()

        jsonFileName = 'top250-' +str(start) + '-' + str(start + count -1) + '.json'
        print "Now saving to file: %s " % (jsonFileName)
        with open(jsonFileName, "wb") as jsonWriter:
            jsonWriter.write(jsonData)

    except Exception as e:
        print 'Exception: %s' % (e)

print 'Start Work...'
# Get to work
get_items(0, 100)
get_items(100, 100)
get_items(200, 50)
print 'Done!'
