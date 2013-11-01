##A guide to use this  
###1.Install mysql   
	sudo apt-get install mysql-server
	sudo apt-get install python-mysql
###2.Create a table and import the sql data  
	use yourDatabase
	source moive_items
###3.Modify the IndexMysql.py to adjust your env (follow the tips in the .py file) before you do this  
	python IndexMysql.py
###4.Enjoy it!  
	python SearchMysql.py
