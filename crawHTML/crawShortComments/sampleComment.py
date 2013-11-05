# -*- coding: utf-8 -*-

import urllib2
import time
import os
import cookielib
import sys
import socket

import fileUtils

socket.setdefaulttimeout(100)


def CrawlCommentsById(eid , num , htmls_dir):

        cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
	opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
	urllib2.install_opener(opener)
	
	start = 0
	if not os.path.isdir( htmls_dir + eid):
		os.mkdir( htmls_dir + eid)		
	
	if num > 1000:
		end = 50
	else:
		end = num / 20 + 1

	for i in range(0,end):
			start = i*20
			url = 'http://movie.douban.com/subject/' + eid + '/comments?start=' + str(start) + '&limit=20&sort=new_score'
			print url
			try:
				data = urllib2.urlopen(url).read()
			except Exception, e:
				data = 'no data'
				print 'this id : %s  has some error' % eid
							
			path = htmls_dir + eid + '/' + str(start) + '.html'
			#print path
			fileUtils.writeTo(path,data,'w')
			time.sleep(2)
	print eid + '    OK'
	


def CrawShortComments(htmls_dir,id_file):
	#计数器
	count = 0
	score = 0
	#时间
	start_time = time.time()
	end_time = time.time()	

	lines = open(id_file, "r").readlines()
	oldRemainingLines = lines
	for line in lines:
		eid = line.strip().split('|')[0]
		assessNum = line.strip().split('|')[1]
		print 'now is dealing with %s '% eid
		#调用爬虫程序 传入eid和该id对应的短评数
		try:
			CrawlCommentsById(eid , int(assessNum) , htmls_dir)
		except Exception, e:
			print 'this round error'
		count += 1
		if count % 10 ==0:
			print 'crawl %s th id:%s, total cost %.2fmin' % (count, eid, (time.time() - start_time) / 60.0)
			break;

	if True:
                #print 'count = %s, lines = %s' % (count, len(lines))
                time.sleep(1)
                lines = open(id_file, "r").readlines()
                lines = lines[count:]
                f = open(id_file, "w+")
                [f.write('%s' % l) for l in lines]
                f.close()
                print 'rewrite txt,delete %s' % (count)

        if len(oldRemainingLines) < 5:
                print 'All Done, Program will exit!'
                return 0,count
        else:
                print 'Processed %s html items...' % (count)
                return 1,count




#CrawlComments('1298189',27020)
