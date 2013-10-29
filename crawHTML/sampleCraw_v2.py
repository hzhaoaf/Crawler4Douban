
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

def main():
    cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)


    count = 0
    htmls_dir = 'html';
    if not os.path.isdir(htmls_dir):
        os.mkdir(htmls_dir)

    id_file = 'hello'

    lines = open(id_file, "r").readlines()
    print str(len(lines)) + ' html items remaining...'
    oldRemainingLines = lines

    pro_start_time = time.time()
    start_time = time.time()
    end_time = time.time()
    for line in lines:
        eid = line.strip()
        path = '%s/%s.html' % (htmls_dir, eid)
        # Check if the file already exists
        if os.path.exists(path):
            print '%s html exists and will pass' %(eid)
        else:
            url = 'http://movie.douban.com/subject/%s' % eid
            if count % 5 == 0:
                end_time = time.time()
                #print 'crawl %s id %s, this round cost %.2fs, total cost %.2fmin' % (count, eid, end_time - start_time, (time.time() - pro_start_time) / 60.0)
                start_time = time.time()
            try:
                data = urllib2.urlopen(url).read()
            except Exception, e:
                data = 'no data'
                #print 'error occured %s id %s' % (e.code, eid)
                #if e.code == 403:
                    #break
            writeTo(path, data, 'w+')
            print 'write %s html OK' % (eid)
            time.sleep(3)
        count += 1
        if count % 200 == 0:
            break;

    #if len(lines) < 10:
    #   print 'All html items crawled.'

    if True:
       #print 'count = %s, lines = %s' % (count, len(lines))
       time.sleep(1)
       #print 'crawled %s ids, restart, programs have running %.2f min' % (count, (time.time() - pro_start_time) / 60.0)
       lines = open(id_file, "r").readlines()
       lines = lines[count:]
       f = open(id_file, "w+")
       [f.write('%s' % l) for l in lines]
       f.close()
       print 'rewrite txt,delete %s' % (count)
       #restart_program()
       #break

    if len(oldRemainingLines) < 200:
        print 'All Done, Program will exit!'
        return 0,count
    else:
        print 'Processed %s html items...' % (count)
        return 1,count



