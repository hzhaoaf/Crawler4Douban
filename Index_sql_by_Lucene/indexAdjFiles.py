#!/usr/bin/env python
#coding:utf-8


import sys, os, lucene, threading, time
from datetime import datetime
import codecs
import json
# import simplejson

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, FloatField,IntField,StringField

from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
from org.apache.lucene.analysis.core import WhitespaceAnalyzer


"""
This class is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""

class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

def getRidOfBOM(data):
    if data[:3] == codecs.BOM_UTF8:
        data = data[3:]
        print 'getRidOfBOM!'
    return data

INDEX_DIR = "/home/env-shared/NGfiles/lucene_adj_index"
baseDir = '/home/rio/workspace/lucene' 

rawDir = baseDir +'/fenciDataRaw'
adjDir = baseDir +'/fenciAdj'



class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(writer)
        ticker = Ticker()
        print 'commit index',
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print 'done'

    def indexDocs(self, writer):

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



        for folder in os.listdir(rawDir):
            for fileName in os.listdir(rawDir+'/'+folder):
                if not fileName.endswith('.json'):
                    continue


                print fileName
                
                subject_id = fileName.split('_')[0]
                
                # print rawDict
                print 'id:'+subject_id
                print 'folder:'+str(folder)

                rawPath = rawDir+'/' +folder +'/'+subject_id+'_res.json'
                adjPath = adjDir+'/' +folder +'/'+subject_id+'_adj.json'
                #tfidfPath = tf_idfDir + '/' + subject_id+'_tfidf.json'

                print adjPath

                rawFile = open(rawPath,'r')
                raw = rawFile.read()
                if raw =='':
                    with open(baseDir+'/'+'err_no_raw_content.txt','a') as err:
                        err.write(subject_id+'\n')
                # if subject_id =='6018943':
                #     rawFile.seek(0)

                rawFile.close()
                adjFile = open(adjPath,'r')
                adj = adjFile.read()

                adjFile.close()

                raw = getRidOfBOM(raw)
                adj = getRidOfBOM(adj)

                if raw != '':
                    rawDict = json.loads(raw)
                adjDict = json.loads(adj)

                rawAll = rawDict['summary'] +' '+ rawDict['user_tags'] + ' '+rawDict['comments']
                summary_adjs = adjDict['summary_adjs']
                comments_adjs = adjDict['comments_adjs']
                title = adjDict['title']
                rating_average = adjDict['rating_average']
                comments_count = adjDict['comments_count']

                doc = Document()
                doc.add(Field("folder",folder,t1))
                doc.add(Field("title", title, t1))
                doc.add(Field("subject_id", subject_id, t1))
                doc.add(IntField("comments_count", comments_count, Field.Store.YES))
                doc.add(FloatField("rating_average", rating_average, Field.Store.YES))


                if len(summary_adjs)>0:
                    print summary_adjs
                    exit()
                doc.add(Field("summary_adjs", summary_adjs, t2))

                #if len(comments_adjs)>0:
                doc.add(Field("comments_adjs", comments_adjs, t2))

                writer.addDocument(doc)

                

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print IndexFiles.__doc__
        sys.exit(1)
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()

    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    IndexFiles(os.path.join(base_dir, INDEX_DIR),
               WhitespaceAnalyzer(Version.LUCENE_CURRENT))
    end = datetime.now()
    print end - start

