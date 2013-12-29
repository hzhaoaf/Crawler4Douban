#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Pull Douban Movie Now Playing
'''

import urllib2
import socket
import time
from HTMLParser import HTMLParser
import sys

basicUrl = 'http://movie.douban.com/nowplaying/beijing'

class parseMovieIDs(HTMLParser):
    def __init__(self):
        self.data = []
        self.movieLinks = []
        self.movieIDs = []
        self.href = 0
        self.linkname = ''
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    self.href = 1
                    self.movieLinks.append(value)

    def handle_data(self, data):
        if self.href:
            self.linkname += data

    def handle_endtag(self, tag):
        if tag == 'a':
            self.linkname = ''.join(self.linkname.split())
            self.linkname = self.linkname.strip()
            if self.linkname:
                self.data.append(self.linkname)
            self.linkname = ''
            self.href = 0

    def getresult(self):
        '''
        for value in self.data:
            print value
        '''

        for link in self.movieLinks:
            #print link
            if link.find('movie.douban.com/subject') > 0 and link.find('?from=playing_poster') > 0:
                link = link.replace('http://movie.douban.com/subject/', '')
                link = link.replace('?from=playing_poster', '')
                movieID = link.replace('/', '')
                self.movieIDs.append(movieID)

        #print 'Successfully got %s movie IDs.' %(len(self.movieIDs))
        #return self.movieIDs


        '''
        print 'Result: '
        print type(self.movieIDs)
        print len(self.movieIDs)

        for movieID in self.movieIDs:
            print movieID
        '''

        return set(self.movieIDs)


def get_items():
    try:
        reqUrl = basicUrl;
        print 'Now requesting: %s'  % (reqUrl)
        req = urllib2.Request(reqUrl)
        response = urllib2.urlopen(req, timeout = 60)
        #print(response.read())

        # Save to file
        htmlData = response.read()

        htmlFileName = 'now_playing.html'
        print "Now saving to file: %s" % (htmlFileName)
        with open(htmlFileName, "wb") as htmlWriter:
            htmlWriter.write(htmlData)

        return htmlData

    except Exception as e:
        print 'Exception: %s' % (e)
        return ''

if __name__ == "__main__":
    print 'Start Work...'
    # Get to work
    htmlSource = get_items()
    myParser = parseMovieIDs()
    myParser.feed(htmlSource)
    resultMovieIDs = myParser.getresult()
    myParser.close()


    print 'Result: '
    print type(resultMovieIDs)
    print len(resultMovieIDs)
    for movieID in resultMovieIDs:
        print movieID


    print 'Done!'
