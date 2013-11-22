#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
A script to import JSON data to Mysql record of Douban Movie items
'''

import json
import MySQLdb as mdb
import sys
import glob
import os
import time

# Test MySQLdb module
'''
print "Test mysql..."
try:
    con = mdb.connect('localhost', 'lihang', 'lilihang', 'test_json_to_mysql')
    cur = con.cursor()
    cur.execute("SELECT VERSION()")
    data = cur.fetchone()
    print "Database version: %s" % data
except mdb.Error, e:
    print "Error: %d %s" % (e.args[0], e.args[1])
    sys.exit(1)
finally:
    if con:
        con.close()
'''

# Test glob module
'''
testJsonFileList = glob.glob('./jsonData/*.json')
print testJsonFileList
'''

# Simple Load
'''
jsonFile = file("test.json")
jsonString = json.load(jsonFile)
print "Contents by json.load method:"
print jsonString
jsonFile.close()
'''

# Using JSONDecoder
'''
jsonFile = file("test.json")
jsonSource = jsonFile.read()
#print "Contents by pure File.read method:"
#print jsonSource

jsonTarget = json.JSONDecoder().decode(jsonSource)
#print "Contents after using JSONDecoder method:"
#print jsonTarget

jsonKeys = jsonTarget.keys()

print "JSON keys:"
#print jsonTarget.keys()

insertDict = {}

for jsonKey in jsonKeys:
    #print jsonKey
    fieldValue = jsonTarget[jsonKey]
    if hasattr(fieldValue, 'keys'):
        subKeys = fieldValue.keys()
        for subKey in subKeys:
            print subKey
            insertDict[subKey] = fieldValue[subKey]
    else:
        print jsonKey
        insertDict[jsonKey] = fieldValue



    if jsonKey == "genres":
        print fieldValue[0] + fieldValue[1] + fieldValue[2]
    elif jsonKey == "do_count":
        print fieldValue
    elif jsonKey == "rating":
        print "rating: " + str(fieldValue["max"]) + " " + str(fieldValue["average"]) + " " + str(fieldValue["stars"]) + " " + str(fieldValue["min"])
        subKeys = fieldValue.keys()
        for subKey in subKeys:
            print subKey
            print fieldValue[subKey]
    elif jsonKey == "images":
        subKeys = fieldValue.keys()
        for subKey in subKeys:
            print subKey
            print fieldValue[subKey]
    else:
        print fieldValue

jsonFile.close()
'''

# Test if our dict works
'''
print "Fields will be inserted are:"
insertKeys = insertDict.keys()
for insertKey in insertKeys:
    print insertKey + ":"
    print insertDict[insertKey]
