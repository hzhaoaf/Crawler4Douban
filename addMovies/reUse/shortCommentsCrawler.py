#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import time
import os
import cookielib
import sys
import socket

import fileUtils

socket.setdefaulttimeout(60)


def crawlShortCommentsBySubjectID(eid , num , htmls_dir):
    try:
        cookie_support = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)

        shortCommentHTMLFilesCount = 0
        start = 0
        if not os.path.isdir(htmls_dir):
            os.mkdir(htmls_dir)

        if num > 1000:
            end = 50
        else:
            end = num / 20 + 1

        for i in range(0, end):
                start = i * 20

                path = htmls_dir + '/' + str(start) + '.html'

                if os.path.exists(path) == False:
                    url = 'http://movie.douban.com/subject/' + eid + '/comments?start=' + str(start) + '&limit=20&sort=new_score'
                    #print url
                    try:
                        data = urllib2.urlopen(url).read()
                    except Exception, e:
                        data = 'no data'

                    #print path
                    fileUtils.writeTo(path, data, 'w')
                else:
                    print 'File %s exists already and will pass.' % (path)

                shortCommentHTMLFilesCount += 1
                time.sleep(2)

        return shortCommentHTMLFilesCount
        #print eid + ' short comments crawled OK!'
    except Exception as e:
        print "Error occured when crawling short comments: %s" % (e)
