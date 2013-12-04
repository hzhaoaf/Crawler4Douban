#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Pull Douban Movie Item according to the subject id
'''

'''
#apikey=032990ce370112ae097cb26aa503380a
#http://api.douban.com/v2/movie/subject/4807924/photos

#id
#http://api.douban.com/v2/movie/subject/4807924?apikey=032990ce370112ae097cb26aa503380a
#long comments
#http://api.douban.com/v2/movie/subject/4807924/reviews?apikey=032990ce370112ae097cb26aa503380a
#comments
#http://api.douban.com/v2/movie/subject/4807924/comments?apikey=032990ce370112ae097cb26aa503380a
#celebrity
#http://api.douban.com/v2/movie/celebrity/1054395?apikey=032990ce370112ae097cb26aa503380a
#nowplaying
#http://api.douban.com/v2/movie/nowplaying
'''

#README
#1.修改step 和 线程 sleep中的时间调节下载速度
#2.每次使用新的avalibleID.txt时 除了要修改path 还要修改record.txt


import time
import urllib,urllib.request
from urllib.error import URLError, HTTPError
import os
import string
import datetime
import socket
import threading
import os

#设置超时，不知道有没有用
timeout = 60
socket.setdefaulttimeout(timeout)

#api信息
basicUrl = 'http://api.douban.com/v2/movie/subject/'
key = '032990ce370112ae097cb26aa503380a'

#计数器什么的
eid = ''
success_counter = 0
NOTFOUNDNUM= 0

#存储路径
main_path = './newJsonData.1'
record_path = 'record.txt'

mid_avalible_txt = 'failIdList.1'
midFile = open(mid_avalible_txt)
lineList = midFile.readlines()

#打开记录文件，继续上次的下载
with open(record_path) as recordFile:
    line = recordFile.readline()
    print('asdas'+line)
    idx_last = int(line)
    recordFile.close()

#测试用，id=5996801的是《狄仁杰之神都龙王》
step = 100

#mid_last =     5996801
the_file_end = len(lineList)
the_vary_end = 9999999

print(the_file_end)


#下载函数
def download_item(loc_str,err_loc_str,eid):
    global NOTFOUNDNUM
    try:
        req = urllib.request.Request(basicUrl+eid)
        response = urllib.request.urlopen(req)
        jsonData = response.read()

        # quote
        #jsonData_ = urllib.parse.quote(jsonData)

        print('success:'+eid)

        #保存json
        with open(loc_str, "wb") as json:
            json.write(jsonData)

    except (URLError,HTTPError) as e:#有问题？？
        print('Error for ID: '+str(eid))
        if hasattr(e, 'code'):
            print('Error code: ', e.code)
        if hasattr(e, 'reason'):
            print('Error reason: ', e.reason)

        with open(err_loc_str, "a") as record_file:
            print('Write Error ID to record file...')
            record_file.write(str(eid)+'\n')
        if e.code == 404:
            NOTFOUNDNUM = NOTFOUNDNUM + 1
            print('Not found number now: ' + str(NOTFOUNDNUM))
    except socket.timeout as e:
        print('Socket timeout for ID: ' + str(eid))
    else:
        pass





while idx_last < the_file_end:
    # 存储线程,每次step个
    task_threads =[]
    nextStop = min(the_file_end, idx_last+step)
    for idx in range(idx_last, nextStop):
        mid_str = str(lineList[idx])

        print('***' + str(idx))

        eid = mid_str[0:-1] # delete \n
        print(eid)

        loc_str = main_path + '/' + eid + '.json'
        err_loc_str = main_path + '/' + 'errorList.txt'
        t = threading.Thread(target = download_item, args = (loc_str, err_loc_str, eid))
        task_threads.append(t)


    # 执行线程
    numOfThreads = len(task_threads)
    i = 0
    while i < numOfThreads:
        task = task_threads[i]
        time.sleep(1.3)
        task.start()
        i = i + 1


    for task in task_threads:
        # task线程合并到主线程中，主线程停止执行过程，转而执行task线程，直到task执行完毕后继续
        task.join()


    idx_last = nextStop
    # 保存当前进度到record
    file_loc_str = record_path
    with open(file_loc_str, "wb") as record_file:
        record_file.write(bytes(str(idx_last).encode('utf-8')))

    print('搞定100个！')



print("已经完成所有任务")







