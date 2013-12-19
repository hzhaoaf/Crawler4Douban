##A guide to use this  

###content

* IndexMysql.py
	usage:Index the data in the mysql database
	how:follow the tips in the file 
	need:change the default analyzer

* SearchMysql_vx.py
	usage:Search the index made by IndexMysql
	how:

		python SearchMysql_vx.py command
		
		or 

		import it in search.py, which is a py connecting Django on server, and use *run()* method after config.

	need:N.A

* SearchFiles.py
	usage: a temp script used for searching adjs   
	how:

		python SearchFiles.py
	need:N.A




* curve.m
	usage:get right function with Matlab

* formatAllSetsDict.py
	usage:format the original allSetsDict.txt --> word<￥>field type

* getBigSet.py
	usage:get allSetsDict.txt from mysql

---

* getAllAdjs.py 
	usage:use Ictclas or LPT to split the text. Then get the text splited and all adjs restore them in a json format.

* indexAdjFiles.py
	usage:RT

* countTerms_adj.py
	usage:count terms in the adjs index((actually tf of a term in a doc), and make a file for each movie named by its id recording the adjs. in folder fenci_tfidf.
	how:be careful with folders
	need:N.A

* getTopAdjs.py
	usage:get the most adjs in each tfidf-file, output to a single file(movieAdjs.txt)

* adjsToMysql.py
	usage:insert all the adj list in a single file(movieAdj.txt) to mysql
	how:config and run it 
	need:N.A

---

* utils.py 
	usage: some useful tools including reRank method

* sqlConstants.py
	usage: some constants


###what about now?


###What need to be done next ?


###attention 
1.	use 

		sudo python IndexMysql.py
	or you'll get a JavaError without *sudo*.
