#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
Wrapper script for getting info of a movie according to its subject ID the pipeline way
'''

import sys

from getAllMovieInfoBySubjectIDModule import getAllMovieInfoById

def getAllMovieInfoBySubjectIDWrapper(movieSubjectID):
    try:

        subjectID, basicInfo, userTags, othersLike, shortComments, awardsInfo = getAllMovieInfoById.getAllMovieInfoBySubjectID(movieSubjectID)
        getAllMovieInfoById.insertMovieInfoToMysql(subjectID, basicInfo, userTags, othersLike, shortComments, awardsInfo)

    except Exception as e:
        print 'Error when dealing with subject ID %s: %s' % (movieSubjectID, e)

'''
if len(sys.argv) != 2:
    print 'Usage: getMovieInfoByIdWrapper.py movieSubjectID'

if len(sys.argv) == 2:
    getAllMovieInfoBySubjectIDWrapper(sys.argv[1])
'''
