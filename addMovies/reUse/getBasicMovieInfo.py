#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Pull Douban Movie basic info according to the subject id
'''

import urllib2
import socket
import cookielib

timeout = 60
socket.setdefaulttimeout(timeout)

basicURL = 'http://api.douban.com/v2/movie/subject/'

def getBasicMovieInfoBySubjectID(subjectID):
    try:
        request = urllib2.Request(basicURL + subjectID)
        response = urllib2.urlopen(request)
        jsonData = response.read()

        return jsonData

    except urllib2.HTTPError as e:
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
