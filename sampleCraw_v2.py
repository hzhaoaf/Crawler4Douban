import time
import urllib2
import socket
import cookielib
import sys
import os

socket.setdefaulttimeout(100)


def writeTo(path,data,mode):
    f = file(path,mode)
    f.write(data)
    f.close()

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)


cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)


count = 0
htmls_dir = 'htmls-5057131-5080414';
if not os.path.isdir(htmls_dir):
    os.mkdir(htmls_dir)

id_file = 'movieId-5057131--5080414'

lines = open(id_file, "r").readlines()

pro_start_time = time.time()
start_time = time.time()
end_time = time.time()
for line in lines:
    eid = line.strip()
    url = 'http://movie.douban.com/subject/%s' % eid
    if count % 10 == 0:
        end_time = time.time()
        print 'crawl %s id %s, this round cost %.2fs, total cost %.2fmin' % (count, eid, end_time - start_time, (time.time() - pro_start_time) / 60.0)
        start_time = time.time()
    try:
        data = urllib2.urlopen(url).read()
    except Exception, e:
        data = 'no data'
        print 'error occured %s id %s' % (e.code, eid)
        if e.code == 403:
            break
    path = '%s/%s.html' % (htmls_dir, eid)
    writeTo(path, data, 'w+')
    time.sleep(3)
    count+=1
    if count % 100 == 0:
        time.sleep(3)
        print 'crawled %s ids, restart, programs have running %.2f min' % (count, (time.time() - pro_start_time) / 60.0)
        lines = open(id_file, "r").readlines()
        lines = lines[count:]
        f = open(id_file, "w+")
        [f.write('%s' % l) for l in lines]
        f.close()
        print 'rewrite txt,delete 100'
        restart_program()


