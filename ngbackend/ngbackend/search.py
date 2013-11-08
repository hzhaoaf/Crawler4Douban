# -- coding:utf-8 --

from django.http import HttpResponse
from django.utils import simplejson

'''
Interface for querying from App
Use standard GET request
Return JSON
'''

def search(request):
    try:
        if request.method == 'GET':
	    # Extract the specified GET parameters
	    field = request.GET['field']
	    keyValue = request.GET['keyValue']

	    # Here goes the PyLucene routines, fetch results and construct json
	    # We can construct a standard Python Dictionary and then convert it to JSON
	    # Examples for returning JSON are demonstrated blow
	    retJson = {}
	    retJson['retCode'] = 0
	    retJson['field'] = field
	    retJson['keyValue'] = keyValue
	    retJson['rating'] = 10
	    retJson['team'] = 'NG'
	    retJson['manifesto'] = u'我们是最棒的！'

	    emdJson = {}
	    emdJson['code'] = 0
	    emdJson['message'] = 'Hello little Dict'
	    emdJson['goal'] = u'测试字典嵌套的JSON输出'

	    retJson['emdJson'] = emdJson

	    return HttpResponse(simplejson.dumps(retJson, ensure_ascii = False), content_type="application/json")
    except Exception, e:
	    errJson = {}
	    errJson['retCode'] = 1
	    errJson['message'] = 'Sorry, server Exception occurred!'
	    errJson['exceptionCode'] = e.args[0]
	    #errJson['exceptionMessage'] = e.args[1]
       	    return HttpResponse(simplejson.dumps(errJson, ensure_ascii = False), content_type="application/json")

