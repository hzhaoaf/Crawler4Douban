# -- coding:utf-8 --
from django.http import HttpResponse
from django.utils import simplejson

def hello(request):
	return HttpResponse("Hello, NG Guy! Our Django works!")

def jsonTest(request):
	if request.method == 'GET':
	    #retString = 'You are sending a GET request.'
	    #retString += 'Request parmas:' + request.GET.get('test','')

	    field = request.GET.get('field','')
	    keyValue = request.GET.get('keyValue','')

	    retJson = {}
	    retJson['field'] = field
	    retJson['keyValue'] = keyValue

	#return HttpResponse("Test json request params are: " + "field = " + field + " & keyValue = " + keyValue)
	return HttpResponse(simplejson.dumps(retJson, ensure_ascii = False), content_type="application/json")

