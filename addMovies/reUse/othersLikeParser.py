#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
from lxml import etree

def parseOthersLikeFromHTML(detailsHTML):
    try:
        #doc = etree.HTML(open(filename, 'r').read().decode('utf-8'))
        doc = etree.HTML(detailsHTML)
        myString='{'
        href = doc.xpath("//div[@class='recommendations-bd']/dl/dd/a")
        myString += '"'
        if href:
            for i in href:
                id = i.attrib.get('href')[32:-19]
                myString += (id +'":"')
                myString += (i.text.encode("utf-8")+'","')

        if myString[-2:] == ',"':
            myString = myString[:-2]
        else:
            myString = myString[:-1]
        myString += '}'

        return myString

    except Exception as e:
        print "Error occured when parsing others like: %s" % (e)

