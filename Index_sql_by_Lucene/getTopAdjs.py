#!usr/bin/bash
#coding:utf-8




import codecs
import json
import os
import operator
import sqlConstants
from utils import *

def getRidOfBOM(data):
	if data[:3] == codecs.BOM_UTF8:
		data = data[3:]
	return data

baseDir = '/home/rio/workspace/lucene' 
tfidfDir = baseDir +'/fenci_tfidf'
tfidfPath = baseDir +'/fenci_tfidf/movieAdjs.txt'

allTopAdjs = open(tfidfPath,'a') 


for folder in os.listdir(tfidfDir):
	if folder.endswith('.txt') or folder.endswith('.txt~'):
		continue
	for fileName in os.listdir(tfidfDir+'/'+folder):
		subject_id = fileName.split('_')[0]

		tfidfPath = tfidfDir+'/' +folder +'/'+subject_id+'_tfidf.json'

		tfidfFile = open(tfidfPath,'r')
		tfidfDict = {}
		infoLinesNum = 3
		title = tfidfFile.readline().split(':')[1][0:-1]
		rating_average = tfidfFile.readline().split(':')[1][0:-1]
		comments_count = tfidfFile.readline().split(':')[1][0:-1]

		line = tfidfFile.readline()
		while(line):
			adj = line.split(':')[0]
			tfidf = line.split(':')[1][0:-1] #去掉/n
			try:
				tfidf = float(tfidf)
			except:
				tfidf = 0.0
			if adj[0] == '*':
				print 'adj in summary'
				tfidf = tfidf * SUMMARY_ADJ_BOOST
				adj = adj[1:]

			#判断dict中是否已有该adj，如果已有，就是说明summary中的adj和comments中的重复了，需要相加
			tfidfDict[adj] = tfidf if adj not in tfidfDict.keys() else tfidfDict[adj]+tfidf
			line = tfidfFile.readline()


		#print tfidfDict
		tfidfTupleList = [(k, v) for k, v in tfidfDict.items()]
		tfidfTupleListSorted = sorted(tfidfTupleList,key=lambda t:t[1], reverse=True)
		topNum = ADJ_NUM if len(tfidfTupleListSorted)>=ADJ_NUM else len(tfidfTupleListSorted)
		topAdjsList = tfidfTupleListSorted[0:topNum]
		#print topAdjsList
		movieAdjsStr = subject_id + ':' + '<'+title+'>' + ' rate:' +rating_average +' count:'+ comments_count +'***'
		for eachTuple in topAdjsList:
			movieAdjsStr = movieAdjsStr + eachTuple[0]+'='+str(eachTuple[1]) + ',' #去掉最后一个','
		movieAdjsStr = movieAdjsStr[0:-1]
		print fileName
		print movieAdjsStr

		allTopAdjs.write(movieAdjsStr + '\n')







print 'we made it!'

		

