# -*- coding: utf-8 -*-

import os

count = 0
htmls_dir = 'html_short_comment';
if not os.path.isdir(htmls_dir):
	os.mkdir(htmls_dir)

id_file = './result/10342838--14238760'

lines = open(id_file, "r").readlines()

for line in lines:
	eid = line.strip().split('|')[0]
	assessNum = line.strip().split('|')[1]
	print assessNum
	'''
	if int(assessNum) < 1000:
		print '<<<<<<<<<'
	else:
		print '>>>>>>>>>'
	'''
	