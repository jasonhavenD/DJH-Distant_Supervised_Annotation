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


import pandas as pd
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
	reader = pd.read_table(input, sep='\t', chunksize=10000, engine='c', names=names)

	client = MongoClient()
	client = MongoClient('localhost', 27017)
	db = client.dbpedia  # 连接数据库，没有则自动创建
	baike_triples = db.baike_triples  # 使用集合，没有则自动创建

	begin = datetime.datetime.now()
	try:
		for chunk in reader:
			documents = []
			aver_begin = datetime.datetime.now()
			for i in chunk.index:
				row = chunk.loc[i]
				doc = {}
				doc['e1'] = row['e1']
				doc['rel'] = row['rel']
				doc['e2'] = row['e2']
				documents.append(doc)
			insert_chunk2mongo(baike_triples, documents)
			aver_end = datetime.datetime.now()
			logger.info("{} insert successfully in {}s".format(i + 1,aver_end-aver_begin))
	except Exception as e:
		logger.error(e)
	end = datetime.datetime.now()
	logger.info("finish in {}s.".format(end - begin))
