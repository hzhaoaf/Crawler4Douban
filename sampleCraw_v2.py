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
#proxy_support = urllib2.ProxyHandler({'http':'http://127.0.0:8087'})
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)


fp=open("./id_test.txt", "r")
cout = 0

for eachline in fp:
    eid = eachline.strip('\n')
    url = 'http://movie.douban.com/subject/'+eid
    print url
    try:
        data = urllib2.urlopen(url).read()
    except Exception, e:
        data = 'no data'
        print e.code
        if e.code == 403:
            break
    path = ''.join(['e:\\detailHtml_2W\\',eid,'.html'])
    writeTo(path,data,'w')
    time.sleep(3)
    cout+=1
    print cout
    #if cout%100==0:
        #print cout
    if cout%5 ==0:
        time.sleep(3)
        print 'restart'
        fp.close
        fp=open("./id_test.txt", "r")
        a = fp.read()
        fp.close
        b = a[40:]
        fp=open("./id_test.txt", "w")
        fp.write(b)
        fp.close
        print 'rewrite txt,delete 40bit'
        restart_program()


