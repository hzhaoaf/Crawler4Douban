#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
    这个脚本用来从全部的电影id中获取其获奖页面,
    对于一个id，访问http://movie.douban.com/subject/1298184/awards/
'''

import urllib2, random
import os, time
import sys

user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
        (KHTML, like Gecko) Element Browser 5.0', \
        'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', \
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
        'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
        'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
        Version/6.0 Mobile/10A5355d Safari/8536.25', \
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/28.0.1468.0 Safari/537.36', \
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']

timeout = 60
awardsURL = 'http://movie.douban.com/subject/'

def crawlAwardslHTMLPage(subjectID, use_proxy=False):
    try:
        url = awardsURL + subjectID + '/awards/'
        index = random.randint(0, 9)
        if use_proxy:
            proxy_handler = urllib2.ProxyHandler({"http":'127.0.0.1:8087', "https":'127.0.0.1:8087'})
            opener = urllib2.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', user_agents[index])]
            urllib2.install_opener(opener)

        #print 'url is %s --%s' % (url, 'use proxy' if use_proxy else 'direct download')
        request = urllib2.Request(url)
        user_agent = user_agents[index]
        request.add_header('User-agent', user_agent)

        response = urllib2.urlopen(request, timeout=timeout)
        code = response.getcode()
        if code not in (200, 201, 202, 302, 304):
            return ''

        html = response.read()
        return html

    except Exception as e:
        print 'Exception occured when crawling awards info for ID %s: %s' % (subjectID, e)
        return ''


