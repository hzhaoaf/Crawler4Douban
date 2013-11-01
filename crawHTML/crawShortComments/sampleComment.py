import urllib2
import time
import os

import fileUtils


#eid = '3718424'
#start = 0

'''
for i in range(0,50):
	start = i*20
	url = 'http://movie.douban.com/subject/' + eid + '/comments?start=' + str(start) + '&limit=20&sort=new_score'
	print url
	data = urllib2.urlopen(url).read()
	path = './html/' + eid + '/' + str(start) + '.html'
	fileUtils.writeTo(path,data,'w')
	time.sleep(2)
	print 'OK'
'''




def CrawlComments(eid , num ,htmls_dir):
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
			#print url
			data = urllib2.urlopen(url).read()
			path = htmls_dir + eid + '/' + str(start) + '.html'
			#print path
			fileUtils.writeTo(path,data,'w')
			time.sleep(2)
	#print end
	print eid + '    OK'


#CrawlComments('1298189',27020)
