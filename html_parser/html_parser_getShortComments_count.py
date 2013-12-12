# -*- coding: utf-8 -*-


import os
import time
from lxml import etree



count = 0

htmls_dir = 'htmls-10026897--14325275'

if not os.path.isdir(htmls_dir):
	os.mkdir(htmls_dir)

id_file = './ids/movieId-10026897--14325275'

lines = open(id_file, "r").readlines()
print str(len(lines)) + ' html items remaining...'
oldRemainingLines = lines

assessNumList = []
errorCout = 0

outFilePath =  './result_short_comment/' + '10026897--14325275'
f = open(outFilePath,"w") 

for line in lines:
	eid = line.strip()	
	filename = './'+htmls_dir+'/'+eid+'.html'
	doc = etree.HTML(open(filename, 'r').read().decode('utf-8'))
	count+=1
	try:
		assessNum = doc.xpath("//div[@id='comments-section']/div[@class='mod-hd']/h2/span[@class='pl']/a")
		#print assessNum[0].text.encode('utf-8')
		num = filter(str.isdigit, assessNum[0].text.encode('utf-8'))
		#assessNumList.append(assessNum[0].text)
		#print eid+'|'+assessNum[0].text
		if int(num) != 0:
			f.write(eid+'|'+num+'\n')
		else:
			errorCout+=1
		print eid
	except Exception, e:
		errorCout+=1
		#print e
		#print "don't have this node"
f.close()

#print assessNumList
print " %s html page don't have assess number." % errorCout


'''
#另一种用法
tags = doc.xpath("//div[@class='tags-body']/a")

for t in tags:
	print t.attrib.get('href')

	'''