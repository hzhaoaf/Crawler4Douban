#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
Script for getting info of a movie according to its subject ID the pipeline way
'''

import urllib2
import socket
import cookielib

timeout = 60
socket.setdefaulttimeout(timeout)

basicURL = 'http://api.douban.com/v2/movie/subject/'
detailsURL = 'http://movie.douban.com/subject/'

def getBasicMovieInfo(subjectID):
    try:
        request = urllib2.Request(basicURL + subjectID)
        response = urllib2.urlopen(request)
        jsonData = response.read()

        return jsonData

    except urlib2.HTTPError as e:
        if hasattr(e, 'code'):
            print 'HTTP Error code for subject ID %s: %s' % (subjectID, e.code)
        if hasattr(e, 'reason'):
            print 'HTTP Error reason for subject ID %s: %s' % (subjectID, e.reason)
    except urllib2.URLError as e:
        if hasattr(e, 'reason'):
            print 'URL Error reason for subject ID %s: %s' % (subjectID, e.reason)
    except socket.timeout as e:
        print 'Socket timeout for subject ID: %s' % (subjectID)
    else:
        pass

def getMovieDetailsHTMLPage(subjectID):
    try:
        cookie_support = urlib2.HTTPCookieProcessor(cookielib.CookieJar())
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urrlib2.install_opener(opener)

        url = detailsURL + subjectID

        htmlData = urllib2.urlopen(url).read()

        return htmlData

    except Exception as e:
        print 'Error when crawling html details for ID: %s' % (subjectID)


def getMovieShortCommentsHTMLPage(subjectID):
    pass

def getMovieAwardsHTMLPage(subjectID):
    pass

def parseUserTagsFromHTML(htmlContent):
    pass

def parseOthersLikeFromHTML(htmlContent):
    pass

def parseShortCommentsFromHTML(htmlContent):
    pass

def parseAwardsInfoFromHTML(htmlContent):
    pass

def insertMovieInfoToMysql(basicInfo, userTags, othersLike, shortComments, awardsInfo):
    pass
