#coding=utf8
'''
    这个脚本从crawler抓取的网页中提取需要的获奖信息，保存到获奖文件中
    保存的单位为三元组：id，电影名，获奖信息（|分开）
'''
import os
import json
import lxml
from lxml import etree


def extract_award_info(html_file):
    '''
        豆瓣网页上获奖的展现方式：
        奖项级别（年份）
        具体获奖名称 对应的人员
        一个奖项可能对应多个获奖名称
        一个获奖名称可能对应多个人员
    '''
    doc = etree.HTML(open(html_file, 'r').read())
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



def extract_awards_by_html():
    cnt = 0
    for num in range(1, 5):
        saved_file = 'parts%s_awards.txt' % (str(num))
        fw = open(saved_file, 'w+')
        round_num = 0
        htmls_dir = 'htmls/parts%s' % (str(num))
        htmls = os.listdir(htmls_dir)
        lines = []
        for html_file in htmls:
            try:
                round_num += 1
                cnt += 1
                subject_id = html_file.replace('.html', '')
                awards_info = extract_award_info('%s/%s' % (htmls_dir, html_file))
                if awards_info.get('award_items'):
                    awards_info['subject_id'] = subject_id
                    lines.append(json.dumps(awards_info, ensure_ascii=False))
                if round_num % 1000 == 0:
                    print 'finish extract %s(%s): %s/%s' % (html_file, saved_file, round_num, cnt)
            except Exception as e:
                print 'error occured: %s--file %s' % (e, html_file)
        res = '%s' % '\n'.join(lines)
        fw.write(res.encode('utf8'))
        fw.close()
        print 'finish one parts saved fils: %s' % (saved_file)


if __name__ == '__main__':
    #print extract_award_info('test.html')
    extract_awards_by_html()
