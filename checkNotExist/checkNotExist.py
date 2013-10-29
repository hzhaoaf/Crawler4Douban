import os


htmls_dir = 'htmls-2000001--2999989';
if not os.path.isdir(htmls_dir):
	os.mkdir(htmls_dir)

id_file = 'test'

lines = open(id_file, "r").readlines()
#print str(len(lines)) + ' html items remaining...'
oldRemainingLines = lines

cout = 0
iCout = 0

for line in lines:
	eid = line.strip()
	path = '%s/%s.html' % (htmls_dir, eid)
	# Check if the file already exists
	if os.path.exists(path):
		cout+=1
		#print eid
		#print '%s html exists and will pass' %(eid)
	else:
		iCout+=1
		print eid

print 'there are %s files exist and %s files not exist' % (cout , iCout)
	