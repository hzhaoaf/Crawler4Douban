#!usr/bin/bash
#coding:utf-8

with open('./allSetsDict_formated.txt','a') as ff:

	with open('./allSetsDict.txt','r') as f:
		lastLine = ''
		line = f.readline()
		firstLineLen = f.tell()
		while(line):
			if lastLine == '\n' or f.tell() == firstLineLen: #读完第一行
				fieldName = line
				print fieldName[0:-1]
			else: #the terms in a field
				if line != '\n': #空域
					ff.write(line[0:-1]+'<￥>'+fieldName[0:-1]+'\n')
				else:
					pass

			lastLine = line
			line = f.readline()

		f.close()
	ff.close()


