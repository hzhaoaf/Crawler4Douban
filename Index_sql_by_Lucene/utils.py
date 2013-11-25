#!/usr/bin/python
#coding:utf-8

#rating_av,rating_stars,reviews_c,wish_c,year,

#others like  理应有更加重要的用途


#!usr/bin/bash
#coding:utf-8

import MySQLdb as mdb
from sqlConstants import *
from time import sleep
from datetime import *


def formatYear(yearStr):
	#usage: this function is used for format the 'year' field in sql to the date type in python 
	# 豆瓣的 year 字段 有几种主要的，还有无数狗屎一样的
	# 1. 年份 2011
	# 2. 年月 2011-06
	# 3  年月日 2011-06-01
	# 4  无信息 0000
	# 	1916-1917 1970–1996 	
	# 	2010年
	# 	2010|2011 	
	# 	空
	#   1995/2011
	#   02/05/2012
	wtf = open('wtf.txt','a')

	year = ''
	month = ''
	day = ''
	#try:
	yearStr = unicode(yearStr,'utf-8')# 转换为unicode 之后才可以被[]索引


	if yearStr != '' and yearStr != u'0000'  and yearStr != u'？'  and yearStr!=u'?' and yearStr != u'???' and yearStr != u'待定' and yearStr[0:4]!=u'http' and yearStr!=u'????' and	yearStr != u'Unknown Da' and yearStr != u'不知道' and yearStr!=u'TV Series ' and yearStr!=u'未知':
		if len(yearStr)==4:
			if yearStr[2] == unicode('年','utf-8') and yearStr[3] == unicode('代','utf-8'): #80年代
				year = '19'+yearStr[0:2]
			else:
				year = yearStr[0:4]
		else:
			#print u'-', u'—' ,u'–'
			#三种横线…… 无语了
			if len(yearStr)<4: # some bullshit		195
				year = '0001'
				#------------------------
			elif yearStr[4] == u'-' or yearStr[4] == u'—' or yearStr[4]==u'-' or yearStr[4] == u'－' or yearStr[4] == u'–' or yearStr[4] == u's' or yearStr[4]==u' ' or yearStr[4]==u'.':
			#2011-06,2011-06-01,2011-2012,1990s  2011 夏
				year = yearStr[0:4] #1990s
				if len(yearStr)<=7:#2011-06 2011-  2011 夏
					month = yearStr[5:7]
				else:
					if yearStr[7] == u'-' or  yearStr[7] == u'—' or yearStr[7] == u'－' or yearStr[7] == u'–' or yearStr[7]==u'.': #2011-06-01
						month = yearStr[5:7]
						day = yearStr[8:]
					elif len(yearStr)>5: #2011-2012
						year = yearStr[5:]
					else: #1999-
						year = year[0:4]
			elif yearStr[4] == u'|' or yearStr[4] == u'/' or yearStr[4] == u','  or yearStr[4] == u',' or yearStr[4] == u'~': ## 有待考证
				if yearStr[5:] != u'pre' and yearStr[5] != u'(':  #2001-pre 
					year = yearStr[5:]
				else:
					year = yearStr[0:4]
			elif yearStr[4] == unicode('年','utf-8'): #1999年
				year = yearStr[0:4]
			elif yearStr[4] == u'（' or yearStr[4:5] == ' (': #2001 (usa)
				year = yearStr[0:4]
			
			elif yearStr[4:7] == u' - ' or yearStr[4:7] == u' – ': #2001 - 2002
				if len(yearStr[7:])>3:  #2001 - pre 1992 – 199
					year = yearStr[7:]
				else:
					year = yearStr[0:4]
					

			elif yearStr[2] == u'/':#03/03/2001 
				year = yearStr[-4:]
				month = yearStr[3:5]
				day = yearStr[0:2]

			elif yearStr[0:2] == u'TV':# Tv 2001
				year = yearStr[-4:]

			else:
				year = '0001'




	else:
		year = '0001'
		month = '01'
		day = '01'

	year = year.replace('?','0')
	year = '0001' if year == '' else year
 	month = '01' if month == '' else month
	day = '01' if day == '' else day

	#-一位的数字 比如 1999-1-2 貌似不能在lucene的datatools中解析
	month = u'0'+month if len(month)==1 else month 
	day = u'0'+day if len(day)==1 else day

	mDateStr = year+u'-'+month+u'-'+day

	#最后一次检查几个个别的例子	
	if mDateStr == u'2011-0夏-01':
		mDateStr = u'2011-06-01'
	if mDateStr == u'2001-现在-01':
		mDateStr = u'2010-01-01'
	if mDateStr == u'1982 -01-01':
		mDateStr = u'1982-01-01'	
	if mDateStr == u'1991-12-4':
		mDateStr = u'1991-12-04'

		

	mDateStr = mDateStr.encode('utf-8')
	return mDateStr   

		

	# mDateStr = year+'-01-01'
	# mDate = date(int(year),1,1)





