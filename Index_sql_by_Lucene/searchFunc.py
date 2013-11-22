#!/usr/bin/env python
# -*- coding: utf-8 -*-

#usage:for test 

import SearchMysql_v2

SearchMysql_v0.initJvm()
searcher,analyzer = SearchMysql_v0.config()
ansList = SearchMysql_v0.run('狄仁杰 龙王',searcher,analyzer)

print ansList[0]
