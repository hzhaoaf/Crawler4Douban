#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
Script for getting all info of a movie according to its subject ID the pipeline way
'''

import urllib2
import socket
import cookielib
import os
import sys

# import all user scripts
import getBasicMovieInfo
import detailsCrawler
import shortCommentsCrawler
import awardsCrawler
import userTagsParser
import othersLikeParser
import shortCommentsCountParser
import shortCommentsParser
import awardsParser

timeout = 60
socket.setdefaulttimeout(timeout)

basicURL = 'http://api.douban.com/v2/movie/subject/'
detailsURL = 'http://movie.douban.com/subject/'

fileMode = 'w+'

def getAllMovieInfoBySubjectID(subjectID):
    try:
        # Some constants of file and directory names
        basic_json = 'basic.json'
        details_html = 'details_html.html'
        awards_html = 'awards_html.html'
        shortComment_htmls_dir= 'short_comment_htmls'
        userTags_json = 'userTags.json'
        othersLike_json = 'othersLike.json'
        shortComments_json = 'shortComments.json'
        awards_json = 'awards.json'

        # Make a directory for each subject
        if not os.path.isdir(subjectID):
            os.mkdir(subjectID)

        shortComment_htmls_dir = subjectID + '/' + shortComment_htmls_dir

        basic_json = subjectID + '/' + basic_json
        details_html = subjectID + '/' + details_html
        awards_html = subjectID + '/' + awards_html
        userTags_json = subjectID + '/' + userTags_json
        othersLike_json = subjectID + '/' + othersLike_json
        shortComments_json = subjectID + '/' + shortComments_json
        awards_json = subjectID + '/' + awards_json

        # Go, boy, Go
        print 'Now trying to construct movie info for ID %s...' % (subjectID)

        '''
        Movie basic info
        '''
        if os.path.exists(basic_json) == False:
            print 'Getting movie basic info for ID %s...' % (subjectID)
            basicInfo = getBasicMovieInfo.getBasicMovieInfoBySubjectID(subjectID)
            if basicInfo == None:
                print 'Movie item %s does not exist and will exit.' % (subjectID)
                return
            #print 'Basic Info: %s' % (basicInfo)
            with open(basic_json, fileMode) as movieBasicInfo:
                movieBasicInfo.write(basicInfo)
            print 'Movie basic info written to %s.' % (basic_json)
        else:
            print 'File %s exists and will pass.' % (basic_json)
            basicInfo = open(basic_json, 'r').read()

        '''
        Movie details HTML
        '''
        if os.path.exists(details_html) == False:
            print 'Crawling movie details html for ID %s...' % (subjectID)
            detailsHTML = detailsCrawler.crawlMovieDetailsHTMLPage(subjectID)
            #print 'Details HTML: %s' % (detailsHTML)
            with open(details_html, fileMode) as movieDetailsHTML:
                movieDetailsHTML.write(detailsHTML)
            print 'Movie details html written to %s.' % (details_html)
        else:
            print 'File %s exists and will pass.' % (details_html)
            detailsHTML = open(details_html, 'r').read()


        '''
        Movie user tags
        '''
        if os.path.exists(userTags_json) == False:
            print 'Parsing movie user tags for ID %s...' % (subjectID)
            userTags = userTagsParser.parseUserTagsFromHTML(detailsHTML)
            #print 'User Tags: %s' % (userTags)
            with open(userTags_json, fileMode) as movieUserTags:
                movieUserTags.write(userTags)
            print 'Movie user tags written to %s.' % (userTags_json)
        else:
            print 'File %s exists and will pass.' % (userTags_json)
            userTags = open(userTags_json, 'r').read()

        '''
        Movie others like
        '''
        if os.path.exists(othersLike_json) == False:
            print 'Parsing movie others like for ID %s...' % (subjectID)
            othersLike = othersLikeParser.parseOthersLikeFromHTML(detailsHTML)
            #print 'Others Like: %s' % (othersLike)
            with open(othersLike_json, fileMode) as movieOthersLike:
                movieOthersLike.write(othersLike)
            print 'Movie others like written to %s.' % (othersLike_json)
        else:
            print 'File %s exists and will pass.' % (othersLike_json)
            othersLike = open(othersLike_json, 'r').read()

        '''
        Movie awards HTML
        '''
        if os.path.exists(awards_html) == False:
            print 'Crawling movie awards html for ID %s...' % (subjectID)
            awardsHTML = awardsCrawler.crawlAwardslHTMLPage(subjectID)
            #print 'Awards HTML: %s' % (awardsHTML)
            with open(awards_html, fileMode) as movieAwardsHTML:
                movieAwardsHTML.write(awardsHTML)
            print 'Movie awards html written to %s.' % (awards_html)
        else:
            print 'File %s exists and will pass.' % (awards_html)
            awardsHTML = open(awards_html, 'r').read()

        '''
        Movie awards info
        '''
        if os.path.exists(awards_json) == False:
            print 'Parsing movie awards info for ID %s...' % (subjectID)
            awardsInfo = awardsParser.parseAwardsInfoFromHTML(awardsHTML)
            #print type(awardsInfo)
            #print 'Awards Info: %s' % (awardsInfo)
            with open(awards_json, fileMode) as movieAwardsInfo:
                movieAwardsInfo.write(str(awardsInfo))
            print 'Movie awards info written to %s.' % (awards_json)
        else:
            print 'File %s exists and will pass.' % (awards_json)
            awardsInfo = open(awards_json, 'r').read()

        '''
        Movie short comment number
        '''
        shortCommentsNum = shortCommentsCountParser.parseShortCommentsCountFromHTML(detailsHTML)
        #print 'Short Comments Number: %s' % (shortCommentsNum)

        '''
        Movie short comment HTML
        '''
        print 'Now crawling short comments for ID %s and will store into %s' % (subjectID, shortComment_htmls_dir)
        htmlFilesCrawled = shortCommentsCrawler.crawlShortCommentsBySubjectID(subjectID, shortCommentsNum, shortComment_htmls_dir)
        print 'Total %s short comment HTML files cralwed for ID %s.' % (htmlFilesCrawled, subjectID)

        '''
        Movie short comments
        '''
        if os.path.exists(shortComments_json) == False:
            print 'Now parsing short comments for ID %s' % (subjectID)
            shortComments, shortCommentsCount = shortCommentsParser.parseShortCommentsFromHTML(subjectID, shortCommentsNum, shortComment_htmls_dir)
            print 'Parsed %s short comments in total for ID %s.' % (shortCommentsCount, subjectID)
            #print 'Short comments: %s' % (shortComments)
            with open(shortComments_json, fileMode) as movieShortComments:
                movieShortComments.write(shortComments)
            print 'Movie short comments written to %s.' % (shortComments_json)
        else:
            print 'File %s exists and will pass.' % (shortComments_json)
            shortComments = open(shortComments_json, 'r').read()

        # Good Boy
        print 'Construction complete for %s!' % (subjectID)

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
    except Exception as e:
        print 'Excption occured: %s' % (e)

def insertMovieInfoToMysql(basicInfo, userTags, othersLike, shortComments, awardsInfo):
    pass

if len(sys.argv) != 2:
    print 'Usage: getAllMovieInfoById.py subjectID'

if len(sys.argv) == 2:
    getAllMovieInfoBySubjectID(sys.argv[1])
