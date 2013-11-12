# -- coding:utf-8 --
#usage: process the get request of the app
from django.http import HttpResponse
from django.utils import simplejson

from django.utils.http import urlquote
import urllib

import SearchMysql_v0

'''
Interface for querying from App
Use standard GET request
Return JSON
'''

SearchMysql_v0.initJvm()

def search(request):
    #try:
    if request.method == 'GET':
        # Extract the specified GET parameters
        #command = urlquote(request.GET['command']).decode('utf8')
        command = urllib.unquote(request.GET['command'])
        start = int(urllib.unquote(request.GET['start']))#start 规定从0开始
        count = int(urllib.unquote(request.GET['count']))
        #count = urllib.unquote(request.GET['count'])
        #command = command.encode('utf8')


        #command_unicoded = unicode(command, 'utf-8') #test the encoding 

        #command = request.GET['command']
        #keyValue = request.GET['keyValue']

        # Here goes the PyLucene routines, fetch results and construct json
        # We can construct a standard Python Dictionary and then convert it to JSON
        # Examples for returning JSON are demonstrated blow

        

        searcher,analyzer = SearchMysql_v0.config()
        retList = SearchMysql_v0.run(command,searcher,analyzer)

        ansCount = len(retList)

        retObj = {}

        if start+count < ansCount:
            retObj['count'] = count
            retObj['start'] = start
            retObj['total'] = ansCount
            retObj['subjects'] = retList[start:start+count]
        elif start < ansCount:
            retObj['count'] = ansCount-start
            retObj['start'] = start
            retObj['total'] = ansCount
            retObj['subjects'] = retList[start:ansCount]
        else:
            retObj['count'] = '老纪你看清楚，总共才'+str(ansCount)+'个！'
        
        retJson = retObj
        #retJson = simplejson.dumps(retObj,ensure_ascii=False)  #all is unicode withoout ensure...
        #retJson = eval(retJson) #将原本是字符串的json的引号去掉 比如'[1,2,3]'-->[1,2,3],将字符串变成变量
        #retJson = retList[0:5] #right encode utf8 list

        '''
        emdJson = {}
        emdJson['code'] = 0
        emdJson['message'] = 'Hello little Dict'
        emdJson['goal'] = u'测试字典嵌套的JSON输出'

        retJson['emdJson'] = emdJson
        '''

        return HttpResponse(simplejson.dumps(retJson, ensure_ascii = False), content_type="application/json")
    '''
    except Exception, e:
            errJson = {}
            errJson['retCode'] = 1
            errJson['message'] = 'Sorry, server Exception occurred!'
            errJson['exceptionCode'] = e.args[0]
            #errJson['exceptionMessage'] = e.args[1]
            return HttpResponse(simplejson.dumps(errJson, ensure_ascii = False), content_type="application/json")
    '''