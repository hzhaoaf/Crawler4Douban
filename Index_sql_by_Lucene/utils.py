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
import operator


def simlifyRetDict(retDict):
	reservedList = ['subject_id','title','directors','year','summary','image_small','rating_average','collect_count','raw_user_tags','countries','score','boost','raw_adjs']
	keyList = retDict.keys()
	for eachKey in keyList:
		if eachKey not in reservedList:
			retDict.pop(eachKey)


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


def scoreDocs2dictList(scoreDocs,searcher):
	#usage:将scoreDoc的转换成dict list的结构
	movieDictList = []
	_pointer = 0 #iterator
	for scoreDoc in scoreDocs:
		movieDictList.append({})
		score = scoreDoc.score
		doc = searcher.doc(scoreDoc.doc)
		fieldsList = doc.getFields()
		for eachField in fieldsList:
			fieldName = eachField.name()
			fieldValue = eachField.stringValue()
			movieDictList[_pointer][fieldName] = fieldValue
		movieDictList[_pointer]['score'] = score
		_pointer = _pointer + 1
	#print movieDictList[0].keys()
	return movieDictList
		
	
def getLevel(num,numArea):
	#usage:用于判断num是否在numArea中，如果不在，取上界或者下界
	scope_len = numArea[1]-numArea[0]
	if num < numArea[0]:
		level = 0.0
	elif num>numArea[1]:
		level = 1.0
	else:
		level = (float(num) - numArea[0])/scope_len
	return level



def basicFeaturesOfMovie(doc_row,statisticDict,dateStr):
	#usage: get a the impressive popularity and the other feature of a movie to reRank
	# it should get all features needed in setBoost and reRank


	#一个傻逼的函数重载,前者用在 sql 查询 后者用在 reRank
	if isinstance(doc_row,tuple):
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

		#时间
		year = int(dateStr)

	elif isinstance(doc_row,dict):
		#ratings
		rating_av = float(doc_row['rating_average']) if doc_row['rating_average']is not None else 0
		ratings_c = int(doc_row['ratings_count']) if doc_row['ratings_count']is not None else 0
		#rating_stars = doc_row['rating_stars'] useless because it's just a part of rating_av,every 5 start for half a star 

		#在看 看过 想看
		do_c = int(doc_row['do_count'])  if doc_row['do_count'] is not None else 0
		collect_c = int(doc_row['collect_count'])  if doc_row['collect_count'] is not None else 0
		wish_c = int(doc_row['wish_count']) if doc_row['wish_count'] is not None else 0

		#评论
		comments_c = int(doc_row['comments_count']) if doc_row['comments_count'] is not None else 0
		reviews_c = int(doc_row['reviews_count']) if doc_row['reviews_count'] is not None else 0

		#时间
		year = int(dateStr)


	#denorm
	#rating_total_denorm #和下面的区别：所有 av×人数/max(av×人数) 和直接拿 avx人数/10×max(人数) 差不多
	#rating_av_max = float(maxDict['rating_av_max'])
	ratings_c_area  = statisticDict['ratings_c_area']
	do_c_area = statisticDict['do_c_area']
	wish_c_area =  statisticDict['wish_c_area']
	collect_c_area = statisticDict['collect_c_area']
	comments_c_area =  statisticDict['comments_c_area']
	reviews_c_area =  statisticDict['reviews_c_area']
	dcw_area = statisticDict['dcw_area']
	tr_area = statisticDict['tr_area']

	#process year
	# yearList = 

	#-----------------
	#all need to return 


	#normlization !!!
	#越高越好，但是要在一定程度上避免 平均分比较低 但是 评分人数高的电影
	#虽然有时候也需要这样
	rating_total = 0 #(rating_av * ratings_c)/(10*ratings_c_max)
	
	#可以反映一个电影的受欢迎程度
	dcw = do_c + collect_c + wish_c
	popularity = getLevel(dcw,dcw_area)

	#trends如果太小，那么就说明这个电影已经过气了,而如果wish_c比较多，则说明最近比较火. 注意这个值在normalize之前可能会大于1
	#最近的火热程度
	trends = 0 #(wish_c/(collect_c+do_c))/tr_max if collect_c != 0 else 0

	#观后感，反应影片的深刻程度 长评显然比短评更有意义
	impressive = 0.2*getLevel(comments_c,comments_c_area) + 0.8*getLevel(reviews_c,reviews_c_area)

	howNew = float(year-firstMovieTime)/(NOW-firstMovieTime)
	print 'howNew' + str(howNew)
	#是不是新电影，新的程度，越小越新
	#new_degree = 20131231 - int(doc.get('year').replace('-',''))

	return rating_av, rating_total, popularity, trends, impressive, howNew



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

def f_contrast(x):
	#目前是 0～10
	coff = [-0.0833,1.2500,-3.1667,-0.0000]
	items = [x*x*x,x*x,x,1]
	y = 0
	for i in range(len(coff)):
		y = y + coff[i]*items[i]
	return y


