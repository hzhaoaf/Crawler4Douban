#!/usr/bin/env python
# -*- coding: utf-8 -*-
#usage:offer initJvm() config() run() the three functions, search_rio.py will use them 

import sys, os, lucene

from java.io import File
from lucene import JArray
#from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.cn.smart import SmartChineseAnalyzer
#from org.apache.lucene.analysis.cn import ChineseAnalyzer

from org.apache.lucene.queryparser.classic import MultiFieldQueryParser
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanClause

import json
from sqlConstants import *

#what need to do 
#step 1. change config below
#step 2. ok

#------step 1------
#---start config---
#the dir to store the index file
INDEX_DIR = "/home/env-shared/NGfiles/lucene_index"
#the field name you want to search
#this list correspond to the order of the field in the sql



def initJvm():
    #Init the jvm
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION

def config():
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(os.path.join(base_dir, INDEX_DIR)))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = SmartChineseAnalyzer(Version.LUCENE_CURRENT)
    return searcher,analyzer


#---end config---

def run(command,searcher, aWrapper):

    print

    if command == '':
        return

    print

    
    
    


    #debug
    #print "Searching for:"+command

    #query = MultiFieldQueryParser(Version.LUCENE_CURRENT,['subject_id','summary'],analyzer).parse(command); 
    #query = MultiFieldQueryParser.parse(command,['subject_id','summary'],analyzer); 

    #'''
    #MultiFieldQueryParser(Version matchVersion, String[] fields, Analyzer analyzer)
    #'''
    #parser = MultiFieldQueryParser(Version.LUCENE_CURRENT, JArray('string')(['subject_id','summary']),analyzer)
    #query = MultiFieldQueryParser.parse(parser, command_jarr)

    #创建QueryParser对象 默认的搜索域为content 
    parser = QueryParser(Version.LUCENE_CURRENT, "title", aWrapper) 
    query = parser.parse(command)

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
    scoreDocs = searcher.search(query, 50).scoreDocs
    #print "%s total matching documents." % len(scoreDocs)

    retList = []
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        #print 'subject_id:', doc.get('subject_id')
        #print 'title:', doc.get('title')

        tmpDict = {
        'subject_id':doc.get('subject_id'),
        'title':doc.get('title'),
        'directors':doc.get('directors'),
        'summary':doc.get('summary'),
        'image_small':doc.get('image_small')}
        retList.append(tmpDict)


    return retList


    del searcher





if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    #print 'lucene', lucene.VERSION
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(os.path.join(base_dir, INDEX_DIR)))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = SmartChineseAnalyzer(Version.LUCENE_CURRENT)
    run(searcher, analyzer)
    del searcher
