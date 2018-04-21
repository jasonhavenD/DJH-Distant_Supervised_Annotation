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


def ner2word(sent, begin, end):
	word = ""
	for i in range(begin, end + 1):
		word += sent[i].split('/')[0]
	return word


def get_bgrams_of_entities(entities):
	words = []
	for item in entities:
		tag, begin, end = item.split('/')
		word = ner2word(sent, int(begin), int(end))
		words.append(word)
	return ngrams(words, 2)


if __name__ == '__main__':
	input_ner = "../data/small/words_ner.txt"
	input_entities = "../data/small/words_ner_entities.txt"
	output = "../data/small/corpus.txt"
	
	sents = IOHelper.read_lines(os.path.abspath(input_ner))
	entities_sents = IOHelper.read_lines(os.path.abspath(input_entities))
	
	client = MongoClient()
	client = MongoClient('202.117.179.250', 27017)
	db = client.dbpedia  # 连接数据库
	baike_triples = db.baike_triples  # 使用集合
	logger.info("连接数据库成功")
	
	begin = datetime.datetime.now()
	
	for sent, entities in zip(sents[:10], entities_sents[:10]):
		if entities.strip() == 'None':
			continue
		entities = entities.strip().split('\t')
		if len(entities) < 2:
			continue
		sent = sent.strip().split('\t')
		bgram_ners = get_bgrams_of_entities(entities)
		try:  # 句子 实体对
			logger.info(list(bgram_ners))
			# 在知识库中查询是否有关系 两个实体，如果有则记录没有则继续
			# logger.info("查询两个实体在知识库中是否有关系")
			# logger.info("如果没有关系则进行下一对")
			# logger.info("如果有关系，则对结果进行筛选")
			# logger.info("以  关系，实体1，实体1位置-1，实体1位置-2，实体2，实体2位置-1，实体2位置-2，原句   的格式保存到文本corpus.txt")
		# cursor=baike_triples.find({'rel': '简称'})
		except Exception as e:
			logger.error(e)
	end = datetime.datetime.now()
	logger.info("finish in {}s.".format(end - begin))
