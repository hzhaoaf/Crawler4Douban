#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
A script to import movie awards to Mysql record of Douban Movie items
'''

import json
import MySQLdb as mdb
import sys
import glob
import os
import time


# Create Database and Tables
databaseName = "douban_movie";
create_douban_movie_items_database = "CREATE DATABASE IF NOT EXISTS " + databaseName + " character set utf8 collate utf8_unicode_ci"
#print create_douban_movie_items_database

create_movie_awards_table = "CREATE TABLE IF NOT EXISTS \
        `movie_awards`( \
                    `subject_id` VARCHAR(50) NOT NULL, \
                    `movie_name` VARCHAR(150), \
                    `award_items` VARCHAR(5000), \
                    PRIMARY KEY (`subject_id`) \
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE utf8_unicode_ci; \
                    "

#print create_movie_items_table

# Insert record to Mysql
insertStringWithAllStringValues = (
                    "INSERT IGNORE INTO movie_awards(subject_id,"
                                        "movie_name,"
                                        "award_items) "
                                    "values (%s,"
                                           "%s,"
                                           "%s);"
                                           )


#print insertStringWithAllStringValues

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
        #jsonFileList = glob.glob(jsonDirectory+'/*.json')
        jsonFileList = glob.glob(jsonDirectory+'/*.txt')
        return jsonFileList
    except IOError:
        print "IOError Occured!"


def insertMysqlRecordFromJson(jsonFileName, databaseCursor):
    global processedFiles
    try:
        # Get raw JSON
        #jsonString = getJsonStringFromJsonFile(jsonFileName)
        jsonString = concatenatetJsonStringFromJsonFile(jsonFileName)

        #print type(jsonString)
        #print jsonString

        # Get seperate fields of JSON
        insertValues = getSeperateFieldFromJson(jsonFileName, jsonString)

        #print type(insertValues)
        #print insertValues

        # Concatenate the Query for logging
        mysqlInsertQueryString = insertStringWithAllStringValues + str(insertValues) + newLineToken
        logFile.write(mysqlInsertQueryString)

        #databaseCursor.execute(insertStringWithValues, insertValues)
        #affectedRows = databaseCursor.execute(insertStringWithAllStringValues, insertValues)
        affectedRows = databaseCursor.executemany(insertStringWithAllStringValues, insertValues)

        # Processed one JSON file
        processedJsonFileName = jsonFileName + newLineToken
        processedJsonList.write(processedJsonFileName)
        processedFiles += 1

    except IOError, e:
        print "IOError: %s" % (e)
    except mdb.Error, e:
        print "mdb Error: %s" % (e)
    except Exception, e:
        print "Database Error: %s" % (e)

def getSeperateFieldFromJson(jsonFileName, jsonString):
    try:
        #print 'Now extracting seperate fields...'
        jsonKeys = jsonString.keys()
        #print type(jsonKeys)

        '''
        for jsonKey in jsonKeys:
            print jsonKey
            print jsonString[jsonKey]
        '''

        insertDict = {}
        insertList = []

        for jsonKey in jsonKeys:
            fieldValue = jsonString[jsonKey]
            fieldValue = json.loads(fieldValue)
            #print type(fieldValue)
            if  hasattr(fieldValue, 'keys'):
                subKeys = fieldValue.keys()
                for subKey in subKeys:
                    #print subKey
                    insertDict[subKey] = fieldValue[subKey]
                    #print insertDict[subKey]
            else:
                #print jsonKey
                insertDict[jsonKey] = fieldValue

            #print type(insertDict['award_items'])
            insertDict['award_items'] = str(insertDict['award_items'])

            insertTuple = (insertDict['subject_id'], insertDict['movie_name'], insertDict['award_items'])

            #print insertTuple

            insertList.append(insertTuple)

        return insertList
    except Exception as e:
        print "Exception occured!"
        print type(e)
        print e.args


def getJsonStringFromJsonFile(jsonFileName):
    try:
        jsonFile = file(jsonFileName)
        jsonString = json.load(jsonFile)
        jsonFile.close()
        return jsonString
    except IOError:
        print "IOError occured!"
    except ValueError, e:
        print "Error %s" % (e)

def concatenatetJsonStringFromJsonFile(jsonFileName):
    try:
        retDict = {}
        iterator = 0
        jsonFile = file(jsonFileName)
        jsonLines = jsonFile.readlines()
        for jsonLine in jsonLines:
            #print type(jsonLine)
            #print jsonLine
            retDict[str(iterator)] = jsonLine
            iterator = iterator + 1

        jsonFile.close()
        return retDict
        #return json.dumps(retDict)
    except Exception, e:
        print "Exception: %s" % (e)


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
    jsonDirectorys = ['./awards_info']
    #jsonDirectorys = ['../jsonTest']

    mysqlLogFile = './mysqlQuery.sql'
    fileMode = 'w+'
    newLineToken = '\n'

    tableName = 'movie_awards'
    hostName = 'localhost'
    userName = 'your_database_user_name_here'
    userPassword = 'your_database_password_here'
    databaseName = 'your_database_name_here'

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
            cur.execute(create_movie_awards_table)

        # For multiple databases and same tableName used, create table anyway
        cur.execute(create_movie_awards_table)

        # Test encoding
        print "System default encoding: %s" %(sys.getdefaultencoding())
        reload(sys)
        sys.setdefaultencoding('utf-8')
        print "System current encoding: %s" %(sys.getdefaultencoding())

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
        print "IOError: %s" % (e)
    except mdb.Error, e:
        print "Error: %s" % (e)
