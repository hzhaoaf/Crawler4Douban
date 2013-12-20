#!usr/bin/python 
#coding:utf-8

RATING_MAX          =0  
RATING_AVERAGE      =1  #2<--this # means that this field is indexed in lucene
RATING_STARS        =2  #3
RATING_MIN          =3  
REVIEWS_COUNT       =4  #5 影评数目
WISH_COUNT          =5  #6 想看人数
DOUBAN_SITE         =6  
YEAR                =7  #8
IMAGE_SMALL         =8  #9 for show
IMAGE_LARGE         =9
IMAGE_MEDIUM        =10
SUBJECT_URL         =11
SUBJECT_ID          =12 #13for debug
MOBILE_URL          =13
TITLE               =14 #15
DO_COUNT            =15     #在看
SEASONS_COUNT       =16 
SCHEDULE_URL        =17
EPISODES_COUNT      =18
GENRES              =19 #20
CURRENT_SEASON      =20
COLLECT_COUNT       =21 #22 看过
CASTS               =22 #23
COUNTRIES           =23 #24
ORIGINAL_TITLE      =24 #25
SUMMARY             =25 #26
SUMMARY_SEGMENTATION=26 #27
SUBTYPE             =27 #28
DIRECTORS           =28 #29
COMMENTS_COUNT      =29 #30 多少短评
RATINGS_COUNT       =30 #31 多少人打分
AKA                 =31 #32
USER_TAGS  		    =32 #31
OTHERS_LIKE         =33 #32
ADJS                =34 #33


fields_name_list = \
[\
'rating_max',\
'rating_average',\
'rating_stars',\
'rating_min',\
'reviews_count',\
'wish_count',\
'douban_site',\
'year',\
'image_small',\
'image_large',\
'image_medium',\
'subject_url',\
'subject_id',\
'mobile_url',\
'title',\
'do_count',\
'seasons_count',\
'schedule_url',\
'episodes_count',\
'genres',\
'current_season',\
'collect_count',\
'casts',\
'countries',\
'original_title',\
'summary',\
'summary_segmentation',\
'subtype',\
'directors',\
'comments_count',\
'ratings_count',\
'aka',\
'user_tags',\
'others_like',\
]
#constant's name ------->field name 
#constant's value------->field order in table 

FIELDS_NUM = len(fields_name_list)


delim = '￥' #genres casts aka user_tag others_like countries
delim_uo = '<>'


TAGS_NUM = 20
SPAN = 500
TAGS_AVER_LEN = 100
ADJS_AVER_LEN = 20
TAG_NUM_FACTOR = 0.0001 #so a tag marked by 16000 people will get a times of 1.6
ADJ_NUM_FACTOR = 0.1 # so a adj with a number of 16 will get a times of 1.6

ADJ_NUM = 5
SUMMARY_ADJ_BOOST = 4

#表示对doc的加权范围
DOC_BOOST_RANGE = [1,8]

# for test 
ID = 0
NAME = 1


#flags
DICT = 0
SCOREDOCS = 1

#这个数字越接近当前时间，时间的影响就越大,越近的电影加权越大
NOW = 20500000

#firstMovieTime
firstMovieTime = 18950000 #工厂大门

#统计粒度
COMMENTS_C_LIDU = 5
RATINGS_C_LIDU = 10
PROB_LIDU = 10
DO_C_LIDU = 10
COLLECT_C_LIDU = 10
DCW_LIDU = 10
TR_LIDU = 10
WISH_C_LIDU = 10
REVIEWS_C_LIDU = 3






#---end define constants---



