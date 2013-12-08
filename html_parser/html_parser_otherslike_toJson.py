# -*- coding: utf-8 -*-
import os
import time
from lxml import etree

count = 0

htmls_dir = './DetailHtml/htmls-5342058--6986033'

if not os.path.isdir(htmls_dir):
	os.mkdir(htmls_dir)

id_file = './ids/movieId-5342058--6986033'

lines = open(id_file, "r").readlines()
print str(len(lines)) + ' html items remaining...'
oldRemainingLines = lines

errorCout = 0

outFilePath =  './result_others_like/5342058--6986033'

for line in lines:
	eid = line.strip()	
	filename = './'+htmls_dir+'/'+eid+'.html'
	outFileName = outFilePath+'/'+'otherslike-'+eid + '.json' 
	doc = etree.HTML(open(filename, 'r').read().decode('utf-8'))
	print eid
	f = open(outFileName,"w")
	count+=1
	myString='{'
	try:
		href = doc.xpath("//div[@class='recommendations-bd']/dl/dd/a")
		myString+='"'
		if href:
			for i in href:
				id = i.attrib.get('href')[32:-19]
				myString += (id +'":"')
				myString += (i.text.encode("utf-8")+'","')				
		else:
			errorCout+=1
	except Exception, e:
		errorCout+=1
		#print e
		#print "don't have this node"
	if myString[-2:]==',"':
		myString = myString[:-2]
	else:
		myString = myString[:-1]
	myString += '}'
	print myString
	f.write(myString)
f.close()

#print assessNumList
print " %s html page don't have assess number." % errorCout
