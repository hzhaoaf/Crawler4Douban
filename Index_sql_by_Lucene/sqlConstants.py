RATING_MAX          =0  
RATING_AVERAGE      =1  #2<--this # means that this field is indexed in lucene
RATING_STARS        =2  #3
RATING_MIN          =3  
REVIEWS_COUNT       =4  #5
WISH_COUNT          =5  #6
DOUBAN_SITE         =6  
YEAR                =7  #8
IMAGE_SMALL         =8  
IMAGE_LARGE         =9
IMAGE_MEDIUM        =10
SUBJECT_URL         =11
SUBJECT_ID          =12 #13for debug
MOBILE_URL          =13
TITLE               =14 #15
DO_COUNT            =15
SEASONS_COUNT       =16 
SCHEDULE_URL        =17
EPISODES_COUNT      =18
GENRES              =19 #20
CURRENT_SEASON      =20
COLLECT_COUNT       =21 #22
CASTS               =22 #23
COUNTRIES           =23 #24
ORIGINAL_TITLE      =24 #25
SUMMARY             =25 #26
SUMMARY_SEGMENTATION=26 #27
SUBTYPE             =27 #28
DIRECTORS           =28 #29
COMMENTS_COUNT      =29 #30
RATINGS_COUNT       =30 #31
AKA                 =31 #32

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
]
#constant's name ------->field name 
#constant's value------->field order in table 

FIELDS_NUM = len(fields_name_list)

# for test 
ID = 0
NAME = 1
#---end define constants---