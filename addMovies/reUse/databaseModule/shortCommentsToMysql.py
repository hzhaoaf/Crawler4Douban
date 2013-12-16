#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
A script to import short comments to Mysql record of Douban Movie items
'''

import json
import MySQLdb as mdb
import sys
import glob
import os
import time

create_short_comments_table = "CREATE TABLE IF NOT EXISTS \
        `short_comments`( \
                    `comment_id` int(50) NOT NULL auto_increment, \
                    `user_name` VARCHAR(50), \
                    `user_comment` VARCHAR(1000), \
                    `comment_date` VARCHAR(50), \
                    `subject_id` VARCHAR(50) NOT NULL, \
                    `vote_number` VARCHAR(10), \
                    `user_star` VARCHAR(10), \
                    PRIMARY KEY (`comment_id`), \
                    KEY (`subject_id`) \
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE utf8_unicode_ci; \
                    "

#print create_movie_items_table

# Insert record to Mysql
insertStringWithAllStringValues = (
                    "INSERT IGNORE INTO short_comments(user_name,"
                                        "user_comment,"
                                        "comment_date,"
                                        "subject_id,"
                                        "vote_number,"
                                        "user_star) "
                                    "values (%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s,"
                                           "%s);"
                                           )


#print insertStringWithAllStringValues

def insertShortCommentsToMysql(jsonString, databaseCursor):
    try:
        # Get seperate fields of JSON
        insertValues = getSeperateFieldFromJson(jsonString)

        #print type(insertValues)
        #print insertValues

        affectedRows = databaseCursor.executemany(insertStringWithAllStringValues, insertValues)

    except Exception as e:
        print "Database Error: %s" % (e)

def getSeperateFieldFromJson(jsonString, subjectID):
    try:
        #print 'Now extracting seperate fields...'
        jsonKeys = jsonString.keys()

        movie_subject_id = subjectID

        insertDict = {}
        insertList = []

        for jsonKey in jsonKeys:
            fieldValue = jsonString[jsonKey]
            if  hasattr(fieldValue, 'keys'):
                subKeys = fieldValue.keys()
                for subKey in subKeys:
                    #print subKey
                    insertDict[subKey] = fieldValue[subKey]
            else:
                #print jsonKey
                insertDict[jsonKey] = fieldValue

            insertTuple = (jsonKey, insertDict['p'], insertDict['date'], movie_subject_id,
                           insertDict['votenum'], insertDict['star']
                           )

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

def getJsonStringFromJsonFileUsingDecoder(jsonFileName):
    try:
        jsonFile = file(jsonFileName)
        jsonSource = jsonFile.read()
        jsonTarget = json.JSONDecoder().decode(jsonSource)
        jsonFile.close()

        return jsonTarget

    except Exception as e:
        print "Error: %s" % (e)
