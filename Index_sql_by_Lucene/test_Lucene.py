#!usr\bin\python
#-*- coding:UTF-8 -*-
import time
import urllib2
import urllib
from urllib2 import URLError,HTTPError
import json

#user agent 
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0')]
urllib2.install_opener(opener)

#base_url+'?'+command_str+'&'+num_str
base_url = 'http://192.158.31.250/search'
command_str = ''
num_str = 'start=0&count=5'
num_str_quoted = urllib.quote(num_str)



testCommandList = [
'command=title:狄仁杰 casts:赵又廷',
\
'command=title:+狄仁杰 casts:+赵又廷',
'command=+title:狄仁杰 +casts:赵又廷',
'command=title:+狄仁杰 +casts:赵又廷',
\
'command=title:+狄仁杰 casts:-赵又廷',
'command=+title:狄仁杰 -casts:赵又廷',
'command=title:+狄仁杰 -casts:赵又廷',
'command=+title:狄仁杰 casts:-赵又廷',
\
'command=title:-狄仁杰 casts:+赵又廷',
'command=-title:狄仁杰 +casts:赵又廷',
'command=title:-狄仁杰 +casts:赵又廷',
'command=-title:狄仁杰 casts:+赵又廷',
\
'command=title:+狄仁杰 +龙王',
'command=title:狄仁杰 AND 龙王',
'command=title:狄仁杰 OR 龙王',
'command=title:狄仁杰  -龙王',
'command=title:狄仁杰  NOT 龙王',
\
'command=title:狄仁杰 AND casts:赵又廷' ,
'command=+title:狄仁杰 AND +casts:赵又廷' ,
'command=title:狄仁杰 AND casts:-赵又廷',
'command=title:狄仁杰 AND casts:NOT 赵又廷',
'command=title:狄仁杰 AND -casts:赵又廷',
'command=title:狄仁杰 AND NOT casts:赵又廷',
\
'command=title:狄仁杰 OR casts:赵又廷',
'command=title:狄仁杰 OR +casts:赵又廷',
'command=title:狄仁杰 OR casts:-赵又廷',
'command=title:狄仁杰 OR casts:NOT 赵又廷',
'command=title:狄仁杰 OR NOT casts:赵又廷',
\
\
\
'command=title:狄仁杰 summary:赵又廷',
\
'command=title:+狄仁杰 summary:+赵又廷',
'command=+title:狄仁杰 +summary:赵又廷',
'command=title:+狄仁杰 +summary:赵又廷',
\
'command=title:+狄仁杰 summary:-赵又廷',
'command=+title:狄仁杰 -summary:赵又廷',
'command=title:+狄仁杰 -summary:赵又廷',
'command=+title:狄仁杰 summary:-赵又廷',
\
'command=title:-狄仁杰 summary:+赵又廷',
'command=-title:狄仁杰 +summary:赵又廷',
'command=title:-狄仁杰 +summary:赵又廷',
'command=-title:狄仁杰 summary:+赵又廷',
\
'command=title:狄仁杰 AND summary:赵又廷' ,
'command=+title:狄仁杰 AND +summary:赵又廷' ,
'command=title:狄仁杰 AND summary:-赵又廷',
'command=title:狄仁杰 AND summary:NOT 赵又廷',
'command=title:狄仁杰 AND -summary:赵又廷',
'command=title:狄仁杰 AND NOT summary:赵又廷',
\
'command=title:狄仁杰 OR summary:赵又廷',
'command=title:狄仁杰 OR +summary:赵又廷',
'command=title:狄仁杰 OR summary:-赵又廷',
'command=title:狄仁杰 OR summary:NOT 赵又廷',
'command=title:狄仁杰 OR NOT summary:赵又廷',
]

print 'here we go!'

with open('./testLog.md','w') as logfile:
	for command_str in testCommandList:

		#quote the value of the key 'command'
		command_arr = command_str.split('=')
		command_str_quoted = command_arr[0]+'='+urllib.quote(command_arr[1])
		
		url = base_url+'?'+command_str_quoted+'&'+num_str
		time.sleep(1)

		print url
		try:
			rspn = urllib2.urlopen(url)
			rspn_content = rspn.read()
			jsonObj = json.loads(rspn_content)
			titles_Str = '\t'
			for subj in jsonObj['subjects']:
				title = subj['title'].encode('UTF-8') #这里得到的居然是unicode编码的!!!!!!!!!1
				titles_Str = titles_Str + title + '\n\t'
			print titles_Str
			logfile.write('####'+command_str+'####'+'\n'+'Content:'+'\n\n'+titles_Str+'\n\n'+'---'+'\n')
		except URLError,e:
			logfile.write('####'+command_str+'####'+'\n\t'+'URLError:'+str(e.code)+'\n\n'+'---'+'\n')
		except HTTPError,e:
			logfile.write('####'+command_str+'####'+'\n\t'+'HTTP Error:'+e.reason +'\n\n'+'---'+'\n')

	logfile.close()





    