'''

# Create Database and Tables
databaseName = "douban_movie";
create_douban_movie_items_database = "CREATE DATABASE IF NOT EXISTS " + databaseName + " character set utf8 collate utf8_unicode_ci"
#print create_douban_movie_items_database

create_movie_items_table = "CREATE TABLE IF NOT EXISTS \
        movie_items( \
                    rating_max INT, \
                    rating_average FLOAT, \
                    rating_stars VARCHAR(20), \
                    rating_min INT, \
                    reviews_count INT, \
                    wish_count INT, \
                    douban_site VARCHAR(50), \
                    year VARCHAR(10), \
                    image_small VARCHAR(100), \
                    image_large VARCHAR(100), \
                    image_medium VARCHAR(100), \
                    subject_url VARCHAR(50), \
                    subject_id VARCHAR(50) PRIMARY KEY, \
                    mobile_url VARCHAR(50), \
                    title VARCHAR(100), \
                    do_count INT, \
                    seasons_count INT, \
                    schedule_url VARCHAR(50), \
                    episodes_count INT, \
                    genres VARCHAR(50), \
                    current_season INT, \
                    collect_count INT, \
                    casts VARCHAR(2000), \
                    countries VARCHAR(20), \
                    original_title VARCHAR(100), \
                    summary TEXT, \
                    summary_segmentation TEXT, \
                    subtype VARCHAR(10), \
                    directors VARCHAR(1000), \
                    comments_count INT, \
                    ratings_count INT, \
                    aka VARCHAR(50), \
                    user_tags VARCHAR(500), \
                    others_like VARCHAR(1000) \
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE utf8_unicode_ci; \
                    "

#print create_movie_items_table

def processingJsonFilesInDirectory(jsonDirectory, databaseConnection, databaseCursor):
    # To deprecate 'local variable xxx referenced before assignment'
    global numberOfJsonFiles
    global fileListDetialOfDirectories

    try:
        jsonFileList = getJsonFileListFromDirectory(jsonDirectory)
        print 'Will process %d JSON Files...' % (len(jsonFileList))
        numberOfJsonFiles += len(jsonFileList)
        fileListDetialOfDirectories += '%s has %d JSON Files.\n' % (jsonDirectory, len(jsonFileList))

        # Log files to be processed
        for jsonFile in jsonFileList:
            toBeProcessedJsonList.write(jsonFile + newLineToken)

        # Process happens here
        for jsonFile in jsonFileList:
            print 'Now processing %s' % (jsonFile)
            insertMysqlRecordFromJson(jsonFile, databaseCursor)

        # Commit the transaction, do remember for the InnoDB Engine
        databaseConnection.commit()

    except Exception as e:
        print e.args

def getJsonFileListFromDirectory(jsonDirectory):
    try:
        jsonFileList = glob.glob(jsonDirectory+'/*.json')
        return jsonFileList
    except IOError:
        print "IOError Occured!"

# Insert record to Mysql
# This is the template for defining fields
'''
insertStringTemplate = (
                    "INSERT IGNORE INTO movie_items(rating_max,"
                                        "rating_average,"
                                        "rating_stars,"
                                        "rating_min,"
                                        "reviews_count,"
                                        "wish_count,"
                                        "douban_site,"
                                        "year,"
                                        "image_small,"
                                        "image_large,"
                                        "image_medium,"
                                        "subject_url,"
                                        "subject_id,"
                                        "mobile_url,"
                                        "title,"
                                        "do_count,"
                                        "seasons_count,"
                                        "schedule_url,"
                                        "episodes_count,"
                                        "genres,"
                                        "current_season,"
                                        "collect_count,"
                                        "casts,"
                                        "countries,"
                                        "original_title,"
                                        "summary,"
                                        "summary_segmentation,"
                                        "subtype,"
                                        "directors,"
                                        "comments_count,"
                                        "ratings_count,"
                                        "aka,"
                                        "user_tags,"
                                        "others_like) "
                                    "values (insertDict['rating_max'],"
                                           "insertDict['rating_average'],"
                                           "insertDict['rating_stars'],"
                                           "insertDict['rating_min'],"
                                           "insertDict['reviews_count'],"
                                           "insertDict['wish_count'],"
                                           "insertDict['douban_site'],"
                                           "insertDict['year'],"
                                           "insertDict['image_small'],"
                                           "insertDict['image_large'],"
                                           "insertDict['image_medium'],"
                                           "insertDict['subject_url'],"
                                           "insertDict['subject_id'],"
                                           "insertDict['mobile_url'],"
                                           "insertDict['title'],"
                                           "insertDict['do_count'],"
                                           "insertDict['seasons_count'],"
                                           "insertDict['schedule_url'],"
                                           "insertDict['episodes_count'],"
                                           "insertDict['genres'],"
                                           "insertDict['current_season'],"
                                           "insertDict['casts'],"
                                           "insertDict['countries'],"
                                           "insertDict['original_title'],"
                                           "insertDict['summary'],"
                                           "insertDict['summary_segmentation'],"
                                           "insertDict['subtype'],"
                                           "insertDict['directors'],"
                                           "insertDict['comments_count'],"
                                           "insertDict['ratings_count'],"
                                           "insertDict['aka'],"
                                           "insertDict['user_tags'],"
                                           "insertDict['others_like']);"
                                           )


