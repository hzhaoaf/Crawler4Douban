#!/usr/bin/env python
# -*- coding: utf-8 -*-
#usage:offer initJvm() config() run() the three functions, search_rio.py will use them 

import sys, os, lucene

from java.io import File,StringReader
from lucene import JArray
#from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.cn.smart import SmartChineseAnalyzer
#from org.apache.lucene.analysis.cn import ChineseAnalyzer

from org.apache.lucene.queryparser.classic import MultiFieldQueryParser
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher ,SortField ,Sort
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanClause

from org.apache.lucene.search.similarities import BM25Similarity,DefaultSimilarity

import json
import operator
from sqlConstants import *

from org.apache.lucene.analysis import TokenStream
from org.apache.lucene.analysis.tokenattributes import \
    OffsetAttribute, CharTermAttribute, TypeAttribute, \
    PositionIncrementAttribute

import utils 


#what need to do 
#step 1. change config below
#step 2. ok

#------step 1------
#---start config---
#the dir to store the index file
INDEX_DIR = "/home/env-shared/NGfiles/lucene_index"
#the field name you want to search
#this list correspond to the order of the field in the sql


class IsolationSimilarity(DefaultSimilarity):
    def tf(docFreq,numDocs):
        return float(1.0)


def initJvm():
    #Init the jvm
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION

def config():
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(os.path.join(base_dir, INDEX_DIR)))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    bm25Sim = BM25Similarity(2.0,0.75) #BM25 with these default values: k1 = 1.2, b = 0.75.
    searcher.setSimilarity(bm25Sim)
    analyzer = SmartChineseAnalyzer(Version.LUCENE_CURRENT)
    return searcher,analyzer

def printTokens(analyzer,command,field):
    #usage: print the tokens 
    #tokenStream
    tokenStream =   analyzer.tokenStream(field, StringReader(command))
    charTermAtr = tokenStream.addAttribute(CharTermAttribute.class_)
    tokenStream.reset()
    while (tokenStream.incrementToken()):
        print charTermAtr.toString()
    tokenStream.close()

def printWrappedAnalyzer(aWrapper):
    print aWrapper.toString()


#---end config---

def run(command,searcher, aWrapper):

    print

    if command == '':
        return
    
    #debug
    #print "Searching for:"+command

    #query = MultiFieldQueryParser(Version.LUCENE_CURRENT,['subject_id','summary'],analyzer).parse(command); 
    #query = MultiFieldQueryParser.parse(command,['subject_id','summary'],analyzer); 

    #'''
    #MultiFieldQueryParser(Version matchVersion, String[] fields, Analyzer analyzer)
    #'''
    #parser = MultiFieldQueryParser(Version.LUCENE_CURRENT, JArray('string')(['subject_id','summary']),analyzer)
    #query = MultiFieldQueryParser.parse(parser, command_jarr)

    #创建QueryParser对象 默认的搜索域为title 
    parser = QueryParser(Version.LUCENE_CURRENT, "title", aWrapper) 
    #A PerFieldAnalyzerWrapper can be used like any other analyzer, for both indexing and query parsing. 
    query = parser.parse(command)

    #test the analyzerWrapper
    #printTokens(aWrapper,command,'title')
    #printWrappedAnalyzer(aWrapper)

    #所有有相关度的doc，进行排序
    #sortField = SortField('boost',SortField.Type.FLOAT,True) #True表示降序
    #sort = Sort(sortField)
    '''
    Error with:
    > query = lucene.MultiFieldQueryParser(lucene.Version.LUCENE_CURRENT,
    > ["payload","subject"], analyzer).parse(command)

    I think there's a bug with the method binding.  MultiFieldQueryParser has several static parse
    methods, plus the inherited regular method from QueryParser.  It looks like all of them are
    being resolved as if they were static.  As a workaround, you can call it like this:

    parser = lucene.MultiFieldQueryParser(lucene.Version.LUCENE_CURRENT, ["payload","subject"],
    analyzer)
    lucene.MultiFieldQueryParser.parse(parser, command)
    '''

    #occ=[BooleanClause.Occur.SHOULD , BooleanClause.Occur.SHOULD]
    #query = MultiFieldQueryParser.parse(command_list,['subject_id','summary'],occ,analyzer)

    #query = QueryParser(Version.LUCENE_CURRENT, FIELD,analyzer).parse(command)

    #scoreDocs = searcher.search(query, 50,sort).scoreDocs
    scoreDocs = searcher.search(query, 50).scoreDocs




    # retList = []
    # for scoreDoc in scoreDocs:
    #     doc = searcher.doc(scoreDoc.doc)
    #     score = scoreDoc.score
    #     #print 'subject_id:', doc.get('subject_id')
    #     #print 'title:', doc.get('title')

    #     tmpDict = {
    #     'subject_id':doc.get('subject_id'),
    #     'title':doc.get('title'),
    #     'directors':doc.get('directors'),
    #     'summary':doc.get('summary'),
    #     'image_small':doc.get('image_small'),
    #     'boost':doc.get('boost'),
    #     'user_tags':doc.get('user_tags'),
    #     'year':doc.get('year'),
    #     'score':score
    #     }
    #     retList.append(tmpDict)

    maxDict = utils.maxDict
    movieDictList =  utils.scoreDocs2dictList(scoreDocs,searcher)
    retList = movieDictList
    retList = utils.reRank(movieDictList,maxDict,command)


    #人工排序
    #retList = sorted(retList, key=operator.itemgetter('boost'), reverse=True)  

    del searcher
    return retList


def printResult(retList):
    #usage: for the testing
    # unicode !
    #print retList[0]['title'].encode('utf-8')
    for each in retList:
        print each['subject_id'] + ':' +each['title'] + 'boost->'+ str(each['boost'])+'|| score:'+str(each['score'])
        #print each['subject_id'] + ':' +each['title'] + 'boost->'+ str(each['boost'])+'|| score:'+str(each['score']) + ' ^'+each['user_tags']+'\n'










if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    #print 'lucene', lucene.VERSION
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(os.path.join(base_dir, INDEX_DIR)))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    command = sys.argv[1]
    import IndexMysql
    aWrapper = IndexMysql.CreateAWrapper()
    retList = run(command,searcher, aWrapper)
    printResult(retList)
    del searcher
