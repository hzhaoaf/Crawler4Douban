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
import MySQLdb as mdb
import json

# import all user scripts
from crawlerModule import basicInfoCrawler
from crawlerModule import detailsCrawler
from crawlerModule import shortCommentsCrawler
from crawlerModule import awardsCrawler

from parserModule import awardsParser
from parserModule import userTagsParser
from parserModule import othersLikeParser
from parserModule import shortCommentsCountParser
from parserModule import shortCommentsParser

from databaseModule import basicInfoToMysql
from databaseModule import userTagsToMysql
from databaseModule import othersLikeToMysql
from databaseModule import shortCommentsToMysql
from databaseModule import awardsToMysql

timeout = 60
socket.setdefaulttimeout(timeout)

basicURL = 'http://api.douban.com/v2/movie/subject/'
detailsURL = 'http://movie.douban.com/subject/'

fileMode = 'w+'

def getAllMovieInfoBySubjectID(subjectID):
    try:
        # Some constants of file and directory names
        dir_prefix = os.path.expanduser('~') + '/OpenData/movie_items/itemsByID/'

        basic_json = 'basic.json'
        details_html = 'details_html.html'
        awards_html = 'awards_html.html'
        shortComment_htmls_dir= 'short_comment_htmls'
        userTags_json = 'userTags.json'
        othersLike_json = 'othersLike.json'
        shortComments_json = 'shortComments.json'
        awards_json = 'awards.json'

        # Make a directory for each subject
        if not os.path.isdir(dir_prefix):
            print 'Will create directory %s' % (dir_prefix)
            os.makedirs(dir_prefix)


        shortComment_htmls_dir = dir_prefix + subjectID + '/' + shortComment_htmls_dir

        basic_json = dir_prefix + subjectID + '/' + basic_json
        details_html = dir_prefix + subjectID + '/' + details_html
        awards_html = dir_prefix + subjectID + '/' + awards_html
        userTags_json = dir_prefix + subjectID + '/' + userTags_json
        othersLike_json = dir_prefix + subjectID + '/' + othersLike_json
        shortComments_json = dir_prefix + subjectID + '/' + shortComments_json
        awards_json = dir_prefix + subjectID + '/' + awards_json

        # Go, boy, Go
        print 'Now trying to construct movie info for ID %s...' % (subjectID)

        '''
        Movie basic info
        '''
        if os.path.exists(basic_json) == False:
            print 'Getting movie basic info for ID %s...' % (subjectID)
            basicInfo = basicInfoCrawler.getBasicMovieInfoBySubjectID(subjectID)

            if basicInfo == None:
                print 'Movie item %s does not exist and will exit.' % (subjectID)
                return

            #print 'Basic Info: %s' % (basicInfo)
            basicInfoJson = json.loads(basicInfo)

            if not os.path.isdir(dir_prefix + subjectID):
                print 'Will create directory %s' % (dir_prefix + subjectID)
                os.mkdir(dir_prefix + subjectID)

            with open(basic_json, fileMode) as movieBasicInfo:
                movieBasicInfo.write(basicInfo)
            print 'Movie basic info written to %s.' % (basic_json)
        else:
            print 'File %s exists and will pass.' % (basic_json)
            #basicInfo = open(basic_json, 'r').read()
            basicInfoJson = json.load(file(basic_json))

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
            userTagsJson = json.loads(userTags)

            with open(userTags_json, fileMode) as movieUserTags:
                movieUserTags.write(userTags)
            print 'Movie user tags written to %s.' % (userTags_json)
        else:
            print 'File %s exists and will pass.' % (userTags_json)
            #userTags = open(userTags_json, 'r').read()
            userTagsJson = json.load(file(userTags_json))

        '''
        Movie others like
        '''
        if os.path.exists(othersLike_json) == False:
            print 'Parsing movie others like for ID %s...' % (subjectID)
            othersLike = othersLikeParser.parseOthersLikeFromHTML(detailsHTML)
            #print 'Others Like: %s' % (othersLike)
            othersLikeJson = json.loads(othersLike)

            with open(othersLike_json, fileMode) as movieOthersLike:
                movieOthersLike.write(othersLike)
            print 'Movie others like written to %s.' % (othersLike_json)
        else:
            print 'File %s exists and will pass.' % (othersLike_json)
            #othersLike = open(othersLike_json, 'r').read()
            othersLikeJson = json.load(file(othersLike_json))

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
            awardsInfoJson = awardsInfo

            with open(awards_json, fileMode) as movieAwardsInfo:
                movieAwardsInfo.write(json.dumps(awardsInfo))
            print 'Movie awards info written to %s.' % (awards_json)
        else:
            print 'File %s exists and will pass.' % (awards_json)
            #awardsInfo = open(awards_json, 'r').read()
            awardsInfoJson = json.load(file(awards_json))

        '''
        Movie short comment number
        '''
        shortCommentsNum = shortCommentsCountParser.parseShortCommentsCountFromHTML(detailsHTML)
        #print 'Short Comments Number: %s' % (shortCommentsNum)

        '''
        Movie short comment HTML
        '''
        print 'Now crawling short comments for ID %s and will store into %s' % (subjectID, shortComment_htmls_dir)
        if not os.path.exists(shortComment_htmls_dir):
            htmlFilesCrawled = shortCommentsCrawler.crawlShortCommentsBySubjectID(subjectID, shortCommentsNum, shortComment_htmls_dir)
            print 'Total %s short comment HTML files cralwed for ID %s.' % (htmlFilesCrawled, subjectID)
        else:
            print 'Short comments already crawled and will pass.'

        '''
        Movie short comments
        '''
        if os.path.exists(shortComments_json) == False:
            print 'Now parsing short comments for ID %s' % (subjectID)
            shortComments, shortCommentsCount = shortCommentsParser.parseShortCommentsFromHTML(subjectID, shortCommentsNum, shortComment_htmls_dir)
            print 'Parsed %s short comments in total for ID %s.' % (shortCommentsCount, subjectID)
            #print 'Short comments: %s' % (shortComments)
            shortCommentsJson = json.loads(shortComments)

            with open(shortComments_json, fileMode) as movieShortComments:
                movieShortComments.write(shortComments)
            print 'Movie short comments written to %s.' % (shortComments_json)
        else:
            print 'File %s exists and will pass.' % (shortComments_json)
            #shortComments = open(shortComments_json, 'r').read()
            shortCommentsJson = json.load(file(shortComments_json))

        # Good Boy
        print 'Construction complete for %s!' % (subjectID)

        print 'Echo the movie info...'

        print 'Basic information:'
        print type(basicInfoJson)
        #print type(eval(basicInfo))
        #print basicInfo

        print 'User tags:'
        print type(userTagsJson)
        #print type(eval(userTags))
        #print userTags

        print 'Others like:'
        print type(othersLikeJson)
        #print type(eval(othersLike))
        #print othersLike

        print 'Short comments:'
        print type(shortCommentsJson)
        #print type(eval(shortComments))
        #print shortComments

        print 'Awards Info:'
        print type(awardsInfoJson)
        #print type(eval(awardsInfo))
        #print awardsInfo
        #print str(awardsInfo)


        #return subjectID, eval(basicInfo), eval(userTags), eval(othersLike), eval(shortComments), eval(awardsInfo)
        #return subjectID, basicInfo, userTags, othersLike, shortComments, awardsInfo
        return subjectID, basicInfoJson, userTagsJson, othersLikeJson, shortCommentsJson, awardsInfoJson

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

