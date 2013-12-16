#!usr/bin/bash
#coding:utf-8

import MySQLdb as mdb
from sqlConstants import *
from time import sleep
import codecs

def printDict(dic,f):
    #print dic
    for eachKey in dic.keys():
        f.write(eachKey+'\n')
        for eachVal in dic[eachKey]:
            if eachVal!='':
                print eachVal
                try:
                    eachVal.decode('utf-8') #test the encoding
                except Exception,e:
                    print "cant decode" + eachVal
                    #eachVal = eachVal.encode('utf-8')
                try:
                    f.write(eachVal+'\n')
                except Exception,e:
                    print 'cant write:'+eachVal+'||'+str(e)
        f.write('\n')
        

#usage: this script is used for getting the set of some classes or properties of the movies

con = mdb.connect('localhost','root','testgce','moviedata')

with con:
        # Careful with codecs
        con.set_character_set('utf8')

        cur = con.cursor()
        # Aagin the codecs
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')
        
        cur.execute("SELECT * FROM movie_items")

        allSetsDict = {}

        for eachFieldName in fields_name_list:
        	allSetsDict[eachFieldName] = set()

        numrows = int(cur.rowcount)
        print 'numrows:',numrows
        for i in range(numrows):
            print i
            row = cur.fetchone()

            
            
            allSetsDict[fields_name_list[YEAR]     ].add(row[YEAR])
            #allSetsDict[fields_name_list[SUBJECT_ID]].add(row[SUBJECT_ID])
            
            #牢记这个set的union方法是不改变原始的set对象的！！！            
            allSetsDict[fields_name_list[CASTS]     ] = allSetsDict[fields_name_list[CASTS]     ].union(set(row[CASTS    ].split(delim)))
            allSetsDict[fields_name_list[DIRECTORS] ] = allSetsDict[fields_name_list[DIRECTORS] ].union(set(row[DIRECTORS].split(delim)))

            
            allSetsDict[fields_name_list[GENRES]    ] = allSetsDict[fields_name_list[GENRES]    ].union(set(row[GENRES   ].split(delim)))
            #allSetsDict[fields_name_list[AKA]       ] = allSetsDict[fields_name_list[AKA]       ].union(set(row[AKA      ].split(delim)))
            allSetsDict[fields_name_list[COUNTRIES] ] = allSetsDict[fields_name_list[COUNTRIES] ].union(set(row[COUNTRIES].split(delim)))


            
            #deal with the user_tags
            user_tags_str = row[USER_TAGS]
            if user_tags_str!='':
                user_tags_list = user_tags_str.split(delim)
                user_tags_set = set()
                for eachTag_pair in user_tags_list:
                    if eachTag_pair!='':  #开始或者结尾的'￥'可能分割之后会有空字符串
                        user_tags_set.add(eachTag_pair.split(delim_uo)[0]) #[0] 是真正的tag，[1]是一个人数
                allSetsDict[fields_name_list[USER_TAGS] ] = allSetsDict[fields_name_list[USER_TAGS] ].union(user_tags_set)
            
            #others like 不用存储

            allSetsDict[fields_name_list[SUBTYPE]   ].union(set(row[SUBTYPE  ].split(delim)))

            #for debug
            if i==100:
                print i 
                # print row[COUNTRIES]
                # print allSetsDict['countries']
                # for each in allSetsDict['countries']:
                #     print each.decode('utf-8')
                # with codecs.open('./tmp.txt','w') as tmp:
                #     tmp.write(each)

                s = row[USER_TAGS]
                print s
                print type(s)
                print isinstance(s, unicode) 

                with open('./allSetsDict.txt','w') as recFile:
                    printDict(allSetsDict,recFile)
#最后一次写入
with open('./allSetsDict.txt','w') as recFile:
    printDict(allSetsDict,recFile)
    #recFile.write(str(allSetsDict))



print 'For the union! We made it! Finally !'

