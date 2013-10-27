from lxml import etree

doc = etree.HTML(open("test.html", 'r').read())
tags = doc.xpath("//div[@class='tags-body']/a")
for t in tags:
    print t.attrib.get('href'), '----', t.text

from lxml import html
doc = html.fromstring(open("test.html", 'r').read())
tags = doc.xpath("//div[@class='tags-body']/a")
for t in tags:
    print t.attrib.get('href'), '----', t.text




