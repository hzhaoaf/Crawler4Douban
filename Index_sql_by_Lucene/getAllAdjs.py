#!usr/bin/bash
#coding:utf-8
#usage:将所有comments和summary分词，并将已抽取出来adj的和为抽取出adj的分别放入fenciAdj和fenciDataRaw
#运行之后查看write_err_raw.txt 记录写入raw的错误的id
#运行之后查看fenci_err_raw.txt 记录分词的错误的id

# 1.首先分词得到分词之后的文件以及挑选出形容词的文件
# 2.对形容词文件进行索引 indexAdjFiles
# 3.统计 countTerms_adj
# 4.选择前几名 getTopAdj

import MySQLdb as mdb
from sqlConstants import *
from time import sleep
import codecs
import PyNLPIR
from time import time as now 

#usage: this script is used for get files of text after split words
import sys
import locale
import json
import os

reload(sys)
sys.setdefaultencoding('UTF-8')

def p(f):
    print '%s.%s(): %s' % (f.__module__, f.__name__, f())

# 返回使用UCS-2还是UCS-4
print sys.maxunicode

# 检查标准输出流的编码
print sys.stdout.encoding

# 返回当前系统所使用的默认字符编码
p(sys.getdefaultencoding)

# 返回用于转换Unicode文件名至系统文件名所使用的编码
p(sys.getfilesystemencoding)

# 获取默认的区域设置并返回元祖(语言, 编码)
p(locale.getdefaultlocale)

# 返回用户设定的文本数据编码
# 文档提到this function only returns a guess
p(locale.getpreferredencoding)

def utf8ToGbk(str_utf8):
    str_uni = unicode(str_utf8,'utf-8')
    str_gbk = ''
    for eachChar in str_uni:
        try:
            char_gbk =  eachChar.encode('gbk')
        except:
            #print 'gbk have no' + eachChar
            char_gbk =  u' '.encode('gbk')
        str_gbk = str_gbk + char_gbk
    return str_gbk

def uni8ToGbk(str_uni):
    str_gbk = ''
    for eachChar in str_uni:
        try:
            char_gbk =  eachChar.encode('gbk')
        except:
            #print 'gbk have no' + eachChar
            char_gbk =  u' '.encode('gbk')
        str_gbk = str_gbk + char_gbk
    return str_gbk

def getAdjs(words_str):
    words_list =  words_str.split(' ')
    adjs = ''
    for eachWord in words_list:
        offset = eachWord.find('/a')
        if offset > 0: #说明是形容词
            eachWord = eachWord[0:offset]
            adjs = adjs + ' ' + eachWord
    return adjs

def write2File():
    pass

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)






#---------config here----
baseDir = '/home/rio/workspace/lucene/'
dbName = 'moviedata'
commentsDir = '/home/rio/workspace/commentsData/'

userDictPath = baseDir + 'allCasts.txt'

con = mdb.connect('localhost','root','testgce',dbName)
#used for getting comments 
con2 = mdb.connect('localhost','root','testgce',dbName)

#---pyNLPIR---
PyNLPIR.nlpir_init('.', 'UTF-8')
#添加语料库
PyNLPIR.nlpir_import_user_dict(userDictPath)

with open(baseDir+'last.txt','r') as rec:
    last = int(rec.read())