def f(x):
	#usage:it's a real function in math, test in curve.m.

	#z depends the shape of the curve
	z = 0;

	a = 2*z-2;
	b = 3 - 3*z;
	c = z;

	y = a*x*x*x + b*x*x + c*x;
	
	return y 



def f_tu(x):
	#z is f(0.5) , it should be 0.5~1 here
	z = 0.7
	b = 4*z -1
	a = 1-b
	y = a*x*x + b*x
	return y


def f_ao(x):
	#z is f(0.5) , it should be 0~0.5 here
	z = 0.3
	b = 4*z -1
	a = 1-b
	y = a*x*x + b*x
	return y





def getMax():
	#usage: this script is used for getting the max, for normalization

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

			maxDict = {}
			maxDict['ratings_c_max'] = 0

			maxDict['do_c_max'] = 0
			maxDict['collect_c_max']=0
			maxDict['wish_c_max'] =0
			maxDict['comments_c_max']=0
			maxDict['reviews_c_max'] =0
			maxDict['dcw_max'] =0
			maxDict['tr_max'] =0
			maxDict['prob_max'] = 0

			ratings_c_max = 0
			do_c_max = 0
			collect_c_max = 0
			wish_c_max = 0
			comments_c_max = 0
			reviews_c_max = 0
			dcw_max =0
			tr_max = 0
			prob_max = 0


			numrows = int(cur.rowcount)
			for i in range(numrows):
				print i
				row = cur.fetchone()

				tmp_rc = int(row[RATINGS_COUNT])     if row[RATINGS_COUNT] is not None else 0
				tmp_dc = int(row[DO_COUNT])     if row[DO_COUNT] is not None else 0
				tmp_cc = int(row[COLLECT_COUNT])     if row[COLLECT_COUNT] is not None else 0
				tmp_wc = int(row[WISH_COUNT])     if row[WISH_COUNT] is not None else 0
				tmp_cmc= int(row[COMMENTS_COUNT])     if row[COMMENTS_COUNT] is not None else 0
				tmp_rec= int(row[REVIEWS_COUNT])     if row[REVIEWS_COUNT] is not None else 0

				tmp_dcw = tmp_dc+tmp_cc + tmp_wc
				tmp_tr  = float(tmp_wc)/(tmp_cc+tmp_dc) if tmp_dc and tmp_cc ==0 else 0

				#tmp_prob = 0.4*(tmp_rv)*0.3/10) + 0.4* + 0.15*popularity + 0.05*trends


				ratings_c_max  = tmp_rc  if tmp_rc>ratings_c_max else ratings_c_max
				do_c_max       = tmp_dc  if tmp_dc>do_c_max  else do_c_max
				collect_c_max  = tmp_cc  if tmp_cc>collect_c_max else collect_c_max
				wish_c_max     = tmp_wc  if tmp_wc>wish_c_max else wish_c_max
				comments_c_max = tmp_cmc if tmp_cmc>comments_c_max else comments_c_max
				reviews_c_max  = tmp_rec if tmp_rec>reviews_c_max else reviews_c_max
				dcw_max        = tmp_dcw if tmp_dcw>dcw_max else dcw_max
				tr_max         = tmp_tr  if tmp_tr>tr_max else tr_max

			maxDict['ratings_c_max'] =  ratings_c_max
			maxDict['do_c_max'] =  do_c_max
			maxDict['collect_c_max']= collect_c_max
			maxDict['wish_c_max'] = wish_c_max
			maxDict['comments_c_max']= comments_c_max
			maxDict['reviews_c_max'] = reviews_c_max
			maxDict['dcw_max'] = dcw_max
			maxDict['tr_max'] = tr_max


			print 'For the biggest! We made it! Finally !'

			return maxDict



