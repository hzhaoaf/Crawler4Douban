#!usr/bin/python
# -*- coding: utf-8 -*-

'''
    NG Team
'''

import httplib
#import MySQLdb as mdb
import threading
import Queue
import time
import socket

#socket.setdefaulttimeout(60)

headers = {'Connection': 'keep-alive'}

start_id = 1
end_id   = 30000000

print 'Will check ID from ' + str(start_id) + ' to ' + str(end_id)


#dbconn = mdb.Connection(host = '127.0.0.1', user = 'user', passwd = '******', db = 'dbname', charset='utf8')
#cursor = dbconn.cursor()
res_set = set()
res_list = []
id_queue = Queue.Queue(100)
lock = threading.Lock()
pro_start = time.time()
cnt = 0

def check_album_id():
    global headers, dbconn, cursor, lock, id_queue, res_list, res_set, cnt
    while True:
        try:
            albumid = id_queue.get()
            print 'Checking ID:' + str(albumid)

            if albumid == None:
                 id_queue.task_done()
                 break
                 return

            if albumid % 100000 == 0:
                 print 'test album id %s crawled %s movies cost %.2fmin' % (albumid, cnt, (time.time() - pro_start) / 60.0)

            conn = httplib.HTTPConnection("www.douban.com")
            conn.request(method='GET', url='/subject/' + str(albumid) + '/', headers=headers)
            response = conn.getresponse()
            location = response.getheader('location', '')
            if location.find('movie.douban.com') > 0:
                print 'ID: ' + str(albumid)
                location = location.replace('http://movie.douban.com/subject/', '')
                location = location.replace('/', '')
                lock.acquire()
                #cursor.execute("select * from album where album_url = %s", location)
                #if cursor.fetchone() == None:
                #    cursor.execute('INSERT INTO album(album_url) values (%s)', location)
                #    dbconn.commit()
                if location not in res_set:
                    cnt += 1
                    res_list.append(location)
                    res_set.add(location)
                    if len(res_list) == 1000 or albumid == end_id:
                        f = open('movie_ids-%s_%s' % (str(cnt - 999), str(cnt)), 'w+')
                        [f.write('%s\n' % r) for r in res_list]
                        f.close()
                        res_list = []
                        print 'get 1000 movie total %s test id is %s' %(str(cnt), str(albumid))
                lock.release()
            conn.close()
            id_queue.task_done()
            time.sleep(0.01)
        except (httplib.HTTPException, socket.error) as e:
            print 'Exception occured!'
	    print "Error: %s" % e
        except KeyboardInterrupt:
	    print "Ctrl+C pressed..."
	    sys.exit()


all_threads = []
for i in range(50):
    new_thread = threading.Thread(target=check_album_id)
    new_thread.setDaemon(True)
    new_thread.start()
    all_threads.append(new_thread)

for j in range(start_id, end_id):
    id_queue.put(j)

for j in range(50):
    id_queue.put(None)

id_queue.join()
for thread in all_threads:
    thread.join()

#dbconn.close()
print 'All Done.'