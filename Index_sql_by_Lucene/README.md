##A guide to use this  
###1.Install mysql   
	sudo apt-get install mysql-server
	sudo apt-get install python-mysql
###2.Create a table and import the sql data  
	use yourDatabase
	source moive_items
###3.Modify the IndexMysql.py to adjust your env (follow the tips in the .py file) before you do this  
	python IndexMysql.py
###4.1 Enjoy it!  
	python SearchMysql.py

type in：
	title keyword_of_summary
like：
	>>神都龙王 狄仁杰

###4.2 Enjoy it!  
	python SearchMysql2.py

type in like：
	title:龙王 AND 狄仁杰 summary:武则天


###what about now?
Use whitespaceAnalyzer instead of SCAnalyzer to index and search casts and dorectors

###What need to be done next ?
1. Debug Log of the test query
2. the poor structure of the code

###attention 
1.	use 

		sudo python IndexMysql.py
	you'll get a JavaError without *sudo*.