# Database Section

hostName = 'your_host_name'
userName = 'your_database_user_name'
userPassword = 'your_database_password'
databaseName = 'your_database_name'

basicInfoTableName = 'movie_items'

def initDB(hostName, userName, userPassword, databaseName):
    try:
        print 'Trying to get database connection...'

        con = mdb.connect(hostName, userName, userPassword, databaseName)

        # Codec settings
        con.set_character_set('utf8')

        cur = con.cursor()

        # Again with the codecs
        cur.execute('SET NAMES utf8')
        cur.execute('SET CHARACTER SET utf8')
        cur.execute('SET character_set_connection=utf8')

        print 'Got a database cursor successfully!'

        print 'Creating database tables...'
        cur.execute(basicInfoToMysql.create_movie_items_table)
        cur.execute(shortCommentsToMysql.create_short_comments_table)
        cur.execute(awardsToMysql.create_movie_awards_table)
        print 'Done!'

        return con, cur

    except Exception as e:
        print 'Excption occured: %s' % (e)

def closeDB(databaseConnection, databaseCursor):
    try:
        print 'Now Closing database connection...'

        databaseCursor.close()
        databaseConnection.close()

        print 'Database closed successfully!'

    except Exception as e:
        print "Error when closing database: %s" % (e)


def insertMovieInfoToMysql(subjectID, basicInfo, userTags, othersLike, shortComments, awardsInfo):
    print 'Trying to insert movie info into database...'

    databaseConnection, databaseCursor = initDB(hostName, userName, userPassword, databaseName)

    basicInfoToMysql.insertBasicInfoToMysql(basicInfo, databaseCursor)
    userTagsToMysql.insertUserTagsToMysql(userTags, databaseCursor, subjectID)
    othersLikeToMysql.insertOthersLikeToMysql(othersLike, databaseCursor, subjectID)
    shortCommentsToMysql.insertShortCommentsToMysql(shortComments, databaseCursor, subjectID)
    awardsToMysql.insertMovieAwardsToMysql(awardsInfo, databaseCursor, subjectID)

    databaseConnection.commit()

    closeDB(databaseConnection, databaseCursor)

    print 'Done with the database operations!'

'''
if len(sys.argv) != 2:
    print 'Usage: getAllMovieInfoById.py subjectID'

if len(sys.argv) == 2:
    subjectID, basicInfo, userTags, othersLike, shortComments, awardsInfo = getAllMovieInfoBySubjectID(sys.argv[1])
    insertMovieInfoToMysql(subjectID, basicInfo, userTags, othersLike, shortComments, awardsInfo)
'''
