import sampleCraw_v2
import time

start_time = time.time()


cout = 0

while 1:
    sampleCraw_v2.main()
    cout+=10
    print 'crawl %s, total cost %.2fmin' % (cout, (time.time() - start_time) / 60.0)
    #print cout

