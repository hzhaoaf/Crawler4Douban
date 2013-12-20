#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding:utf-8

import json


# def set_charvalue():
#     width,height=600,600 
#     surface=cairo.ImageSurface(cairo.FORMAT_ARGB32,width,height) 
#     return surface

# if __name__ == '__main__':
#     '''
#     Function:使用pycha画各种图表
#     Input：NONE
#     Output: NONE
#     author: socrates
#     blog:http://blog.csdn.net/dyx1024
#     date:2012-02-28
#     '''
#     #数据来源
#     dataSet=( 
#              ('iphone',((0,1),(1,3),(2,2.5))), 
#              ('htc',((0,2),(1,4),(2,3))), 
#              ('hw',((0,5),(1,1,),(2,0.5))), 
#              ('zte',((0,3),(1,2,),(2,1.5))), 
#             ) 
    
#     #图像属性定义
#     options={ 
#                 'legend':{'hide':False}, 
#                 'title':'手机销售量分布图(by dyx1024)',
#                 'titleColor':'#0000ff',
#                 'titleFont':'字体',
#                 'background':{'chartColor': '#ffffff'}, 
#                 'axis':{'labelColor':'#ff0000'},
#             } 


# surface = set_charvalue()
    
# #根据需要调用不同函数画不同形状的图
# #draw_pie(surface, options, dataSet)
# draw_vertical_bar(surface, options, dataSet) 

def countList(alist):
	#uasge:返回一个tuple，包含一个起始位置和一个结束位置，能够涵盖大部分数目
	if len(alist) == 0:
		return 'get out of here!'

	percent = 0.9
	sum_ = sum(alist)
	print 'sum of all:'+ str(sum_)

	#这段用来找到开始点，以去除开始的那那些bullshit
	sum_useful = 20000
	sum_bullshit = sum_ - sum_useful #bullshit个数
	sum_tmp = 0 
	for i in range(len(alist)):
		sum_tmp = sum_tmp + alist[i]
		if sum_tmp>sum_bullshit:
			break;
	print 'bullshit num:'+str(sum_tmp)
	print 'usefull num:'+str(sum_-sum_tmp)
	start = i

	#在 useful 的中继续找能够满足 90%的
	sum_tmp = 0 
	for i in range(start,len(alist)):
		sum_tmp = sum_tmp + alist[i]
		if sum_tmp >= percent*sum_useful:
			break;
	if i == len(alist)-1:
		return "until the end"
	return (start,i+1)


with open('statistic.txt','r') as f:
	content = f.read()
statisticDict = json.loads(content)     
for eachKey in statisticDict.keys():
	print eachKey
	print countList(statisticDict[eachKey])
	print 
