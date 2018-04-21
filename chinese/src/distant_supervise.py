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
from nltk import ngrams
from util.io import IOHelper
import os

logger = log.Logger().get_logger()


def pre_process_words_ner(words_ner):
	'''
	合并BIO实体，并记录在原句子中的begin,end
	ner={BIO实体，begin，end}  [begin,end]
	ners=[ner,ner,ner]
	:param words_ner:
	:return:
	'''
	ners = []
	ner = ()
	for i, item in enumerate(words_ner):
		word, tag = item.strip().split('/')
		begin = end = i
		ner = (word, begin, end)  # 对于'O'而言 [begin,end]
		print(ner)
		if tag == 'O':
			continue
		if tag.startswith('B-'):
			ner=(word,begin,end)

	# ner1 = ('中国', 1, 3)
	# ner2 = ('北京', 5, 7)
	# ner3 = ('天安门', 12, 16)
	# ner4 = ('故宫', 18, 23)
	#
	# ners = [ner1, ner2, ner3, ner4]
	return ngrams(ners, 2)


if __name__ == '__main__':
	input = "../data/small/words_ner.txt"
	output = "../data/small/corpus.txt"

	words_ners = IOHelper.read_lines(os.path.abspath(input))

	for words_ner in words_ners[:3]:
		bgram_ners = pre_process_words_ner(words_ner.strip().split('\t'))
		print(list(bgram_ners))


# text = []
# names = ['e1', 'rel', 'e2']
# delimiter = "\t"
#
# client = MongoClient()
# client = MongoClient('202.117.179.250', 27017)
# db = client.dbpedia  # 连接数据库
# baike_triples = db.baike_triples  # 使用集合
# logger.info("连接数据库成功")
#
# begin = datetime.datetime.now()
# try:
# 	logger.info("获取实体bgrams")
# 	logger.info("查询两个实体在知识库中是否有关系")
# 	logger.info("如果没有关系则进行下一对")
# 	logger.info("如果有关系，则对结果进行筛选")
# 	logger.info("以  关系，实体1，实体1位置-1，实体1位置-2，实体2，实体2位置-1，实体2位置-2，原句   的格式保存到文本corpus.txt")
# 	# cursor=baike_triples.find({'rel': '简称'})
# except Exception as e:
# 	logger.error(e)
# end = datetime.datetime.now()
# logger.info("finish in {}s.".format(end - begin))
