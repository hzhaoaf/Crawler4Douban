#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding:utf-8

import sys, os, lucene, threading, time
from datetime import datetime

#from lucene import \
#    NumericField


from java.io import File
from java.util import Map,HashMap
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
#from org.apache.lucene.analysis.cn import ChineseAnalyzer
from org.apache.lucene.analysis.cn.smart import SmartChineseAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, FloatField,IntField,StringField
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
from org.apache.lucene.search.similarities import BM25Similarity
from org.apache.lucene.document import DateTools

from org.apache.lucene.analysis.miscellaneous import PerFieldAnalyzerWrapper

import MySQLdb as mdb


from sqlConstants import *
import utils

#what need to do 
#step 1. change config below
#step 2. make right connection to the sql
#step 3. choose right table
#step 4. select the field of the table you need to index or store


#------step 1------
#---start config---

#the dir to store the index file
INDEX_DIR = "/home/env-shared/NGfiles/lucene_index"
#the field name you want to index
FIELD = 'summary'

#---end config---



class Ticker(object):
    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

def CreateAWrapper():
        #索引的时候使用该wrappe，到了搜索的时候还是使用该wrapper

        analyzerPerField = HashMap()
        #为所有的域设置不同的analyzer  
        analyzerPerField.put('rating_max', StandardAnalyzer(Version.LUCENE_CURRENT))
        analyzerPerField.put('rating_average', StandardAnalyzer(Version.LUCENE_CURRENT))
        analyzerPerField.put('rating_stars', StandardAnalyzer(Version.LUCENE_CURRENT))
        analyzerPerField.put('rating_min', StandardAnalyzer(Version.LUCENE_CURRENT))
        analyzerPerField.put('reviews_count', StandardAnalyzer(Version.LUCENE_CURRENT))
        analyzerPerField.put('wish_count', StandardAnalyzer(Version.LUCENE_CURRENT))
        analyzerPerField.put('year', StandardAnalyzer(Version.LUCENE_CURRENT))

        analyzerPerField.put('title', SmartChineseAnalyzer(Version.LUCENE_CURRENT))
        analyzerPerField.put('original_title', SmartChineseAnalyzer(Version.LUCENE_CURRENT))
        analyzerPerField.put('summary', SmartChineseAnalyzer(Version.LUCENE_CURRENT))
        analyzerPerField.put('aka', SmartChineseAnalyzer(Version.LUCENE_CURRENT))

        analyzerPerField.put('genres', WhitespaceAnalyzer(Version.LUCENE_CURRENT))
        analyzerPerField.put('casts', WhitespaceAnalyzer(Version.LUCENE_CURRENT))
        analyzerPerField.put('countries', WhitespaceAnalyzer(Version.LUCENE_CURRENT))
        analyzerPerField.put('summary_segmentation', WhitespaceAnalyzer(Version.LUCENE_CURRENT))
        analyzerPerField.put('subtype', WhitespaceAnalyzer(Version.LUCENE_CURRENT))
        analyzerPerField.put('directors', WhitespaceAnalyzer(Version.LUCENE_CURRENT))
        analyzerPerField.put('user_tags', WhitespaceAnalyzer(Version.LUCENE_CURRENT))
        analyzerPerField.put('others_like   ', WhitespaceAnalyzer(Version.LUCENE_CURRENT))
        analyzerPerField.put('adjs', WhitespaceAnalyzer(Version.LUCENE_CURRENT))

        #analyzerPerField.put('douban_site', StandardAnalyzer(Version.LUCENE_CURRENT))注释起来的都是没必要分析的
        #analyzerPerField.put('image_small', StandardAnalyzer(Version.LUCENE_CURRENT))
        #analyzerPerField.put('image_large', StandardAnalyzer(Version.LUCENE_CURRENT))
        #analyzerPerField.put('image_medium', StandardAnalyzer(Version.LUCENE_CURRENT))
        #analyzerPerField.put('subject_url', StandardAnalyzer(Version.LUCENE_CURRENT))
        #analyzerPerField.put('subject_id', StandardAnalyzer(Version.LUCENE_CURRENT))
        #analyzerPerField.put('mobile_url', StandardAnalyzer(Version.LUCENE_CURRENT))
        #analyzerPerField.put('do_count', StandardAnalyzer(Version.LUCENE_CURRENT))
        #analyzerPerField.put('seasons_count', StandardAnalyzer(Version.LUCENE_CURRENT))
        #analyzerPerField.put('schedule_url', StandardAnalyzer(Version.LUCENE_CURRENT))
        #analyzerPerField.put('episodes_count', StandardAnalyzer(Version.LUCENE_CURRENT))
        #analyzerPerField.put('current_season', new KeywordAnalyzer(Version.LUCENE_CURRENT))
        #analyzerPerField.put('collect_count', new KeywordAnalyzer(Version.LUCENE_CURRENT))
        #analyzerPerField.put('comments_count', StandardAnalyzer(Version.LUCENE_CURRENT))
        #analyzerPerField.put('ratings_count', StandardAnalyzer(Version.LUCENE_CURRENT))

        #!欢叔将QueryParser弄好之后就可以改成 WhiteSpace的
        aWapper = PerFieldAnalyzerWrapper(SmartChineseAnalyzer(Version.LUCENE_CURRENT),analyzerPerField)

        return aWapper

