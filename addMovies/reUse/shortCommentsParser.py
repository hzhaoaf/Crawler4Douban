#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import time
from lxml import etree


def parseShortCommentsFromHTML(eid, num, htmls_dir):
    try:
        myString = '{'

        shortCommentsCount = 0

        if num > 1000:
            end = 50
        else:
            end = num / 20 + 1

        for i in range(end):
            start = i*20
            inFilePath = htmls_dir + '/' + str(start) + '.html'
            doc = etree.HTML(open(inFilePath, 'r').read().decode("utf-8"))
            nameList = doc.xpath("//div[@class='comment']/h3/span[@class='comment-info']/a")
            listLength =  len(nameList)
            #print listLength
            shortCommentsCount += listLength

            for i in range(listLength):
                try:
                    name = doc.xpath("//div[@class='comment']/h3/span[@class='comment-info']/a")[i].text.encode("utf-8")
                    name = name.replace('"','')
                    name = name.replace('\\','')
                except Exception, e:
                    name = ''
                try:
                    p0 = doc.xpath("//div[@class='comment']/p")[i].text.strip().encode("utf-8")
                    p1 = ''
                    for line in p0:
                        p1 += line.rstrip()
                    p1 = p1.replace('"','')
                    p = p1.replace('\\','')
                except Exception, e:
                    p = ''
                try:
                    date = doc.xpath("//div[@class='comment']/h3/span[@class='comment-info']/span[2]")[i].text.strip()
                except Exception, e:
                    date = ''
                try:
                    votenum = doc.xpath("//span[@class='votes pr5']")[i].text
                except Exception, e:
                    votenum = ''
                try:
                    star = doc.xpath("//h3/span[@class='comment-info']/span[@title]")[i].attrib.get("title").encode("utf-8")
                except Exception, e:
                    star = ''
                myString += '\n"' + name + '":{"p":"' + p + '","date":"' + date + '","votenum":"' + votenum + '","star":"' + star + '"},'
                #print star.attrib.get("title").encode("utf-8")
                #print name
                #print p
                #print date
                #print votenum

        myString = myString[:-1]
        myString += '}'

        return myString, shortCommentsCount

    except Exception, e:
        print 'Error occured when parsing short comments for ID %s: %s' % (eid, e)

