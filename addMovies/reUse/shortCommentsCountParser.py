#!/usr/bin/python
# -*- coding:utf-8 -*-


import os
import time
from lxml import etree

def parseShortCommentsCountFromHTML(detailsHTML):
    try:
        #doc = etree.HTML(open(filename, 'r').read().decode('utf-8'))
        doc = etree.HTML(detailsHTML)
        assessNum = doc.xpath("//div[@id='comments-section']/div[@class='mod-hd']/h2/span[@class='pl']/a")
        num = filter(str.isdigit, assessNum[0].text.encode('utf-8'))

        return num

    except Exception, e:
        print 'Error occured when parsing short comments count: %s' % (e)
