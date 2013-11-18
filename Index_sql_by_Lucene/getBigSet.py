import MySQLdb as mdb
from sqlConstants.py import *

#usage: this script is used for getting the set of some classes or properties of the movies

con = mdb.connect('localhost','root','testgce','moviedata')

with con:
        # Careful with codecs
        con.set_character_set('utf8')

        cur = con.cursor()
        # Aagin the codecs
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')
        
        cur.execute("SELECT * FROM movie_items")

        allSetsDict = {}

        for eachFieldName in fields_name_list:
        	allSetsDict['eachFieldName'] = set()

        numrows = int(cur.rowcount)
        print 'numrows:',numrows
        for i in range(numrows):
            row = cur.fetchone()
            allSetsDict[fields_name_list[YEAR])     ].add(row[REAR])
            allSetsDict[fields_name_list[SUBJECT_ID]].add(row[SUBJECT_ID])
            
            allSetsDict[fields_name_list[GENRES]    ].union(set(row[GENRES   ].split(split_sym))
            allSetsDict[fields_name_list[CASTS]     ].union(set(row[CASTS    ].split(split_sym))
            allSetsDict[fields_name_list[COUNTRIES] ].union(set(row[COUNTRIES].split(split_sym))
            allSetsDict[fields_name_list[SUBTYPE]   ].union(set(row[SUBTYPE  ].split(split_sym))
            allSetsDict[fields_name_list[DIRECTORS] ].union(set(row[DIRECTORS].split(split_sym))
            allSetsDict[fields_name_list[USER_TAGS] ].union(set(row[USER_TAGS].split(split_sym))

with open('allSetsDict.txt',w) as recFile:
    recFile.write(allSetsDict)

print 'For the union! We made it !'







YEAR                =7  #8

SUBJECT_ID          =12 #13for debug

GENRES              =19 #20

CASTS               =22 #23

COUNTRIES           =23 #24

SUBTYPE             =27 #28

DIRECTORS           =28 #29

USER_TAGS  		    =32 #31

