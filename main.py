#!/usr/bin/python
# -*- coding: utf-8 -*-

import sampleCraw_v2
import time

start_time = time.time()


count = 0

while 1:
    returnCode,crawlCount = sampleCraw_v2.main()
    print 'returnCode is ' + str(returnCode)

    count += crawlCount
    print 'crawl %s, total cost %.2fmin' % (count, (time.time() - start_time) / 60.0)
    if returnCode == 0:
        break;

print 'GoodBye'

