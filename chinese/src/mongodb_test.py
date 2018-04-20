#!/usr/bin/python
# -*- coding: utf-8 -*-
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:create_corpus
   Author:jasonhaven
   date:2018/4/19
-------------------------------------------------
   Change Activity:2018/4/19:
-------------------------------------------------
"""


from pymongo import MongoClient
import datetime
from util import log

logger = log.Logger().get_logger()


def insert_chunk2mongo(collection, documents):
	try:
		for doc in documents:
			collection.insert(doc)
	except Exception as e:
		logger.error(e)


if __name__ == '__main__':
	input = "../CN-DBpedia/baike_triples.txt"

	text = []
	names = ['e1', 'rel', 'e2']
	delimiter = "\t"

	client = MongoClient()
	client = MongoClient('202.117.179.250', 27017)
	db = client.dbpedia  # 连接数据库，没有则自动创建
	baike_triples = db.baike_triples  # 使用集合，没有则自动创建
	begin = datetime.datetime.now()
	try:
		print("hello")
	except Exception as e:
		logger.error(e)
	end = datetime.datetime.now()
	logger.info("finish in {}s.".format(end - begin))


