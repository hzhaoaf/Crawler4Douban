
#normlization !!!
#越高越好，但是要在一定程度上避免 平均分比较低 但是 评分人数高的电影
#虽然有时候也需要这样
rating_total = (rating_av * ratings_c)/(10*ratings_c_max)

#可以反映一个电影的受欢迎程度
popularity = (do_c + collect_c + wish_c)/dcw_max

#trends如果太小，那么就说明这个电影已经过气了,而如果wish_c比较多，则说明最近比较火. 注意这个值在normalize之前可能会大于1
#最近的火热程度
trends = (wish_c/(collect_c+do_c))/tr_max if collect_c != 0 else 0

#观后感，反应影片的深刻程度
impressive = 0.3*comments_c/comments_c_max + 0.7*reviews_c/reviews_c_max

#temp adjustment
rating_total = f_tu(rating_total)
impressive = f_tu(impressive)


#it is a measure of whether a movie should be addBoost, =1 means it is a  totally good movie which should be boosted
boostProb = 0.6*f(rating_total) + 0.2*f(impressive) + 0.15*popularity + 0.05*trends

结果：
3412830:狄仁杰之通天帝国/2.5705194
5996801:狄仁杰之神都龙王/1.721988
4090554:少年狄仁杰/1.0000805
2995948:神探狄仁杰/1.0141044

分析：少年狄仁杰 和 神探狄仁杰 的权重过于接近，估计是因为 
rating_total = (rating_av * ratings_c)/(10*ratings_c_max)
分母太大，将数值变低了

解决：
直接使用 平均打分/10  或者在搜索之后进行一个数值拉伸



---

平均打分/10

#normlization !!!
#越高越好，但是要在一定程度上避免 平均分比较低 但是 评分人数高的电影
#虽然有时候也需要这样
rating_total = (rating_av * ratings_c)/(10*ratings_c_max)

#可以反映一个电影的受欢迎程度
popularity = (do_c + collect_c + wish_c)/dcw_max

#trends如果太小，那么就说明这个电影已经过气了,而如果wish_c比较多，则说明最近比较火. 注意这个值在normalize之前可能会大于1
#最近的火热程度
trends = (wish_c/(collect_c+do_c))/tr_max if collect_c != 0 else 0

#观后感，反应影片的深刻程度
impressive = 0.3*comments_c/comments_c_max + 0.7*reviews_c/reviews_c_max

#temp adjustment
rating_total = f_tu(rating_total)
impressive = f_tu(impressive)


#it is a measure of whether a movie should be addBoost, =1 means it is a  totally good movie which should be boosted
boostProb = 0.5*f(float(rating_av)/10) + 0.3*f(impressive) + 0.15*popularity + 0.05*trends

#print rating_total, impressive, popularity, trends
return boostProb

2995948:神探狄仁杰-->5.086066
4160349:狄仁杰断案传奇-->5.3493004
3412830:狄仁杰之通天帝国-->5.060738
4090554:少年狄仁杰-->3.7194934
5996801:狄仁杰之神都龙王-->5.009498
3190095:月上江南之狄仁杰洗冤录-->4.2933254
6808707:护国良相狄仁杰之风摧边关-->4.693164
3892394:仁医-->5.3154483

分析：显然平均分/10的数值相对较大，导致平均分权重太高，而人数的权重在数值上相对较低
解决：适当给予平均分/10降低数值，并增加人数权重

---

	#it is a measure of whether a movie should be addBoost, =1 means it is a  totally good movie which should be boosted
	boostProb = 0.4*f(float(rating_av)*0.5/10) + 0.4*f(impressive) + 0.15*popularity + 0.05*trends

2995948:神探狄仁杰-->2.305008
4160349:狄仁杰断案传奇-->2.5048697
3412830:狄仁杰之通天帝国-->2.9580033
5996801:狄仁杰之神都龙王-->2.659228
4090554:少年狄仁杰-->1.7106367
3190095:月上江南之狄仁杰洗冤录-->1.9175633
6808707:护国良相狄仁杰之风摧边关-->2.0888815
10801896:护国良相狄仁杰之古墓惊雷-->1.0000381

神探狄仁杰评分 8.1 
狄仁杰断案传奇是一个很老很小众的电视剧，但是评分居然有 8.6！！！
大部分评分都集中在 1-3 这个范围， f函数的作用有没有体现？ 如果没有作用，反而可能会起副作用


