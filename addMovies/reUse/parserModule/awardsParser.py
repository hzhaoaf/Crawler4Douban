#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
    这个脚本从crawler抓取的网页中提取需要的获奖信息
'''

import os
import json
import lxml
from lxml import etree


def parseAwardsInfoFromHTML(awards_html):
    '''
        豆瓣网页上获奖的展现方式：
        奖项级别（年份）
        具体获奖名称 对应的人员
        一个奖项可能对应多个获奖名称
        一个获奖名称可能对应多个人员
    '''
    try:
        #doc = etree.HTML(open(html_file, 'r').read())
        doc = etree.HTML(awards_html)
        movie_name = doc.xpath('//div[@id="content"]/h1/text()')[0].replace(u'获奖情况', u'')
        awards = doc.xpath('//div[@class="awards"]')
        awards_info = {}
        awards_info['movie_name'] = movie_name
        for award in awards:
            titles = award.xpath('.//div[@class="hd"]/h2') or ['',]
            title = titles[0].text.replace(u'\xa0', u'')

            years = award.xpath('.//div[@class="hd"]/h2/span[@class="year"]') or ['',]
            year = years[0].text.replace(u'\xa0', u'')
            info = {}
            info['title'] = title
            info['year'] = year.replace('(', '').replace(')', '')

            award_details = award.xpath('.//ul[@class="award"]')
            for detail in award_details:
                award_names = detail.xpath('./li[1]') or ['', ]
                award_name = award_names[0].text.replace(u'\xa0', u'')
                persons = detail.xpath('./li[position()>1]/a')
                persons = '|'.join(p.text.replace(u'\xa0', u'') for p in persons)
                info.setdefault('award_detail', []).append('%s:%s' % (award_name, persons))
            awards_info.setdefault('award_items', []).append(info)

        return awards_info

    except Exception as e:
        print 'Error occured when parsing awards info: %s' % (e)
