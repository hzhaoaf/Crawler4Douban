#!/usr/bin/python
#coding:utf-8

#rating_av,rating_stars,reviews_c,wish_c,year,

#others like  理应有更加重要的用途


#!usr/bin/bash
#coding:utf-8

import MySQLdb as mdb
from sqlConstants import *
from time import sleep




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





