#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

if len(sys.argv) != 3:
    print 'Usage: fineNewIds.py originalIdsFile newIdsFile'

originalFile = sys.argv[1]
newFile = sys.argv[2]

if len(sys.argv) == 4:
    resultFile = sys.argv[3]
else:
    resultFile = 'newIdListFound'

with open(originalFile) as totalIds:
    totalIdList = totalIds.readlines()

totalIdSet = set(totalIdList)
print 'Number of original Ids:%s ' %  (len(totalIdSet))

with open(newFile) as newIds:
    newIdList = newIds.readlines()

newIdSet = set(newIdList)
print 'Number of new Ids:%s' % (len(newIdSet))

newIdCounter = 0

with open(resultFile, 'w+') as resultIds:
    for newId in newIdSet:
        if newId not in totalIdSet:
            #print 'New ID:' + newId
            newIdCounter += 1
            resultIds.write(newId)
        else:
            pass

print 'Find %s new Ids and written to file %s' % (newIdCounter, resultFile)
print 'Done!'