class IndexMySql(object):
    """Usage: python IndexFiles.py"""

    def __init__(self, storeDir, aWrapper):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))
        aWrapper = LimitTokenCountAnalyzer(aWrapper, 1048576)
        bm25Sim = BM25Similarity(2.0,0.75) #BM25 with these default values: k1 = 1.2, b = 0.75.
        config = IndexWriterConfig(Version.LUCENE_CURRENT, aWrapper)
        #使用BM25算法，如果不需要就去掉这句即可
        config.setSimilarity(bm25Sim)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        #start
        self.indexTable(writer)

        ticker = Ticker()
        print 'commit index'
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print 'done'

    def indexTable(self, writer):

        #connection 
        con = None

        #define the index of all the fields
        #---------step 2：connect to mysql----------
        con = mdb.connect('localhost','root','lhj75211314','douban_movie_v3')

        #t_num = FieldType.NumericType it is wrong!!
        t_num = FieldType()
        t_num.setStored(False)

        t1 = FieldType()
        t1.setIndexed(True)
        t1.setStored(True)
        t1.setTokenized(False)
        t1.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)
        
        t2 = FieldType()
        t2.setIndexed(True)
        t2.setStored(False)
        t2.setTokenized(True)
        t2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        t3 = FieldType()
        t3.setIndexed(True)
        t3.setStored(True)
        t3.setTokenized(True)
        t3.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)

        maxDict = utils.maxDict
        #加权数值范围
        base = DOC_BOOST_RANGE[0]
        upper = DOC_BOOST_RANGE[1]

        with con:
            # Careful with codecs
            con.set_character_set('utf8')

            cur = con.cursor()
            # Aagin the codecs
            cur.execute('SET NAMES utf8;')
            cur.execute('SET CHARACTER SET utf8;')
            cur.execute('SET character_set_connection=utf8;')
            
            #------step 3： choose the right table------
            cur.execute("SELECT * FROM movie_items")

            numrows = int(cur.rowcount)
            print 'numrows:',numrows
            for i in range(numrows):
                print
                row = cur.fetchone()

                #------step 4：Index your field------
                summary = row[SUMMARY]  
                subject_id = row[SUBJECT_ID]


                print 'id'+subject_id
                year = utils.formatYear(row[YEAR])
                try:
                    date = DateTools.stringToDate(year.replace('-',' '))
                    wtfFile = open('wtf.txt','a')
                    dateStr  = DateTools.dateToString(date,DateTools.Resolution.DAY)
                except:
                    wtfFile.write(year+'\n')

                        

                doc = Document()

                #boosting
                boostProb = utils.calcBoostProb(row,maxDict,dateStr)
                boost = base + boostProb*(upper-base)

                doc.add(FloatField("boost",boost,Field.Store.YES))
                doc.add(StringField("year",dateStr,Field.Store.YES))
                print 'dateStr:'+dateStr
                #A text field is a sequence of terms that has been tokenized while a string field is a single term (although it can also be multivalued.)

                do_count = row[DO_COUNT] if row[DO_COUNT] != None else 0
                wish_count = row[COLLECT_COUNT] if row[WISH_COUNT] != None else 0

                #fields which should not be analyzed
                doc.add(FloatField("rating_average",float(row[RATING_AVERAGE]),Field.Store.YES))
                doc.add(FloatField("rating_stars", float(row[RATING_STARS]), Field.Store.YES))
                doc.add(IntField("reviews_count", int(row[REVIEWS_COUNT]), Field.Store.YES))
                #doc.add(FloatField("year", float(row[YEAR]), Field.Store.YES).setBoost(boost))
                doc.add(IntField("collect_count", int(row[COLLECT_COUNT]), Field.Store.YES))
                doc.add(IntField("do_count", int(do_count), Field.Store.YES))
                doc.add(IntField("wish_count", int(wish_count), Field.Store.YES))
                doc.add(IntField("subject_id", int(row[SUBJECT_ID]), Field.Store.YES))
                doc.add(IntField("comments_count", int(row[COMMENTS_COUNT]), Field.Store.YES))
                doc.add(IntField("ratings_count", int(row[RATINGS_COUNT]), Field.Store.YES))
                doc.add(StringField("image_small", row[IMAGE_SMALL], Field.Store.YES))

                #fields which should be analyzed with WhitespaceAnalyzer
                #attention!!! dont use a long sentence like :
                #doc.add(Field("genres",    row[GENRES].replace(delim,' '),    t3).setBoost(boost))
                #or you'll get a null pointer error
                f = Field("countries", row[COUNTRIES].replace(delim,' '), t3)
                f.setBoost(boost)
                doc.add(f)

                #将英文人名中的 ·
                f = Field("casts",     row[CASTS].replace(delim,' ').replace('·',' '),     t3)
                f.setBoost(boost)
                doc.add(f)

                f = Field("directors", row[DIRECTORS].replace(delim,' ').replace('·',' '), t3)
                f.setBoost(boost)
                doc.add(f)

                Field("genres",    row[GENRES].replace(delim,' '),    t3)
                f.setBoost(boost)
                doc.add(f)

                Field("subtype",   row[SUBTYPE].replace(delim,' '),   t3)
                f.setBoost(boost)
                doc.add(f)

                #it is wrong cause indexable field has no method setBoost
                # fieldList = doc.getFields()  # is not a python 'list' , but a 'List' which is unindexable                
                # for eachField in fieldList:
                #     eachField.setBoost(boost)


                #user_tags 原始字符串要存，reRank要用：
                doc.add(StringField("raw_user_tags",row[USER_TAGS],Field.Store.YES))
                doc.add(StringField("raw_others_like",row[OTHERS_LIKE],Field.Store.YES))
                

                user_tags_str = ''
                others_like_str = ''
                tags_len = 0
                

                if row[USER_TAGS]!='':
                    user_tags_list = row[USER_TAGS].split(delim) 
                    for tag_pair in user_tags_list:
                        if tag_pair!='':#字符串的最后一个字符是￥，这样split之后最后一个元素是空字符
                            print 'tag_pair'+tag_pair+'hhe'
                            tag_name = tag_pair.split(delim_uo)[0]+' ' # dont forget this space !!
                            tag_num = tag_pair.split(delim_uo)[1]
                            tag_num_processed = int(int(tag_num)/SPAN)+1
                            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            user_tags_str = user_tags_str +' '+ tag_name * tag_num_processed
                            tags_len = tags_len + tag_num_processed #最后得到总共词的个数


                if tags_len<TAGS_AVER_LEN:
                    #填充tags，目测3是平均长度
                    user_tags_str = user_tags_str +' ￥￥￥'*(TAGS_AVER_LEN - tags_len)
                #


                if row[OTHERS_LIKE]!='':
                    for like_pair in row[OTHERS_LIKE].split(delim):
                        if like_pair!='':
                            others_like_str = others_like_str +' '+like_pair.split(delim_uo)[1]


                #start process adjs
                if row[ADJS] != None:
                    doc.add(StringField("raw_adjs",row[ADJS],Field.Store.YES))

                    adjs_str = ''
                    adjs_len = 0
                    if row[ADJS] != '' and row[ADJS] != '\n':
                        #'重要=4.0,特殊=4.0'
                        adjs_str = row[ADJS]
                        adjs_list = adjs_str.split(',')
                        for adj_pair in adjs_list:
                            #print 'adj_pair:'+adj_pair+'hhe'
                            adj_name = adj_pair.split('=')[0]
                            adj_num = adj_pair.split('=')[1] 
                            if adj_num[-1] == '\n':
                                adj_num = adj_num[0:-1]
                            adj_num = int(float(adj_num))
                            adjs_str = adjs_str + ' ' + adj_name * adj_num
                            adjs_len = adjs_len + adj_num #最后得到总共tags的个数



                    if adjs_len<ADJS_AVER_LEN:
                        #填充tags，目测3是平均长度
                        adjs_str = adjs_str +' ￥￥￥'*(ADJS_AVER_LEN - adjs_len)

                    f = Field("adjs", adjs_str, t3)
                    f.setBoost(boost)
                    doc.add(f)

                f = Field("user_tags", user_tags_str, t3)
                f.setBoost(boost)
                doc.add(f)

                f = Field("others_like", others_like_str, t3)
                f.setBoost(boost)
                doc.add(f)



                #fields which should be analyzed with good analyzer
                f = Field("title", row[TITLE], t3)                
                f.setBoost(boost)
                doc.add(f)

                f = Field("original_title", row[ORIGINAL_TITLE], t3)
                f.setBoost(boost)
                doc.add(f)

                f = Field("summary_segmentation", row[SUMMARY_SEGMENTATION], t3)
                f.setBoost(boost)
                doc.add(f)

                f = Field("aka", row[AKA], t2)
                f.setBoost(boost)
                doc.add(f)

                if len(summary) > 0:
                    print subject_id +'--->'+':\n    '+ row[TITLE]
                    try:
                        summary_unicoded = unicode(summary, 'utf-8') #test the encoding 
                    except Exception,e:
                        print "Decode Failed: ", e
                    f = Field('summary', summary, t2)
                    f.setBoost(boost)
                    doc.add(f)
                else:
                    print "warning:\n" + subject_id +'---> No content!'
                print 'boosting:' + str(boost)

                #for debug
                if boost>upper:
                    print boostProb
                    print maxDict
                    
                    exit(0)

                writer.addDocument(doc)



if __name__ == '__main__':
    if len(sys.argv) !=1:
        print IndexMySql.__doc__
        sys.exit(1)
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    #try:
    CreateAWrapper()

    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    aWrapper = CreateAWrapper()
    IndexMySql(os.path.join(base_dir, INDEX_DIR), aWrapper)
    end = datetime.now()
    print end - start

