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

# Insert record to Mysql
updateStringWithAllStringValues = (
                    "UPDATE movie_items SET others_like=%s "
                                        "WHERE subject_id=%s "
                                           )


#print updateStringWithAllStringValues

def insertOthersLikeToMysql(jsonString, databaseCursor, movie_subject_id):
    try:
        # Get seperate fields of JSON
        insertValues = getSeperateFieldFromJson(jsonString, movie_subject_id)

        #print type(insertValues)
        #print insertValues

        # Check if we have the record for the specified subject_id
        fetchSqlParams = (movie_subject_id)
        rowCount = databaseCursor.execute("SELECT * FROM movie_items WHERE subject_id = %s;", fetchSqlParams)

        if (rowCount > 0):
            # Got a record, insert to database and log the subject_id
            print 'Now inserting others like...'
            affectedRows = databaseCursor.execute(updateStringWithAllStringValues, insertValues)
            print 'Done!'
        else:
            # No record, log the subject_id
            print 'No record for ID: %s' % (movie_subject_id)

    except Exception, e:
        print "Database Error: %s" % (e)

def getSeperateFieldFromJson(jsonString, movie_subject_id):
    try:
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

        insertTuple = (othersLikeString, movie_subject_id)

        return insertTuple

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

def getJsonStringFromJsonFileUsingDecoder(jsonFileName):
    try:
        jsonFile = file(jsonFileName)
        jsonSource = jsonFile.read()
        jsonTarget = json.JSONDecoder().decode(jsonSource)
        jsonFile.close()

        return jsonTarget

    except Exception as e:
        print "Error: %s" % (e)
