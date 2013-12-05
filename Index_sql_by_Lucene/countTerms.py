#!usr/bin/bash
#coding:utf-8

import lucene
import os
import sys
from java.io import File
from org.apache.lucene.index import DirectoryReader,MultiFields,Term
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher,DocIdSetIterator
from org.apache.lucene.util import BytesRefIterator


import math
import numpy as np
from scipy.sparse import coo_matrix

#索引存放位置
INDEX_DIR = "/home/env-shared/NGfiles/lucene_index"


lucene.initVM(vmargs=['-Djava.awt.headless=true'])
base_dir = os.path.dirname(os.path.abspath(sys.argv[0])) #py文件所在的目录
directory = SimpleFSDirectory(File(os.path.join(base_dir, INDEX_DIR)))
indexReader = DirectoryReader.open(directory)

liveDocs = MultiFields.getLiveDocs(indexReader)
fields = MultiFields.getFields(indexReader)
convert = lambda term: term.utf8ToString()  #将byteRef类型转码成string

#要建立特征的域
field_ = 'summary'


#总文档数目
numDocs = indexReader.maxDoc()-1

def idf(docFreq,numDocs):
	#usage:根据docFreq 和 numDocs 计算 idf值（依据的是lucene的idf计算公式）
	factor= float(numDocs)/(docFreq+1)
	idf = 1+math.log(factor,2)
	return idf

def appendZero2Matrix(termsMatrix):
	#usage：动态append元素到mat的每一行
	#使用 list嵌套list的matrix
	docNums =  len(termsMatrix)
	for i in range(docNums):
		termsMatrix[i].append(0)
	return termsMatrix

def formatWriteMatrix(mat,f):
	#usage:write a matrix to a file in a decent format
	#mat is a numpy 2-d matrix
	shape = mat.shape
	rows = shape(0)
	columns = shape(1)
	for r in range(rows):
		for c in range(columns):
			numStr = str(mat[r,c])
			if len(numStr)<5: #假设每个数字占5格
				numStr = (5-len(numStr))*'0' + numStr
			f.write(numStr + ' ')
		f.write('\n')
	f.close()
	print '写入完成！～'
	return None



# lucene：idf 公式
# idf(t)  =   	1 + log ( 	
# numDocs
# –––––––––
# docFreq+1
# 	)


#用来记录特征矩阵
termsFile = open('termsMatrix.txt','w')

#动态分配 使用list
# #termsMatrix = [[]]*numDocs  #不能使用这种形式，这是浅拷贝
# termsMatrix = []
# for i in range(numDocs+1): #这里+1 是因为 lucene的doc的id是从1开始的
# 	termsMatrix.append([])  #这就ok了

#静态分配内存 使用numpy的zeros
numTerms = 135310
termsMatrix = np.zeros((numDocs,numTerms)) #需要跑一遍才能知道这个数字

#coo_matrix((3,4), dtype=np.int8)

#按照 field -> terms -> doc 的顺序遍历
for field in fields:
	if field == field_:
		termsEnum = MultiFields.getTerms(indexReader, field).iterator(None);
		#BytesRef bytesRef;
		#print help(BytesRefIterator.cast_) nothing!!!
		bytesIterator = BytesRefIterator.cast_(termsEnum)  
		#it is awesome, thanks to https://github.com/seecr/meresco-lucene/blob/master/meresco/lucene/index.py
		bytesRef = bytesIterator.next()
		term = convert(bytesRef)


		count = 0
		while bytesRef != None: #遍历 terms

			#----------------------1-------------------
			#统计各个域的 term 的 docFreq ，就是每个 term的出现频率
			docFreq = indexReader.docFreq(Term(field, bytesRef));
			# print convert(bytesRef) + " in " + str(docFreq) + " documents"
			idf_ = idf(docFreq,numDocs)


			#----------------------2--------------------
			#统计各个域的 term 在每个 doc中的频率，也就是 tf(t)

			#先全部append 0
			#termsMatrix = appendZero2Matrix(termsMatrix)
			if (termsEnum.seekExact(bytesRef, True)):
				docsEnum = termsEnum.docs(liveDocs, None)


				if docsEnum != None:
					doc = docsEnum.nextDoc() #int 就是doc的id
					while doc != DocIdSetIterator.NO_MORE_DOCS:
						tf_ = docsEnum.freq()
						# print convert(bytesRef) + " in doc " + str(doc) + ": " + str(docsEnum.freq())
						#termsMatrix[doc][count]=tf_*idf_ #这里是给含有这些词的doc进行了赋值,将append的0覆盖掉
						# termsMatrix[doc,count]=tf_*idf_ #这里是给含有这些词的doc进行了赋值,将append的0覆盖掉
						doc = docsEnum.nextDoc() #int


			try:
				bytesRef = bytesIterator.next()
			except StopIteration:
				print '完毕'
				print '一共有term：'+str(count)
				exit(0)
			print count 
			count = count + 1


formatWriteMatrix(termsMatrix,termsFile)



	# StopIteration:
	# Raised by an iterator‘s next() method to signal that there are no further values. 
	# This is derived from Exception rather than StandardError, 
	# since this is not considered an error in its normal application.





# 以下内容没用
# #统计各个域的 term 的 docFreq ，就是每个 term的出现频率
# for field in fields:
# 	if field == field_:
# 		termsEnum = MultiFields.getTerms(indexReader, field).iterator(None)
# 		bytesIterator = BytesRefIterator.cast_(termsEnum)  
# 		bytesRef = bytesIterator.next()
# 		while bytesRef != None:		
# 			docFreq = indexReader.docFreq(Term(field, bytesRef));
# 			print convert(bytesRef) + " in " + str(docFreq) + " documents"
# 			bytesRef = bytesIterator.next()






