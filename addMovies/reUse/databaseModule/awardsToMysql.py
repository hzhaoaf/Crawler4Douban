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

def insertMovieAwardsToMysql(jsonString, databaseCursor, subjectID):
    try:
        # Get seperate fields of JSON
        insertValues = getSeperateFieldFromJson(jsonString, subjectID)

        #print type(insertValues)
        #print insertValues

        print 'Now inserting awards info...'
        affectedRows = databaseCursor.executemany(insertStringWithAllStringValues, insertValues)
        print 'Done!'

    except Exception as e:
        print "Database Error: %s" % (e)

def getSeperateFieldFromJson(jsonString, subjectID):
    try:
        #print 'Now extracting seperate fields...'
        jsonKeys = jsonString.keys()
        #print type(jsonKeys)

        '''
        for jsonKey in jsonKeys:
            print jsonKey
            print jsonString[jsonKey]
            print type(jsonString[jsonKey])
        '''

        insertDict = {}
        insertList = []

        if 'awards_items' in jsonKeys:
            #print type(insertDict['award_items'])
            insertDict['award_items'] = json.dumps(insertDict['award_items'])
        else:
            insertDict['award_items'] = ''

        insertDict['movie_name'] = jsonString['movie_name']
        insertDict['subject_id'] = subjectID

        insertTuple = (insertDict['subject_id'], insertDict['movie_name'], insertDict['award_items'])

        #print insertTuple

        insertList.append(insertTuple)

        return insertList

    except Exception as e:
        print "Error: %s" % (e)


def getJsonStringFromJsonFile(jsonFileName):
    try:
        jsonFile = file(jsonFileName)
        jsonString = json.load(jsonFile)
        jsonFile.close()

        return jsonString

    except Exception as e:
        print "Error: %s" % (e)

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

    except Exception as e:
        print "Error: %s" % (e)

