#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:save_dbpedia2db
   Author:jasonhaven
   date:2018/4/19
-------------------------------------------------
   Change Activity:2018/4/19:
-------------------------------------------------
"""


def insert2mysql():
	'''
	修改my.ini 缓存大小
	修改等待时间
	因为数据中存在单引号和其他特殊字符，sql语句会报错，导致插入失败，所以使用mongodb
	:return:
	'''
	input = "../CN-DBpedia/small_baike_triples.txt"
	output = "../CN-DBpedia/baike_triples.csv"

	text = []
	names = ['e1', 'rel', 'e2']
	delimiter = "\t"
	reader = pd.read_table(input, sep='\t', chunksize=500, engine='c', names=names)

	# 打开数据库连接
	conn = pymysql.connect(host="localhost", user="root", password="root", database="dbpedia", charset="utf8")

	# 使用 cursor() 方法创建一个游标对象 cursor
	cursor = conn.cursor()

	# 使用 execute()  方法执行 SQL 查询
	prefix = "insert into baike_triples(e1,rel,e2) values "
	values = ""

	begin = datetime.datetime.now()
	# sql="insert into baike_triples(e1,rel,e2) values('{}','{}','{}')".format(u'a', u'b', u'c')
	# cursor.execute(sql)
	try:
		for chunk in reader:
			for i in chunk.index:
				row = chunk.loc[i]
				values += "('{}','{}','{}'),".format(row['e1'], row['rel'], row['e2'])
				sql = prefix + values[:-1]
			cursor.execute(sql)
			conn.commit()  # 如果执行成功就提交事务
			logger.info("{} insert successfully!".format(i + 1))
	except Exception as e:
		conn.rollback()  # 如果执行失败就回滚事务
		raise e
	finally:
		conn.close()
	end = datetime.datetime.now()
	logger.info("finish in {}s.".format(end - begin))


import pandas as pd
import pymysql
from pymongo import MongoClient
import pymongo
import datetime
from util import log

logger = log.Logger().get_logger()

if __name__ == '__main__':
	input = "../CN-DBpedia/small_baike_triples.txt"
	output = "../CN-DBpedia/baike_triples.csv"

	text = []
	names = ['e1', 'rel', 'e2']
	delimiter = "\t"
	reader = pd.read_table(input, sep='\t', chunksize=500, engine='c', names=names)

	client = MongoClient()
	client = MongoClient('localhost', 27017)
	# db = client.dbpedia  # 连接数据库，没有则自动创建
	# baike_triples = db.baike_triples  # 使用集合，没有则自动创建
	db = client.test_db
	collection = db.test_collection
	document = {"name": "zhangsan", "age": 18}
	collection.save(document)

	#
	# begin = datetime.datetime.now()
	# try:
	# 	for chunk in reader:
	# 		for i in chunk.index:
	# 			row = chunk.loc[i]
	# 		# 构造数据json
	# 		# 一次插入多个
	# 		logger.info("{} insert successfully!".format(i + 1))
	# except Exception as e:
	# 	raise e
	# finally:
	# 	db.close()  # close
	# end = datetime.datetime.now()
	# logger.info("finish in {}s.".format(end - begin))