def insert2HistList(alist,pos):
	#如果list已经够长
	if len(alist)>pos:
		alist[pos] = alist[pos]+1
	else:#不足补零
		for i in range(len(alist),pos):
			alist.append(0)
		alist.append(1)
	return True


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

			histoDict = {}
			histoDict['ratings_c_hist'] = []
			histoDict['do_c_hist'] = []
			histoDict['collect_c_hist']=[]
			histoDict['wish_c_hist'] = []
			histoDict['comments_c_hist']=[]
			histoDict['reviews_c_hist'] =[]
			histoDict['dcw_hist'] =[]
			histoDict['tr_hist'] =[]
			histoDict['prob_hist'] = []


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



				ratings_c_max  = tmp_rc  if tmp_rc>ratings_c_max else ratings_c_max
				do_c_max       = tmp_dc  if tmp_dc>do_c_max  else do_c_max
				collect_c_max  = tmp_cc  if tmp_cc>collect_c_max else collect_c_max
				wish_c_max     = tmp_wc  if tmp_wc>wish_c_max else wish_c_max
				comments_c_max = tmp_cmc if tmp_cmc>comments_c_max else comments_c_max
				reviews_c_max  = tmp_rec if tmp_rec>reviews_c_max else reviews_c_max
				dcw_max        = tmp_dcw if tmp_dcw>dcw_max else dcw_max
				tr_max         = tmp_tr  if tmp_tr>tr_max else tr_max



				histPos = int(tmp_rc/RATINGS_C_LIDU)
				insert2HistList(histoDict['ratings_c_hist' ],histPos)
				histPos = int(tmp_dc/DO_C_LIDU)
				insert2HistList(histoDict['do_c_hist'      ],histPos)
				histPos = int(tmp_cc/COLLECT_C_LIDU)
				insert2HistList(histoDict['collect_c_hist' ],histPos)
				histPos = int(tmp_wc/WISH_C_LIDU)
				insert2HistList(histoDict['wish_c_hist'    ],histPos)
				histPos = int(tmp_cmc/COMMENTS_C_LIDU)
				insert2HistList(histoDict['comments_c_hist'],histPos)
				histPos = int(tmp_rec/REVIEWS_C_LIDU)
				insert2HistList(histoDict['reviews_c_hist' ],histPos)
				histPos = int(tmp_dcw/DCW_LIDU)
				insert2HistList(histoDict['dcw_hist'       ],histPos)
				histPos = int(tmp_tr/TR_LIDU)
				insert2HistList(histoDict['tr_hist'        ],histPos)


			maxDict['ratings_c_max'] =  ratings_c_max
			maxDict['do_c_max'] =  do_c_max
			maxDict['collect_c_max']= collect_c_max
			maxDict['wish_c_max'] = wish_c_max
			maxDict['comments_c_max']= comments_c_max
			maxDict['reviews_c_max'] = reviews_c_max
			maxDict['dcw_max'] = dcw_max
			maxDict['tr_max'] = tr_max



			print 'For the biggest! We made it! Finally !'

			return maxDict,histoDict

maxDict = {
	'comments_c_max': 140283,  #1000为1步
	'ratings_c_max': 470876,  #1000为1步
	'prob_max': 0, 
	'do_c_max': 23873, #1000为1步
	'collect_c_max': 610043, #1000为1步
	'dcw_max': 671908, #1000为1步
	'tr_max': 77.0, ##10为1步
	'wish_c_max': 77535, #1000为1步 
	'reviews_c_max': 5216  #100为1步
}

statisticDict = {
	#思考这样没有什么index的问题，应该是对的,从最简单的（0,1）可思考
	'comments_c_area': (COMMENTS_C_LIDU*2.0,COMMENTS_C_LIDU*88.0),
	'ratings_c_area': (RATINGS_C_LIDU*4.0,RATINGS_C_LIDU*486.0),
	'prob_area':(0,0),
	'do_c_area':(0,0),
	'collect_c_area':(COLLECT_C_LIDU*6.0, COLLECT_C_LIDU*811.0) ,
	'dcw_area': (DCW_LIDU*14.0, DCW_LIDU *1128.0),
	'tr_area':(0, 0),
	'wish_c_area':(WISH_C_LIDU*6.0,WISH_C_LIDU*310.0),
	'reviews_c_area': (REVIEWS_C_LIDU*1.0,REVIEWS_C_LIDU*255.0) #这个255 是自己看的

}


