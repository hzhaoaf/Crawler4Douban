#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
A script to import movie others like information to Mysql record of Douban Movie items
'''

import json
import sys
import glob
import os
import time
import string

def processingJsonFilesInDirectory(jsonDirectory):
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
            getMovieIDsFromJson(jsonFile)

    except Exception as e:
        print 'Exception: %s' %(e)

def getJsonFileListFromDirectory(jsonDirectory):
    try:
        jsonFileList = glob.glob(jsonDirectory+'/*.json')
        return jsonFileList
    except IOError as e:
        print "IOError Occured: %s" % (e)


def getMovieIDsFromJson(jsonFileName):
    global processedFiles
    global rawMovieIdsCount
    try:
        # Get raw JSON
        jsonString = getJsonStringFromJsonFile(jsonFileName)
        #print jsonString

        movieIDs = jsonString.keys()
        rawMovieIdsCount += len(movieIDs)

        for movieID in movieIDs:
            movieIDsSet.add(movieID)
            movieIDsRaw.write(movieID + newLineToken)


        # Processed one JSON file
        processedJsonFileName = jsonFileName + newLineToken
        processedJsonList.write(processedJsonFileName)
        processedFiles += 1

    except Exception, e:
        print "Error: %s" % (e)

def getJsonStringFromJsonFile(jsonFileName):
    try:
        jsonFile = file(jsonFileName)
        jsonString = json.load(jsonFile)
        jsonFile.close()

        return jsonString

    except Exception as e:
        print "Error  %s" % (e)

def getJsonStringFromJsonFileUsingDecoder(jsonFileName):
    try:
        jsonFile = file(jsonFileName)
        jsonSource = jsonFile.read()
        jsonTarget = json.JSONDecoder().decode(jsonSource)
        jsonFile.close()

        return jsonTarget

    except Exception as e:
        print "Error  %s" % (e)

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

    fileMode = 'w+'
    newLineToken = '\n'

    numberOfJsonFiles = 0
    processedFiles = 0
    rawMovieIdsCount = 0

    fileListDetialOfDirectories = ''

    toBeProcessedFileList = './toBeProcessedJsonFiles'
    processedJsonFileList = './processedJsonFiles'

    movieIDsSet = set()
    movieIDsLogFile = './movieIDsMergedFromOthersLike'
    movieIDsRawFile = './movieIDsFromOthresLike'

    # Profiling
    startTime = 0
    endTime = 0

    try:
        # Open file for logging
        processedJsonList = open(processedJsonFileList, fileMode)
        toBeProcessedJsonList = open(toBeProcessedFileList, fileMode)
        movieIDsFile = open(movieIDsLogFile, fileMode)
        movieIDsRaw = open(movieIDsRawFile, fileMode)

        # Start Profiling
        startTime = time.time()

        # Go and insert records
        for jsonDirectory in jsonDirectorys:
            if os.path.exists(jsonDirectory):
                print 'Now processing %s...' % (jsonDirectory)
                processingJsonFilesInDirectory(jsonDirectory)
            else:
                print 'The directory %s will be processed does not exist...' % (jsonDirectory)
                raise Exception

        for movieID in movieIDsSet:
            movieIDsFile.write(movieID + newLineToken)

        #End Profiling
        endTime = time.time()

        # Close Log File
        processedJsonList.close()
        toBeProcessedJsonList.close()
        movieIDsFile.close()
        movieIDsRaw.close()

        print '\nReport:'
        print 'Start time: %s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(startTime)))
        print 'Have %d files to process' % (numberOfJsonFiles)
        print 'Details are:'
        print fileListDetialOfDirectories
        print 'Processed %d files in total' % (processedFiles)
        print 'End time: %s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(endTime)))
        print 'Cost %.2f minutes.' % ((endTime - startTime) / 60)
        print 'Got %s distinct Movie IDs in total and %s raw Movie Ids.' % (len(movieIDsSet), rawMovieIdsCount)
        print 'All Done!'

    except Exception, e:
        print "Exception: %s" % (e)
