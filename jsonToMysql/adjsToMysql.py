#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
A script to import movie adjectives to Mysql record of Douban Movie items
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
                    others_like VARCHAR(1000), \
                    adjs        VARCHAR(100) \
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE utf8_unicode_ci; \
                    "

#print create_movie_items_table

# Insert record to Mysql
updateStringWithAllStringValues = (
                    "UPDATE movie_items SET adjs =%s "
                                        "WHERE subject_id=%s "
                                           )


#print updateStringWithAllStringValues

def insertMysqlRecordFromAdjString(recordString, databaseCursor):
    try:
        # Get seperate fields of JSON
        insertValues = getSeperateFieldFromAdjString(recordString)
        movie_subject_id = insertValues[1]

        #print type(insertValues)
        #print insertValues

        # Check if we have the record for the specified subject_id
        fetchSqlParams = (movie_subject_id)
        rowCount = databaseCursor.execute("SELECT * FROM movie_items WHERE subject_id = %s;", fetchSqlParams)
        if (rowCount > 0):
            # Got a record, insert to database and log the subject_id
            print 'Now inserting adjs for ID: %s' % (movie_subject_id)
            affectedRows = databaseCursor.execute(updateStringWithAllStringValues, insertValues)
        else:
            # No record, log the subject_id
            print 'No record for ID: %s' % (movie_subject_id)

    except Exception as e:
        print "Error: %s" % (e)

def getSeperateFieldFromAdjString(adjString):
    try:
        #print 'Now extracting seperate fields...'
        movie_subject_id = adjString.split(':')[0]
        adjsField = adjString.split('***')[1]

        print 'Data for %s: %s' % (movie_subject_id, adjsField)

        insertTuple = (adjsField, movie_subject_id)

        return insertTuple

    except Exception as e:
        print "Error: %s" % (e)

# Main Routine
if __name__ == '__main__':

    adjsFile = './movieAdjs.txt'
    fileMode = 'w+'
    newLineToken = '\n'

    tableName = 'movie_items'
    hostName = 'your_host_name'
    userName = 'your_database_user_name'
    userPassword = 'your_database_user_password'
    databaseName = 'your_database_name'

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

        # Start Profiling
        startTime = time.time()

        # Do the dirty job here
        adjLines = file(adjsFile).readlines()
        for adjLine in adjLines:
            insertMysqlRecordFromAdjString(adjLine, cur)

        con.commit()


        # Close cursor and connection
        cur.close()
        con.close()

        #End Profiling
        endTime = time.time()


        print '\nReport:'
        print 'Start time: %s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(startTime)))
        print 'End time: %s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(endTime)))
        print 'Cost %.2f minutes.' % ((endTime - startTime) / 60)
        print 'All Done!'

    except Exception as e:
        print "Error: %s" % (e)