想到：用户搜索的关键词对应的可能 boost 都不是很高， 怎么能在这些结果中达到区分的效果：使用  数值拉伸 并且 使用修改的f 函数


---

	boostProb = 0.4*(float(rating_av)*0.5/10) + 0.4*impressive + 0.15*popularity + 0.05*trends


3412830:狄仁杰之通天帝国-->3.5397623
2995948:神探狄仁杰-->2.4961658
4160349:狄仁杰断案传奇-->2.6035857
4090554:少年狄仁杰-->2.0261774
5996801:狄仁杰之神都龙王-->3.2528517
3190095:月上江南之狄仁杰洗冤录-->2.1892247
6808707:护国良相狄仁杰之风摧边关-->2.3143885
10801896:护国良相狄仁杰之古墓惊雷-->1.0001074

加权的结果虽然是比较合理的，但是大家都进行了很大的加权，神都龙王的 3.25的加权意义就不大了

解决：

1. 数值上进行区分
2. 直接按照权值排序！



---

#人工排序
    retList = sorted(retList, key=operator.itemgetter('boost'), reverse=True)  

3412830:狄仁杰之通天帝国-->3.5397623
5996801:狄仁杰之神都龙王-->3.2528517
10561898:仁显王后的男人-->3.11168
4881202:仁医 完结篇-->2.7670016
3892394:仁医-->2.719505
2963313:百年拜仁-->2.6979835
3581476:太空堡垒卡拉狄加  第一季-->2.6315176
3581471:太空堡垒卡拉狄加  第二季-->2.6295528
3581466:太空堡垒卡拉狄加 第四季-->2.6153116
4225354:席琳·狄翁：全世界的目光-->2.6150103


不可行

想到：boostProb 需要保证有的doc能达到1 !!!!!!!!!!!!!!!!!!!!!!!!!
在 getMax的时候就进行各个因子的加权，得到一个 tmp_prob，（每个因子需要 数值归一化 权重需要考虑 但是权重之和不必再为1,但是数值也必须在一个量级）
这样就可以进行将prob进行归一，


---

	boostProb = 0.4*(float(rating_av)*0.3/10) + 0.4*impressive + 0.15*popularity + 0.05*trends


3412830:狄仁杰之通天帝国-->3.0789623
5996801:狄仁杰之神都龙王-->2.7560518
4160349:狄仁杰断案传奇-->1.9627856
2995948:神探狄仁杰-->1.9129657
4090554:少年狄仁杰-->1.6157774
3190095:月上江南之狄仁杰洗冤录-->1.7140247
6808707:护国良相狄仁杰之风摧边关-->1.7887884
10801896:护国良相狄仁杰之古墓惊雷-->1.0001074

结果还是可以的



#为了减少一个电影由于太过热门，而把一些不够热门的好电影给去掉，电影热门程度在权重和评分中的比重应该是一个 sqrt类型的凸函数，甚至
可以是一个 /— 型的函数






7. Wrapper：
既然Search的时候（或者是Index的时候？？ 使用查看功能验证一下） analyzerWrapper貌似不管用，那就进行每个域的预处理，然后外部分词,即重写query
然后全部使用 whiteSpaceAnalyzer


1. tags 长度？ norm？ 这样就不用在开始对比较热门的电影增加过多的权值

4. 分词

5. 统计 ML:sklearn

6. 时间信息 作为因子
已经将时间格式统一




2. 提前加权，是为了把好电影，热门电影能够排在前1000？ 加权力度要控制好

3. 得到lucene的score，进行事后加权

		问题：如何将 tag:人性 中的 人数体现出来

		Index的时候加权：
		不能整体加权，不能区分

		查询到来时：
		计算相关度的时候加权，过来一个query，在search tags 域的时候考虑人数信息：
		How？

		1. 评论人数 在实际情况中相当于 tf 即 词频， 可以修改打分公式中的 tf，将其由 1或者0（现有情况下的tag）替换为 评分人数
		但是要修改评分公式，可能会造成系统不稳定..
		2. 直接填充，这太傻比了
		3. 接到用户query之后，进行Index，重新调整权值。。。不管怎么说，这是一个思路

		我还是觉得1是最靠谱的方法！

		查询结束后：
		加权，排序


* 填充 tags(已填充'￥￥￥<>0') ， 得到score ，| 验证wrapper

* 

* 加权（增加时间因子、tags人数因子），更改tf