print insertStringTemplate
'''

# This is the real SQL query
insertStringWithValues = (
                    "INSERT IGNORE INTO movie_items(rating_max,"
                                        "rating_average,"
                                        "rating_stars,"
                                        "rating_min,"
                                        "reviews_count,"
                                        "wish_count,"
                                        "douban_site,"
                                        "year,"
                                        "image_small,"
                                        "image_large,"
                                        "image_medium,"
                                        "subject_url,"
                                        "subject_id,"
                                        "mobile_url,"
                                        "title,"
                                        "do_count,"
                                        "seasons_count,"
                                        "schedule_url,"
                                        "episodes_count,"
                                        "genres,"
                                        "current_season,"
                                        "collect_count,"
                                        "casts,"
                                        "countries,"
                                        "original_title,"
                                        "summary,"
                                        "summary_segmentation,"
                                        "subtype,"
                                        "directors,"
                                        "comments_count,"
                                        "ratings_count,"
                                        "aka,"
                                        "user_tags,"
                                        "others_like) "
                                    "values (%d,"
                                           "%f,"
                                           "%s,"
                                           "%d,"
                                           "%d,"
                                           "%d,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%d,"
                                           "%s,"
                                           "%s,"
                                           "%d,"
                                           "%d,"
                                           "%s,"
                                           "%d,"
                                           "%s,"
                                           "%d,"
                                           "%d,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%d,"
                                           "%d,"
                                           "%s,"
                                           "%s,"
                                           "%s);"
                                           )


#print insertStringWithValues

insertStringWithAllStringValues = (
                    "INSERT IGNORE INTO movie_items(rating_max,"
                                        "rating_average,"
                                        "rating_stars,"
                                        "rating_min,"
                                        "reviews_count,"
                                        "wish_count,"
                                        "douban_site,"
                                        "year,"
                                        "image_small,"
                                        "image_large,"
                                        "image_medium,"
                                        "subject_url,"
                                        "subject_id,"
                                        "mobile_url,"
                                        "title,"
                                        "do_count,"
                                        "seasons_count,"
                                        "schedule_url,"
                                        "episodes_count,"
                                        "genres,"
                                        "current_season,"
                                        "collect_count,"
                                        "casts,"
                                        "countries,"
                                        "original_title,"
                                        "summary,"
                                        "summary_segmentation,"
                                        "subtype,"
                                        "directors,"
                                        "comments_count,"
                                        "ratings_count,"
                                        "aka,"
                                        "user_tags,"
                                        "others_like) "
                                    "values (%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s);"
                                           )


#print insertStringWithAllStringValues

def insertMysqlRecordFromJson(jsonFileName, databaseCursor):
    global processedFiles
    try:
        # Get raw JSON
        jsonString = getJsonStringFromJsonFile(jsonFileName)

        # Get seperate fields of JSON
        insertValues = getSeperateFieldFromJson(jsonString)

        # Concatenate the Query for logging
        mysqlInsertQueryString = insertStringWithAllStringValues + str(insertValues) + newLineToken
        logFile.write(mysqlInsertQueryString)

        #databaseCursor.execute(insertStringWithValues, insertValues)
        affectedRows = databaseCursor.execute(insertStringWithAllStringValues, insertValues)

        # Processed one JSON file
        processedJsonFileName = jsonFileName + newLineToken
        processedJsonList.write(processedJsonFileName)
        processedFiles += 1

    except IOError, e:
        print "IOError occured! %d %s" % (e.args[0], e.args[1])
    except mdb.Error, e:
        print "Database Error: %d %s" % (e.args[0], e.args[1])
    except Exception, e:
        print "Database Error: %d %s" % (e.args[0], e.args[1])

def getSeperateFieldFromJson(jsonString):
    try:
        #print 'Now extracting seperate fields...'
        jsonKeys = jsonString.keys()

        insertDict = {}

        for jsonKey in jsonKeys:
            fieldValue = jsonString[jsonKey]
            if hasattr(fieldValue, 'keys'):
                subKeys = fieldValue.keys()
                for subKey in subKeys:
                    #print subKey
                    insertDict[subKey] = fieldValue[subKey]
            else:
                #print jsonKey
                insertDict[jsonKey] = fieldValue

        # Check insertDict type
        #print type(insertDict)

        # Return values as a tuple for insert
        # Casts and directors will use their related IDs
        # However for debugging, we use a Long String here
        #insertDict['casts'] = '..'.join(str(d) for d in insertDict['casts'])
        #insertDict['directors'] = '..'.join(str(d) for d in insertDict['directors'])
        #insertDict['casts'] = str(insertDict['casts'])
        #insertDict['directors'] = str(insertDict['directors'])
        #insertDict['summary'] = ''
        insertDict['genres'] = u'￥'.join(insertDict['genres']).encode('utf-8').strip()
        insertDict['countries'] = u'￥'.join(insertDict['countries']).encode('utf-8').strip()
        insertDict['aka'] = u'￥'.join(insertDict['aka']).encode('utf-8').strip()
        insertDict['user_tags'] = ''
        insertDict['others_like'] = ''

        '''
        print insertDict['max']
        print insertDict['average']
        print insertDict['stars']
        print insertDict['min']
        print insertDict['reviews_count']
        print insertDict['wish_count']
        print insertDict['douban_site']
        print insertDict['year']
        print insertDict['small']
        print insertDict['large']
        print insertDict['medium']
        print insertDict['alt']
        print insertDict['id']
        print insertDict['mobile_url']
        print insertDict['title']
        print insertDict['do_count']
        print insertDict['seasons_count']
        print insertDict['schedule_url']
        print insertDict['episodes_count']
        print insertDict['genres']
        print insertDict['current_season']
        print insertDict['collect_count']
        print insertDict['casts']
        print insertDict['countries']
        print insertDict['original_title']
        print insertDict['summary']
        print insertDict['subtype']
        print insertDict['directors']
        print insertDict['comments_count']
        print insertDict['ratings_count']
        print insertDict['aka']
        '''

        directorsList = []
        directorsString = ''
        #print type(insertDict['directors'])
        #print insertDict['directors']
        #print len(insertDict['directors'])
        '''
        for director in insertDict['directors']:
            #print director
            for directorsKey in director.keys():
                #print directorsKey
                directorsField = director[directorsKey]
                if directorsField == None:
                    directorsField = 'None'
                if hasattr(directorsField, 'keys'):
                    directorSubKeys = directorsField.keys()
                    for directorSubKey in directorSubKeys:
                        #print directorSubKey
                        if directorsField[directorSubKey] == None:
                            directorsField[directorSubKey] = 'None'
                        directorsString += '<>'
                        directorsString += directorsField[directorSubKey]
                else:
                    directorsString += u'￥'
                    directorsString += directorsField
        '''
        for director in insertDict['directors']:
            if director['name'] == None:
                director['name'] = 'None'
            #directorsString += u'￥'
            #directorsString += director['name']
            directorsList.append(director['name'])

        directorsString = u'￥'.join(directorsList).encode('utf-8').strip()

        castsList = []
        castsString = ''
        #print type(insertDict['casts'])
        #print insertDict['casts']
        #print len(insertDict['casts'])
        '''
        for cast in insertDict['casts']:
            #print cast
            for castsKey in cast.keys():
                #print castsKey
                castsField = cast[castsKey]
                if castsField == None:
                    castsField = 'None'
                if hasattr(castsField, 'keys'):
                    castSubKeys = castsField.keys()
                    for castSubKey in castSubKeys:
                        #print castSubKey
                        if castsField[castSubKey] == None:
                            castsField[castSubKey] = 'None'
                        castsString += '<>'
                        castsString += castsField[castSubKey]
                else:
                    castsString += u'￥'
                    castsString += castsField
        '''
        for cast in insertDict['casts']:
            if cast['name'] == None:
                cast['name'] = 'None'
            #castsString += u'￥'
            #castsString += cast['name']
            castsList.append(cast['name'])

        castsString = u'￥'.join(castsList).encode('utf-8').strip()


        #print directorsString
        #print castsString

        insertDict['directors'] = directorsString
        insertDict['casts'] = castsString

        insertTuple = (insertDict['max'], insertDict['average'], insertDict['stars'],
                       insertDict['min'], insertDict['reviews_count'], insertDict['wish_count'],
                       insertDict['douban_site'], insertDict['year'], insertDict['small'],
                       insertDict['large'], insertDict['medium'], insertDict['alt'],
                       insertDict['id'], insertDict['mobile_url'], insertDict['title'],
                       insertDict['do_count'], insertDict['seasons_count'], insertDict['schedule_url'],
                       insertDict['episodes_count'], insertDict['genres'], insertDict['current_season'],
                       insertDict['collect_count'], insertDict['casts'], insertDict['countries'],
                       insertDict['original_title'], insertDict['summary'], insertDict['summary'],
                       insertDict['subtype'],
                       insertDict['directors'], insertDict['comments_count'], insertDict['ratings_count'],
                       insertDict['aka'], insertDict['user_tags'], insertDict['others_like']
                       )
        #print len(insertTuple)
        #print insertTuple
        return insertTuple
    except Exception as e:
        print "Exception occured!"
        print type(e)
        print e.args
        #print "Error: %d %s" % (e.errno, e.strerror)


def getJsonStringFromJsonFile(jsonFileName):
    try:
        jsonFile = file(jsonFileName)
        jsonString = json.load(jsonFile)
        jsonFile.close()
        return jsonString
    except IOError:
        print "IOError occured!"
    except ValueError, e:
        print "Error %d %s" % (e.args[0], e.args[1])

def getJsonStringFromJsonFileUsingDecoder(jsonFileName):
    try:
        jsonFile = file(jsonFileName)
        jsonSource = jsonFile.read()
        jsonTarget = json.JSONDecoder().decode(jsonSource)
        jsonFile.close()
        return jsonTarget
    except IOError:
        print "IOError occured!"

# Main Routine
if __name__ == '__main__':
    jsonDirectorys = ['./jsonData'] # You can add more directories here into the list

	mysqlLogFile = './mysqlQuery.sql'
    fileMode = 'w+'
    newLineToken = '\n'

	tableName = 'movie_items'
    hostName = 'your_host_name' # Typically use 'localhost'
    userName = 'your_user_name'
    userPassword = 'your_user_password'
    databaseName = 'your_database_name'

	numberOfJsonFiles = 0
    processedFiles = 0
    fileListDetialOfDirectories = ''

    toBeProcessedFileList = './toBeProcessedJsonFiles'
    processedJsonFileList = './processedJsonFiles'

    # Profiling
    startTime = 0
    endTime = 0

    try:
        con = mdb.connect(hostName, userName, userPassword, databaseName)
        # Careful with codecs
        con.set_character_set('utf8')

        cur = con.cursor()
        # Aagin the codecs
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')
        # Create Table movie_items if necessary
        stmt = """
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_name = '{0}'
                """.format(tableName.replace('\'','\'\''))
        cur.execute(stmt)
        result = cur.fetchone()[0]
        #print type(result)
        #print result
        if result:
            print 'Table %s already exists and will not create again.' % (tableName)
        else:
            print 'Table %s will be created...' % (tableName)
            cur.execute(create_movie_items_table)

        # For multiple databases and same tableName used, create table anyway
        cur.execute(create_movie_items_table)

        # Open file for logging
        logFile = open(mysqlLogFile,fileMode)
        processedJsonList = open(processedJsonFileList, fileMode)
        toBeProcessedJsonList = open(toBeProcessedFileList, fileMode)

        # Start Profiling
        startTime = time.time()

        # Go and insert records
        for jsonDirectory in jsonDirectorys:
            if os.path.exists(jsonDirectory):
                print 'Now processing %s...' % (jsonDirectory)
                processingJsonFilesInDirectory(jsonDirectory, con, cur)
            else:
                print 'The directory %s will be processed does not exist...' % (jsonDirectory)
                raise Exception

        # Close cursor and connection
        cur.close()
        con.close()

        #End Profiling
        endTime = time.time()

        # Close Log File
        logFile.close()
        processedJsonList.close()
        toBeProcessedJsonList.close()

        print '\nReport:'
        print 'Start time: %s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(startTime)))
        print 'Have %d files to process' % (numberOfJsonFiles)
        print 'Details are:'
        print fileListDetialOfDirectories
        print 'Processed %d files in total' % (processedFiles)
        print 'End time: %s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(endTime)))
        print 'Cost %.2f minutes.' % ((endTime - startTime) / 60)
        print 'All Done!'
    except IOError, e:
        print "IOError occured! %d %s" % (e.args[0], e.args[1])
    except mdb.Error, e:
        print "Error: %d %s" % (e.args[0], e.args[1])
