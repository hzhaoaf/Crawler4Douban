# -*- coding: utf-8 -*-

import os
import time
from lxml import etree


htmls_dir = 'htmls-10026897--14325275'

if not os.path.isdir(htmls_dir):
	os.mkdir(htmls_dir)

id_file = './ids/movieId-10026897--14325275'

lines = open(id_file, "r").readlines()
print str(len(lines)) + ' html items remaining...'
oldRemainingLines = lines

outFilePath =  './tags/10026897--14325275'

errorCout = 0

for line in lines:
	eid = line.strip()	
	filename = './'+htmls_dir+'/'+eid+'.html'
	outFileName = outFilePath+'/'+'tags-'+eid + '.json' 
	doc = etree.HTML(open(filename, 'r').read().decode('utf-8'))
	print eid
	f = open(outFileName,"w")
	i = 1
	tags = doc.xpath("//div[@class='tags-body']/a")
	myString='{"'
	for t in tags:
		tag_name = doc.xpath("//div[@class='tags-body']/a["+str(i)+"]")
		for t in tag_name:
			myString += t.text.encode("utf-8")
			#print t.text.encode("utf-8")
			#f.write(t.text.encode("utf-8"))
		tag_span = doc.xpath("//div[@class='tags-body']/a["+str(i)+"]/span")
		for t in tag_span:
			#print t.text.strip("()")
			myString += '":"' + t.text.strip("()") + '","'
			#f.write(t.text)
		i+=1
	if myString[-2:]==',"':
		myString = myString[:-2]
	else:
		myString = myString[:-1]
	myString += '}'
	print myString
	f.write(myString)
	f.close()

	'''
	try:
		tags = doc.xpath("//div[@class='tags-body']/a")
		for t in tags:
			tag_name = doc.xpath("//div[@class='tags-body']/a["+str(i)+"]")
			for t in tag_name:
				#print t.text.encode("utf-8")
				f.write(t.text)
			tag_span = doc.xpath("//div[@class='tags-body']/a["+str(i)+"]/span")
			for t in tag_span:
				#print t.text.encode("utf-8")
				f.write(t.text)
			i+=1
		time.sleep(0.5)
	except Exception, e:
		#raise e
		print 'no'
	
	'''
	'''
	for t in tags:
		print t.text.encode("utf-8")
		#time.sleep(1)
		i+=1
	'''

