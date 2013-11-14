#!usr/bin/python
# -*- coding: utf-8 -*-

'''
    NG Team
'''

import httplib
import threading
import Queue
import time
import socket
import urllib2

#headers = {'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)',
#           'Connection': 'keep-alive'}

headers = {
           'Connection': 'keep-alive'}

#headers = {}

res_set = set()
res_list = []
id_queue = Queue.Queue(100)
lock = threading.Lock()
pro_start = time.time()
cnt = 0

errorListFilePath = './jsonData.error'
errorListFile = open(errorListFilePath)
lineList = errorListFile.readlines()

numberOfLinesToProcess = len(lineList)

print 'Will process ' + str(numberOfLinesToProcess) + ' ids...'

processedLines = 0

def check_movie_id():
    global headers, lock, id_queue, res_list, res_set, cnt
    global processedLines
    global numberOfLinesToProcess
    while True:
        try:
            movieid = id_queue.get()

            if movieid == None:
                 id_queue.task_done()
                 break
                 return
            else :
                #print 'Processing line ' + str(processedLines + 1) + ' & Checking ID:' + str(movieid)
                processedLines += 1

            reqUrl = 'http://www.douban.com' + '/subject/' + str(movieid)
            #print reqUrl
            response = urllib2.urlopen(reqUrl)
            #print "Response for %s is: " % (movieid)
            #print response.code
            #print response.info()
            #print response.geturl()
            location = response.geturl()
            response.close()

            if location.find('movie.douban.com') > 0:
                #print 'Found a movie subject for ' + str(movieid)
                # urllib2 will handle redirect for us:-)
                location = location.replace('http://movie.douban.com/subject/', '')
                location = location.replace('/', '')
                #print 'New ID: ' + location
                print location

                lock.acquire()

                if location not in res_set:
                    cnt += 1
                    res_list.append(location)
                    res_set.add(location)
                    if processedLines == numberOfLinesToProcess and False:
                        f = open('movie_ids_check_redirect', 'w+')
                        [f.write('%s\n' % r) for r in res_list]
                        f.close()
                        res_list = []
                        print 'Done writing IDs to file!'
                lock.release()
            id_queue.task_done()
            time.sleep(1.0)
        except urllib2.URLError as e:
            print "Exception: %s for %s" % (e, movieid)
        except urllib2.HTTPError as e:
            if e.code == 404:
                print '404:' + movieid
            elif e.code == 403:
                print '403:' + movieid
            elif e.code == 401:
                print '401:' + movieid
            else:
                print str(e.code) + location
        except KeyboardInterrupt:
            print "Ctrl+C pressed..."
            sys.exit()


all_threads = []
for i in range(50):
    new_thread = threading.Thread(target=check_movie_id)
    new_thread.setDaemon(True)
    new_thread.start()
    all_threads.append(new_thread)

for line in lineList:
    id_queue.put(line)

for j in range(50):
    id_queue.put(None)

id_queue.join()
for thread in all_threads:
    thread.join()

print 'All Done.'
