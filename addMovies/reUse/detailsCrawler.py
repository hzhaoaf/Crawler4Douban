#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
Script for getting detail info of a movie according to its subject ID the pipeline way
'''

import urllib2
import socket
import cookielib

timeout = 100
socket.setdefaulttimeout(timeout)

detailsURL = 'http://movie.douban.com/subject/'

def crawlMovieDetailsHTMLPage(subjectID):
    try:
        cookie_support = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)

        url = detailsURL + subjectID

        htmlData = urllib2.urlopen(url).read()

        return htmlData

    except Exception as e:
        print 'Error when crawling html details for ID: %s' % (subjectID)
        if hasattr(e, 'code'):
            print 'Error code: %s' % (e.code)

        if hasattr(e, 'reason'):
            print 'Error reason: %s' % (e.reason)

        print 'Exception: %s' % (e)
