#!/usr/bin/python
# -*- coding:utf-8 -*-

def writeTo(path, data, mode):
    try:
        f = file(path, mode)
        f.write(data)
        print 'New short comments written to %s.' % (path)
        f.close()
    except Exception as e:
        print 'Error occured when writing to file %s' % (path)
