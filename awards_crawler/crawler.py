#coding=utf8
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

timeout = 10

def crawl(url, use_proxy=False):
    index = random.randint(0, 9)
    if use_proxy:
        proxy_handler = urllib2.ProxyHandler({"http":'127.0.0.1:8087', "https":'127.0.0.1:8087'})
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', user_agents[index])]
        urllib2.install_opener(opener)

    print 'url is %s --%s' % (url, 'use proxy' if use_proxy else 'direct download')
    request = urllib2.Request(url)
    user_agent = user_agents[index]
    request.add_header('User-agent', user_agent)
    try:
        response = urllib2.urlopen(request, timeout=timeout)
        code = response.getcode()
        if code not in (200, 201, 202, 302, 304):
            return '', False, code

        html = response.read()
        return html, True, code
    except Exception as e:
        return '', False, None

save_dir = 'htmls'
if not os.path.isdir(save_dir):
    os.mkdir(save_dir)

def save_error_id(id_):
    error_filename = 'error_ids.txt'
    error_lines = open(error_filename, 'r').readlines()
    error_ids = set([l.strip() for l in error_lines])
    error_ids.add(id_)
    fw = open(error_filename, 'w+')
    fw.write('%s' % '\n'.join(list(error_ids)))
    fw.close()


ids_filename = 'remaining_ids.txt'
def crawl_by_id():
    pro_start = time.time()
    lines = open(ids_filename, 'r').readlines()
    ids = [l.strip() for l in lines if l.strip()]
    try:
        count = len(ids)
        step = count / 4 + 1
        total = 0
        success_num = 0
        failed_num = 0
        for i in range(count):
            '''
                需要整体try住，一旦发生异常，保存当前的ids到文件，下次直接对这个文件进行循环爬取
            '''
            total += 1
            id_ = ids.pop(0)
            url = 'http://movie.douban.com/subject/%s/awards/' % id_
            dir_ = '%s/parts%s' % (save_dir, str((i / step + 1)))
            wfilename = '%s/%s.html' % (dir_, id_)
            try:
                start = time.time()
                if not os.path.isdir(dir_):
                    os.mkdir(dir_)
                #import pdb;pdb.set_trace()
                html, is_successed, code = crawl(url)
                end = time.time()
                total_cost = (end - pro_start) / 60.0
                if is_successed:
                    fw = open(wfilename, 'w+')

                    success_num += 1
                    fw.write('%s\n' % html)
                    fw.close()
                    print 'successed, id=%s(left %s), file saved in %s, cost %.2fs(%.2fmin)--%s/%s\n' % (id_, len(ids), wfilename, end - start, total_cost, success_num, total)
                else:
                    error_line = '%s/%s\t%s' % (save_dir, str(i+1), url)
                    save_error_id(id_)
                    failed_num += 0
                    print 'failed, id=%s(left %s), file saved in %s, cost %.2fs(%.2fmin)--%s/%s\n' % (id_, len(ids), wfilename, end - start, total_cost, success_num, total)
                time.sleep(1)
            except Exception as e:
                print 'error occured: %s, id=%s' % (e, id_)
                save_error_id(id_)
                failed_num += 0
                time.sleep(2)
                continue
    except KeyboardInterrupt:
        f = open('remaining_ids.txt', 'w+')
        f.write('%s' % '\n'.join(ids))
        f.close()
        print 'You press the Ctrl+C, saved the remaining %s ids to crawl in remaining_ids.txt, exit!!' % str(len(ids))
        sys.exit()

if __name__ == '__main__':
    crawl_by_id()
