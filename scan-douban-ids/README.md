Scan IDs
========

We have two approaches for scanning ids:

### Number 1
httplib utilizing HTTPConnection using GET request, however http redirect like 301 and 302 must be handled by us

### Number 2
urllib2 utilizing openurl method, automatically handle redirect for us, but easier got forbidden maybe:-(

**Known Issues:**

The urllib2 approach dosen't support `log files` now and you may invoke the script by issuing:

    nohup python scan_douban_ids_with_urllib2.py

The result will be reside in `nohup.out` and post-process it with `find grep wc less awk sed` stuff as you like.