def calcBoostProb(doc_row,maxDict,dateStr):

	rating_av, rating_total, popularity, trends, impressive , howNew = basicFeaturesOfMovie(doc_row,statisticDict,dateStr)
	
	#temp adjustment
	rating_total = rating_total
	impressive = impressive

	#稀疏因子，因为rating_av/10 的结果相对数值比较大，而impressive的结果比较小
	#一个好的加权，应该保证这几个维度上的数值都在差不多的范围
	sparse = 0.3
	#评分比较差的，就让它更差
	#rating_av = f_contrast(rating_av)
	#print 'rating_av adjusted:'+str(rating_av)

	#it is a measure of whether a movie should be addBoost, =1 means it is a  totally good movie which should be boosted
	boostProb = 0.65*(rating_av/10) + (0.15*impressive + 0.1*popularity) +0.1*howNew

	print 'rating_av:'+str(rating_av), 'impressive:'+str(impressive), 'popularity:'+str(popularity),'trends'+str(trends)
	# if boostProb>0.8:
	# 	exit()
	return boostProb

def getFieldValueInCommand(command,field):
	#usage: return a Value of field in command in the type of list
	#！！！！！！！！！！！！！服务器的时候 不要下面这句话
	command = unicode(command,'utf-8')
	offset = command.find(field)
	if  offset >= 0: #说明使用了field搜索 
		offset = offset + len(field) + 1 #get to the position after the ':' of the field
		start = offset 

		while offset<len(command):
			if command[offset] != ':':
				offset = offset + 1
			else:
				break
		tag_ = command[start:offset] #it's like 'tag1 tag2 NextField '
		if tag_[-1] == u':':
			tag_list = tag_.split(u' ')[0:-1] #get rid of the 'NextFiled'
		else:
			tag_list = tag_.split(u' ') #get rid of the 'NextFiled'
		return tag_list
	else:
		return False

def getTagValueInRawTags(raw_user_tags,tag):
	#usage: return a num of tag in raw_user_tags in the type of list
	offset = raw_user_tags.find(tag)
	if  offset >= 0: #说明使用了field搜索 
		offset = offset + len(tag) #get to the next position of the field
		start = offset 

		while offset<len(raw_user_tags):
			if raw_user_tags[offset] != u'￥':
				offset = offset + 1
			else:
				break
		num_ = raw_user_tags[start:offset] #it's like '<>123'
		tag_num = int(num_[2:]) #get rid of the '<>'
		if tag_num == 0:
			exit('error when analyzing the raw_user_tags')
		return tag_num
	else:
		return False

def getAdjValueInRawAdjs(raw_adjs,adj):
	#usage: return a num of adj in raw_user_tags in the type of list
	offset = raw_adjs.find(adj)
	if  offset >= 0: #说明 含有 adj字串
		offset = offset + len(adj) #get to the end position of the next adj
		start = offset 

		#这一块是叫 offset 往前走，有两种可能停下来 1.遇到',' 2.到结尾
		while offset<len(raw_adjs):
			#往前走，知道遇见一个 ','
			if raw_adjs[offset] != u',':
				offset = offset + 1
			else:
				break
		num_ = raw_adjs[start:offset] #it's like '=12.0'
		adj_num = int(float(num_[1:])) #get rid of the '='
		if adj_num == 0:
			exit('error when analyzing the raw_adjs')
		return adj_num
	else:
		return False


def reRank(movieDictList,maxDict,command=None,rankFlag = None):
	#reRank的最核心的意义在于将command 信息融入，可以弥补一些缺陷比如 user_tags后的人数对加权的作用有限
	#rankFlag 是按照什么排序，如果该值为 None，直接reRank
	for eachDict in movieDictList:
		boost = 1 # 初始boost
		times = 1 # 倍数

		# rating_av, rating_total, popularity, trends, impressive,howNew = basicFeaturesOfMovie(eachDict,maxDict)

		#process tags
		tag_list = getFieldValueInCommand(command,'user_tags')
		if tag_list: #exist,说明用户搜索了该域
			for eachTag in tag_list: #再raw中搜索每个再command中出现的tag
				raw_tags = eachDict['raw_user_tags']
				tag_num = getTagValueInRawTags(raw_tags,eachTag)
				if tag_num:
					times = times*(1 + tag_num*TAG_NUM_FACTOR) #0.0001 now

		#process adjs
		adj_list = getFieldValueInCommand(command,'adjs')
		if adj_list:
			for eachAdj in adj_list:
				raw_adjs = eachDict['raw_adjs']
				adj_num = getAdjValueInRawAdjs(raw_adjs,eachAdj)
				# if adj_num:
					# times = times*(1+adj_num*ADJ_NUM_FACTOR)



		boost = boost * times
		eachDict['score'] = eachDict['score']*boost

		simlifyRetDict(eachDict)

	retMovieList = sorted(movieDictList, key=operator.itemgetter('score'), reverse=True)  
	return retMovieList






#debug area 

#print getAdjValueInRawAdjs('哈哈=23,呵呵=90','哈哈')

# a = [1,5]
# insert2HistList(a,5)
# print a

# import json 

# maxDict,histoDict = getMax()
# print maxDict
# histoDictStr = json.dumps(histoDict)
# with open('./statistic.txt','w') as f:
# 	f.write(histoDictStr)






















