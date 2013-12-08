# -*- coding: utf-8 -*-

import os
import time
import sampleComment

#计数器
count = 0
score = 0
#时间
start_time = time.time()
end_time = time.time()

#html资源文件夹
htmls_dir = './html/';
if not os.path.isdir(htmls_dir):
	os.mkdir(htmls_dir)
	
#要操作的id文件
id_file = './ShortCommentsId-1920713--2389554'

lines = open(id_file, "r").readlines()
for line in lines:
	eid = line.strip().split('|')[0]
	assessNum = line.strip().split('|')[1]
	print 'now is dealing with %s '% eid
	#调用爬虫程序 传入eid和该id对应的短评数
	try:
		sampleComment.CrawlCommentsById(eid , int(assessNum) , htmls_dir)
	except Exception, e:
		print 'this round error'
	#sampleComment.CrawlComments(eid , int(assessNum) , htmls_dir)
	count += 1
	if count % 10 ==0:
		print 'crawl %s th id:%s, total cost %.2fmin' % (count, eid, (time.time() - start_time) / 60.0)

	if count % 3 == 0:
		break;

if True:
	lines = open(id_file, "r").readlines()
    lines = lines[count:]
    f = open(id_file, "w+")
    [f.write('%s' % l) for l in lines]
    f.close()
    print 'rewrite txt,delete %s' % (count)
    
if len(oldRemainingLines) < 3:
	print 'there are 3 files remain'

	'''
	if int(assessNum) >10:
		newfile.write(eid+'|'+assessNum+'\n')
		
		if int(assessNum)>1000:
			score+=1000
		else:
			score += int(assessNum)
		count+= 1
	print count
	'''

print 'ALL Finished!'