with con:
        # Careful with codecs
        con.set_character_set('utf8')

        cur = con.cursor()
        # Aagin the codecs
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;') 
        cur.execute("SELECT * FROM movie_items")
        
        cur2 = con2.cursor()
        # Aagin the codecs
        cur2.execute('SET NAMES utf8;')
        cur2.execute('SET CHARACTER SET utf8;')
        cur2.execute('SET character_set_connection=utf8;')

        numrows = int(cur.rowcount)

        print 'numrows:',numrows
        idList = []
        resList = []
        adjList = []
        count = 0
        #last = 4567
        for i in range(last,numrows):

            print 'index:'+str(i)
            print 'count:'+str(count)

            #make dirs 每10000个(左右)重新建立一个文件夹
            folderID = i/10000
            rawDir = baseDir+'fenciDataRaw/'+str(folderID)
            adjDir = baseDir+'fenciAdj/'+str(folderID)
            if folderID*10000 == i: #说明这10000刚开头
                if not os.path.isdir(rawDir):
                    os.mkdir(rawDir)
                if not os.path.isdir(adjDir):
                    os.mkdir(adjDir)

            if 0:
                print u"0.3秒后,程序将重启..."
                #如果不关闭，会出现too many connections ！
                con.close()
                con2.close()
                sleep(0.3)
                restart_program()

           


            cur.scroll(i,'absolute') #如果i是30,就从下一句fetchone将得到index为30的row
            row = cur.fetchone()

            #---1.get comments---
            comments = ''
            subject_id = row[SUBJECT_ID]
            title = row[TITLE]
            rating_average = row[RATING_AVERAGE]
            comments_count = row[COMMENTS_COUNT]
            # print 'id:'+subject_id
            # sql = "SELECT user_comment FROM short_comments WHERE subject_id = " + subject_id
            # cur2.execute(sql)
            # comments_num = int(cur2.rowcount)
            # #print 'comments number: ' + str(comments_num)
            # for j in range(comments_num):
            #     row2 = cur2.fetchone()
            #     comments = comments + ' ' + row2[0] # user_comment
            jsonPath = commentsDir+subject_id+'.json' 
            if os.path.exists(jsonPath):
                with open(jsonPath,'r') as commentsJson:
                    commDict =  json.loads(commentsJson.read())
                for eachKey in commDict:
                    comments = comments + ' ' + commDict[eachKey]['p']




            #---2.get summary---
            summary = row[SUMMARY]

            #---3.get user_tags---
            user_tags_raw = row[USER_TAGS]
            user_tags = ''
            if user_tags_raw!='':
                user_tags_list = user_tags_raw.split(delim)
                user_tags_set = set()
                for eachTag_pair in user_tags_list:
                    if eachTag_pair!='':  #开始或者结尾的'￥'可能分割之后会有空字符串
                        user_tags = user_tags + eachTag_pair.split(delim_uo)[0] #[0] 是真正的tag，[1]是一个人数
            


            # ---fenci start---
            try:
                if comments != '' and comments != None:
                    comments_gbk = uni8ToGbk(comments)  #json.loads() 使comments变成了unicode
                    comments_ = PyNLPIR.nlpir_paragraph_process(comments_gbk, True)
                else:
                    comments_ = ''


                if summary != '' and summary != None:
                    summary_gbk = utf8ToGbk(summary)
                    summary_ = PyNLPIR.nlpir_paragraph_process(summary_gbk, True)
                else:
                    summary_ = ''

                if user_tags != '' and user_tags != None:
                    user_tags_gbk = utf8ToGbk(user_tags)
                    #出现段错误的index！！！！！！
                    if i not in [4568,6471,9311,21310,41248,42070,42524,70616,76265]: #[4568,6471,21310,41248,42070,42524,70616,76265]:
                        user_tags_ = PyNLPIR.nlpir_paragraph_process(user_tags_gbk, True)
                else:
                    user_tags_ = ''
            except:
                with open(baseDir+'fenci_err.txt','a') as err:
                    err.write(subject_id+'\n')
            
            #---fenci end---

            #---append to three list---
            idList.append(subject_id)

            fenciDict = {}
            fenciDict['comments'] = comments_ # 得到的是utf8编码的哦
            fenciDict['summary']  = summary_
            fenciDict['user_tags'] = user_tags_
            resList.append(fenciDict)


            #---get adjs---
            adjDict = {}
            comments_adjs = getAdjs(comments_)
            summary_adjs = getAdjs(summary_)
            user_tags_adjs = getAdjs(user_tags_)


            adjDict['title'] = title 
            adjDict['rating_average'] = rating_average
            adjDict['comments_count'] = comments_count
            adjDict['comments_adjs'] = comments_adjs 
            adjDict['summary_adjs']  = summary_adjs
            adjDict['user_tags_adjs'] = user_tags_adjs
            adjList.append(adjDict)


            #---write---
            count  = count + 1

            NUM = 30
            # 1~100 一共100个
            if count == NUM or i==(numrows-1):
                for eachId in idList:
                    print eachId
                
                for k in range(count):
                    with open(rawDir+'/' + idList[k]+'_res.json','w') as recFile:
                        try:
                            jsonStr = json.dumps(resList[k])
                            recFile.write(jsonStr)
                        except:
                            with open(baseDir+ 'write_err_raw.txt','a') as f:
                                f.write(subject_id+'\n')
                        recFile.close()



                    with open(adjDir+'/' + idList[k]+'_adj.json','w') as recFile2:
                        jsonStr = json.dumps(adjList[k])
                        recFile2.write(jsonStr)

                        if jsonStr.find('title') < 0:
                            print title
                            print adjDict   
                            exit()
                        recFile2.close()

                count = 0
                idList = []
                resList = []
                adjList = []

                with open(baseDir+'last.txt','w') as rec:
                    rec.write(str(i))

            #---write end ---


            #print get_time,fenci_time,append_time,write_time,all_time
            #print sql_time


PyNLPIR.nlpir_exit()

print 'Yeah! we\'ve got all the adjs!'

