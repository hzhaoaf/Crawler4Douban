# -*- coding: utf-8 -*-

import os
import time
from lxml import etree

def parseUserTagsFromHTML(detailsHTML):
    try:
        #doc = etree.HTML(open(filename, 'r').read().decode('utf-8'))
        doc = etree.HTML(detailsHTML)
        i = 1
        tags = doc.xpath("//div[@class='tags-body']/a")
        myString='{"'
        for t in tags:
            tag_name = doc.xpath("//div[@class='tags-body']/a["+str(i)+"]")
            for t in tag_name:
                myString += t.text.encode("utf-8")
            tag_span = doc.xpath("//div[@class='tags-body']/a["+str(i)+"]/span")
            for t in tag_span:
                myString += '":"' + t.text.strip("()") + '","'
            i += 1
        if myString[-2:]==',"':
            myString = myString[:-2]
        else:
            myString = myString[:-1]
        myString += '}'
        return myString
    except Exception as e:
        print "Error occured when parsing user tags: %s" % (e)