def calcBoostProb(doc_row,maxDict):
	
	#ratings
	rating_av = doc_row[RATING_AVERAGE] if doc_row[RATING_AVERAGE]is not None else 0
	ratings_c = doc_row[RATINGS_COUNT] if doc_row[RATINGS_COUNT]is not None else 0
	#rating_stars = doc_row['rating_stars'] useless because it's just a part of rating_av,every 5 start for half a star 

	#在看 看过 想看
	do_c = doc_row[DO_COUNT]  if doc_row[DO_COUNT] is not None else 0
	collect_c = doc_row[COLLECT_COUNT]  if doc_row[COLLECT_COUNT] is not None else 0
	wish_c = doc_row[WISH_COUNT] if doc_row[WISH_COUNT] is not None else 0

	#评论
	comments_c = doc_row[COMMENTS_COUNT] if doc_row[COMMENTS_COUNT] is not None else 0
	reviews_c = doc_row[REVIEWS_COUNT] if doc_row[REVIEWS_COUNT] is not None else 0

	
	#denorm
	#rating_total_denorm #和下面的区别：所有 av×人数/max(av×人数) 和直接拿 avx人数/10×max(人数) 差不多
	#rating_av_max = float(maxDict['rating_av_max'])
	ratings_c_max  = float(maxDict['ratings_c_max'])
	do_c_max = float(maxDict['do_c_max'])
	wish_c_max =  float(maxDict['wish_c_max'])
	collect_c_max = float(maxDict['collect_c_max'])
	comments_c_max =  float(maxDict['comments_c_max'])
	reviews_c_max =  float(maxDict['reviews_c_max'])
	dcw_max = float(maxDict['dcw_max'])
	tr_max = float(maxDict['tr_max'])


	#normlization !!!
	#越高越好，但是要在一定程度上避免 平均分比较低 但是 评分人数高的电影
	#虽然有时候也需要这样
	rating_total = (rating_av * ratings_c)/(10*ratings_c_max)
	
	#可以反映一个电影的受欢迎程度
	popularity = (do_c + collect_c + wish_c)/dcw_max

	#trends如果太小，那么就说明这个电影已经过气了,而如果wish_c比较多，则说明最近比较火. 注意这个值在normalize之前可能会大于1
	#最近的火热程度
	trends = (wish_c/(collect_c+do_c))/tr_max if collect_c != 0 else 0

	#观后感，反应影片的深刻程度
	impressive = 0.3*comments_c/comments_c_max + 0.7*reviews_c/reviews_c_max

	#temp adjustment
	rating_total = f_tu(rating_total)
	impressive = f_tu(impressive)


	#it is a measure of whether a movie should be addBoost, =1 means it is a  totally good movie which should be boosted
	boostProb = 0.4*(float(rating_av)*0.3/10) + 0.4*impressive + 0.15*popularity + 0.05*trends

	#print rating_total, impressive, popularity, trends
	return boostProb





