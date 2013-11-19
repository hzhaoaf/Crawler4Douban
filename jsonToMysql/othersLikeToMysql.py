#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
A script to import movie others like information to Mysql record of Douban Movie items
'''

import json
import MySQLdb as mdb
import sys
import glob
import os
import time
import string


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
        print 'Exception: %s' %(e)

def getJsonFileListFromDirectory(jsonDirectory):
    try:
        jsonFileList = glob.glob(jsonDirectory+'/*.json')
        return jsonFileList
    except IOError as e:
        print "IOError Occured: %s" % (e)

# Insert record to Mysql
updateStringWithAllStringValues = (
                    "UPDATE movie_items SET others_like=%s "
                                        "WHERE subject_id=%s "
                                           )


#print updateStringWithAllStringValues

def insertMysqlRecordFromJson(jsonFileName, databaseCursor):
    global processedFiles
    try:
        # Get raw JSON
        jsonString = getJsonStringFromJsonFile(jsonFileName)
        #print jsonString

        # Get seperate fields of JSON
        insertValues = getSeperateFieldFromJson(jsonFileName, jsonString)
        movie_subject_id = insertValues[1]

        #print type(insertValues)
        #print insertValues

        # Concatenate the Query for logging
        mysqlUpdateQueryString = updateStringWithAllStringValues + str(insertValues) + newLineToken
        #print mysqlUpdateQueryString
        logFile.write(mysqlUpdateQueryString)

        # Check if we have the record for the specified subject_id
        fetchSqlParams = (movie_subject_id)
        rowCount = databaseCursor.execute("SELECT * FROM movie_items WHERE subject_id = %s;", fetchSqlParams)
        if (rowCount > 0):
            # Got a record, insert to database and log the subject_id
            print 'Insert othersLike for ID: %s' % (movie_subject_id)
            affectedRows = databaseCursor.execute(updateStringWithAllStringValues, insertValues)
            successIds.write(movie_subject_id + newLineToken)
        else:
            # No record, log the subject_id
            print 'No record for ID: %s' % (movie_subject_id)
            failIds.write(movie_subject_id + newLineToken)


        # Processed one JSON file
        processedJsonFileName = jsonFileName + newLineToken
        processedJsonList.write(processedJsonFileName)
        processedFiles += 1

    except IOError, e:
        print "IOError occured: %s" % (e)
    except mdb.Error, e:
        print "Database Error: %s" % (e)
    except Exception, e:
        print "Database Error: %s" % (e)

def getSeperateFieldFromJson(jsonFileName, jsonString):
    try:
        # Get the subject id from jsonFileName
        movie_subject_id = getMovieSubjectId(jsonFileName)

        print 'Movie Subject ID: %s' % (movie_subject_id)

        #print 'Now extracting seperate fields...'
        jsonKeys = jsonString.keys()

        insertDict = {}
        insertList = []
        othersLikeString = ''

        for jsonKey in jsonKeys:
            fieldValue = jsonString[jsonKey]
            if hasattr(fieldValue, 'keys'):
                subKeys = fieldValue.keys()
                for subKey in subKeys:
                    #othersLikeString += subKey + '<>' + fieldValue[subKey] + u'￥'
                    insertList.append(subKey + '<>' + fieldValue[subKey])
                    insertDict[subKey] = fieldValue[subKey]
            else:
                #othersLikeString += jsonKey + ':' + fieldValue + '..'
                insertList.append(jsonKey + '<>' + fieldValue)
                insertDict[jsonKey] = fieldValue

        othersLikeString = u'￥'.join(insertList).encode('utf-8').strip()

        insertTuple = (othersLikeString,movie_subject_id)

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

def getMovieSubjectId(jsonFileName):
    try:
        #print 'Full path Name: %s' % (jsonFileName)
        jsonFileName = os.path.basename(jsonFileName)
        #print 'Basename: %s' % (jsonFileName)

        movieSubjectId = jsonFileName.replace('otherslike-', '').replace('.json', '')
        #print 'movieSubjectId extracted from jsonFileName: %s' % (movieSubjectId)

        return movieSubjectId
    except Exception, e:
        print "Exception: %s" % (e)


# Main Routine
if __name__ == '__main__':
    jsonDirectorys = os.listdir('../result_others_like')
    #jsonDirectorys = ['./othersLikeTest']

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

    insertedUserTagsSubjectIds = './successInsertedIds'
    noInsertedUserTagsSubjectIds = './failInsertedIds'

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

        successIds = open(insertedUserTagsSubjectIds, fileMode)
        failIds = open(noInsertedUserTagsSubjectIds, fileMode)

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
        successIds.close()
        failIds.close()

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
