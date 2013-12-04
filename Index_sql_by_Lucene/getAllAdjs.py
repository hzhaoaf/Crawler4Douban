#!usr/bin/bash
#coding:utf-8

import MySQLdb as mdb
from sqlConstants import *
from time import sleep
import codecs
import PyNLPIR

#usage: this script is used for get files of text after split words
import sys
import locale
import json

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
            print 'gbk have no' + eachChar
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

# test = '哈哈/a 呵呵/a af/x'
# print getAdjs(test)
# exit()

#---pyNLPIR---
PyNLPIR.nlpir_init('.', 'UTF-8')
#PyNLPIR.nlpir_setposmap(ICT_POS_MAP_SECOND)



con = mdb.connect('localhost','root','testgce','moviedata')
#used for getting comments 
con2 = mdb.connect('localhost','root','testgce','moviedata')

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
        for i in range(numrows):
            print i
            row = cur.fetchone()

            #get comments 
            comments = ''
            subject_id = row[SUBJECT_ID]
            #subject_id = '6015756'
            print subject_id
            #cur2.execute("SELECT * FROM short_comments WHERE subject_id = 6015756")
            sql = "SELECT user_comment FROM short_comments WHERE subject_id = " + subject_id
            cur2.execute(sql)
            comments_num = int(cur2.rowcount)
            print 'comments number: ' + str(comments_num)
            for j in range(comments_num):
                row2 = cur2.fetchone()
                comments = comments + ' ' + row2[0] # user_comment

            #get summary
            summary = row[SUMMARY]

            #deal with the user_tags
            user_tags_raw = row[USER_TAGS]
            #get user_tags
            user_tags = ''
            if user_tags_raw!='':
                user_tags_list = user_tags_raw.split(delim)
                user_tags_set = set()
                for eachTag_pair in user_tags_list:
                    if eachTag_pair!='':  #开始或者结尾的'￥'可能分割之后会有空字符串
                        user_tags = user_tags + eachTag_pair.split(delim_uo)[0] #[0] 是真正的tag，[1]是一个人数
            

            # -------
            if comments != '' and comments != None:
                comments_gbk = utf8ToGbk(comments)
                comments_ = PyNLPIR.nlpir_paragraph_process(comments_gbk, True)
            else:
                print 'no comments'
                comments_ = ''

            if summary != '' and summary != None:
                summary_gbk = utf8ToGbk(summary)
                summary_ = PyNLPIR.nlpir_paragraph_process(summary_gbk, True)
            else:
                print 'no summary'
                summary_ = ''

            if user_tags != '' and user_tags != None:
                user_tags_gbk = utf8ToGbk(user_tags)
                user_tags_ = PyNLPIR.nlpir_paragraph_process(user_tags_gbk, True)
            else:
                print 'no user_tags'
                user_tags_ = ''
     
            #---pyNLPIR---



            fenciDict = {}
            fenciDict['comments'] = comments_ # 得到的是utf8编码的哦
            fenciDict['summary']  = summary_
            fenciDict['user_tags'] = user_tags_
            with open('/home/rio/workspace/lucene/fenciDataRaw/' + subject_id+'_res.json','w') as recFile:
                recFile.write(json.dumps(fenciDict))
                #others like 不用存储

            #get adjs
            comments_adjs = getAdjs(comments_)
            summary_adjs = getAdjs(summary_)
            user_tags_adjs = getAdjs(user_tags_)
            adjDict = {}
            adjDict['comments_adjs'] = comments_adjs 
            adjDict['summary_adjs']  = summary_adjs
            adjDict['user_tags_adjs'] = user_tags_adjs

            with open('/home/rio/workspace/lucene/fenciAdj/' + subject_id+'_adj.json','w') as recFile:
                recFile.write(json.dumps(adjDict))



PyNLPIR.nlpir_exit()

print 'Yeah! we\'ve got all the adjs!'

