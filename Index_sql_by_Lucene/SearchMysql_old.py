#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
query_flag_list = [None]*FIELDS_NUM

#make the falg of the field you want to search be 1
query_flag_list[RATING_MAX]          =0 #1
query_flag_list[RATING_AVERAGE]      =0 #2<--this # means that this field is indexed in lucene
query_flag_list[RATING_STARS]        =0 #3
query_flag_list[RATING_MIN]          =0 #  
query_flag_list[REVIEWS_COUNT]       =0 #5
query_flag_list[WISH_COUNT]          =0 #6
query_flag_list[DOUBAN_SITE]         =0  
query_flag_list[YEAR]                =0 #8
query_flag_list[IMAGE_SMALL]         =0  
query_flag_list[IMAGE_LARGE]         =0
query_flag_list[IMAGE_MEDIUM]        =0
query_flag_list[SUBJECT_URL]         =0
query_flag_list[SUBJECT_ID]          =0 #13for debug
query_flag_list[MOBILE_URL]          =0
query_flag_list[TITLE]               =0 #15
query_flag_list[DO_COUNT]            =0
query_flag_list[SEASONS_COUNT]       =0 
query_flag_list[SCHEDULE_URL]        =0
query_flag_list[EPISODES_COUNT]      =0
query_flag_list[GENRES]              =1 #20
query_flag_list[CURRENT_SEASON]      =0
query_flag_list[COLLECT_COUNT]       =0 #22
query_flag_list[CASTS]               =1 #23
query_flag_list[COUNTRIES]           =0 #24
query_flag_list[ORIGINAL_TITLE]      =0 #25
query_flag_list[SUMMARY]             =0 #26
query_flag_list[SUMMARY_SEGMENTATION]=0 #27
query_flag_list[SUBTYPE]             =0 #28
query_flag_list[DIRECTORS]           =0 #29
query_flag_list[COMMENTS_COUNT]      =0 #30
query_flag_list[RATINGS_COUNT]       =0 #31
query_flag_list[AKA]                 =0 #32

print len(query_flag_list)



query_fields_list = []
for i in range(0,len(query_flag_list)):
    if query_flag_list[i]==1:
        query_fields_list.append(fields_name_list[i])
query_fields_num = len(query_fields_list)

#---end config---

def run(searcher, analyzer):
    while True:
        print
        print query_fields_list
        print "Hit enter with no input to quit."
        command = raw_input("Query:")
        if command == '':
            return

        print


        input_queries_list = command.split();

        if len(input_queries_list) != query_fields_num:
            print 'input words num is wrong!'
            print query_fields_list
            return 
        
        occ_list = [BooleanClause.Occur.SHOULD]*query_fields_num


        queries_jarr = JArray('string')(input_queries_list)
        fields_jarr = JArray('string')(query_fields_list)
        occs_jarr   = JArray('object')(occ_list)

        #debug
        print "Searching for:"
        for i in range(query_fields_num):
            print input_queries_list[i],'in',query_fields_list[i]
        

        #query = MultiFieldQueryParser(Version.LUCENE_CURRENT,['subject_id','summary'],analyzer).parse(command); 
        #query = MultiFieldQueryParser.parse(command,['subject_id','summary'],analyzer); 

        #'''
        #MultiFieldQueryParser(Version matchVersion, String[] fields, Analyzer analyzer)
        #'''
        #parser = MultiFieldQueryParser(Version.LUCENE_CURRENT, JArray('string')(['subject_id','summary']),analyzer)
        #query = MultiFieldQueryParser.parse(parser, command_jarr)

        clauses = JArray('object')(occ_list)
        query = MultiFieldQueryParser.parse(Version.LUCENE_CURRENT,queries_jarr,fields_jarr, clauses, analyzer)
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
        print "%s total matching documents." % len(scoreDocs)

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print 'subject_id:', doc.get('subject_id')
            print 'title:', doc.get('title')
            #print 'path:', doc.get("path"), 'name:', doc.get("name")


if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(os.path.join(base_dir, INDEX_DIR)))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = SmartChineseAnalyzer(Version.LUCENE_CURRENT)
    run(searcher, analyzer)
    del searcher
