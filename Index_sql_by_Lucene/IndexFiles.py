#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys, os, lucene, threading, time
from datetime import datetime

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

import MySQLdb as mdb

from sqlConstants import *

#what need to do 
#step 1. change config below
#step 2. make right connection to the sql
#step 3. choose right table
#step 4. select the field of the table you need to index or store


#------step 1------
#---start config---

#the dir to store the index file
INDEX_DIR = "/home/rio/tmp_index2"
#the field name you want to index
FIELD = 'name'

#---end config---



class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

class IndexMySql(object):
    """Usage: python IndexFiles.py"""

    def __init__(self, storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexTable(writer)
        ticker = Ticker()
        print 'commit index',
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print 'done'

    def indexTable(self, writer):

        #connection 
        con = None

        #define the index of all the fields
        #---------step 2----------
        con = mdb.connect('localhost','testuser','test623','testdb')

        t1 = FieldType()
        t1.setIndexed(True)
        t1.setStored(True)
        t1.setTokenized(False)
        t1.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)
        
        t2 = FieldType()
        t2.setIndexed(True)
        t2.setStored(True)
        t2.setTokenized(True)
        t2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
        
        with con:
            cur = con.cursor()
            #------step 3------
            cur.execute("SELECT * FROM Writers12")

            numrows = int(cur.rowcount)
            print 'numrows:',numrows
            for i in range(numrows):
                row = cur.fetchone()

                #------step 4------
                people_name = row[NAME]  

                peo_name_unicoded = unicode(people_name, 'utf-8')
                print peo_name_unicoded
                #file.close()
                doc = Document()
                #doc.add(Field("name", filename, t1))
                #doc.add(Field("path", root, t1))
                if len(people_name) > 0:

                    print 'Id:'+str(row[ID])+'--->'+'Name:'+row[NAME]
                    doc.add(Field(FIELD, people_name, t2))
                else:
                    print "warning: no content in %s" % filename
                writer.addDocument(doc)



if __name__ == '__main__':
    if len(sys.argv) !=1:
        print IndexMySql.__doc__
        sys.exit(1)
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    try:
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        IndexMySql(os.path.join(base_dir, INDEX_DIR), StandardAnalyzer(Version.LUCENE_CURRENT))
        end = datetime.now()
        print end - start
    except Exception, e:
        print "Failed: ", e
        raise e
