# -*- coding: utf-8 -*-
from lxml import etree



html = open("test.html", 'r').read()
doc = etree.HTML(open("test.html", 'r').read())
i = 1
tags = doc.xpath("//div[@class='tags-body']/a["+str(i)+"]")
for t in tags:
	print t.text.encode("utf-8")


'''
tags = doc.xpath("//div[@class='tags-body']/a")
for t in tags:
    #print t.attrib.get('href')
    print t.text.encode("utf-8")
'''
'''
tags = doc.xpath("//div[@id='comments-section']/div[@class='mod-hd']/h2/span[@class='pl']/a")
for t in tags:
    print t.text.encode('utf-8')

'''
'''
from lxml import html
doc = html.fromstring(open("test.html", 'r').read())
tags = doc.xpath("//div[@class='tags-body']/a")
for t in tags:
    print t.attrib.get('href'), '----', t.text
'''



