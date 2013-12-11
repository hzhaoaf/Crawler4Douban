# -*- coding: utf-8 -*-
import os
import time
from lxml import etree

start_time = time.time()

count = 0

htmls_dir = './3264227--4144377'

id_file = './id/ShortCommentsId-3264227--4144377'

lines = open(id_file, "r").readlines()
print str(len(lines)) + ' html items remaining...'
oldRemainingLines = lines

errorCout = 0
errorlist = []

outFilePath =  './result_short_comments_json/3264227--4144377'

for line in lines:
	eid = line.strip().split('|')[0]
	num = int(line.strip().split('|')[1])
	outFileName = outFilePath+'/'+eid + '.json' 
	if os.path.exists(outFileName):
		continue
	f = open(outFileName,"w")
	count+=1
	myString='{'
	if num > 1000:
		end = 50
	else:
		end = num / 20 + 1
	try:
		for i in range(end):
			start = i*20
			inFilePath = htmls_dir+'/'+eid+'/'+str(start)+'.html'
			doc = etree.HTML(open(inFilePath, 'r').read().decode("utf-8"))
			nameList = doc.xpath("//div[@class='comment']/h3/span[@class='comment-info']/a")
			listLength =  len(nameList)
			#print listLength
			for i in range(listLength):
				try:
					name = doc.xpath("//div[@class='comment']/h3/span[@class='comment-info']/a")[i].text.encode("utf-8")
					name = name.replace('"','')
					name = name.replace('\\','')
				except Exception, e:
					name = ''
				try:
					p0 = doc.xpath("//div[@class='comment']/p")[i].text.strip().encode("utf-8")
					p1=''
					for line in p0:
						p1 += line.rstrip()
					p1 = p1.replace('"','')
					p = p1.replace('\\','')
				except Exception, e:
					p=''
				try:
					date = doc.xpath("//div[@class='comment']/h3/span[@class='comment-info']/span[2]")[i].text.strip()
				except Exception, e:
					date=''
				try:
					votenum = doc.xpath("//span[@class='votes pr5']")[i].text
				except Exception, e:
					votenum=''
				try:
					star = doc.xpath("//h3/span[@class='comment-info']/span[@title]")[i].attrib.get("title").encode("utf-8")
				except Exception, e:
					star=''
				myString += '\n"'+name+'":{"p":"'+p+'","date":"'+date+'","votenum":"'+votenum+'","star":"'+star+'"},'
				#print star.attrib.get("title").encode("utf-8")
				#print name
				#print p
				#print date
				#print votenum
		myString = myString[:-1]
		myString+='}'
		f.write(myString)
		f.close()
		print myString
	except Exception, e:
		errorlist.append(eid)
		print errorlist
	
end_time = time.time()
print 'cost   ' +str(end_time-start_time)


print errorlist


'''
#check json exist by id

cout = 0
id_file = './id/ShortCommentsId-2389939--3264139'

lines = open(id_file, "r").readlines()
mSum = len(lines)
print 'mSum = ' + str(mSum)
outFilePath =  './result_short_comments_json/2389939--3264139'
for line in lines:
	eid = line.strip().split('|')[0]
	outFileName = outFilePath+'/'+eid + '.json' 

	if os.path.exists(outFileName):
		cout += 1

print 'not in = '+ str(mSum - cout)

'''
