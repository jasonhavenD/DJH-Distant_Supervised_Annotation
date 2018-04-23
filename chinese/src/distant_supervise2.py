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
import sys
import re
import time

logger = log.Logger().get_logger()


def ner2word(sent, begin, end):
	word = ""
	for i in range(begin, end + 1):
		word += sent[i].split('/')[0]
	return (word, begin, end)


def get_bgrams_of_entities(entities):
	words = []
	for item in entities:
		tag, begin, end = item.split('/')
		word = ner2word(sent, int(begin), int(end))
		words.append(word)
	return ngrams(words, 2)


if __name__ == '__main__':
	input_ner = "../data/corpus/words_ner.txt"
	input_entities = "../data/corpus/words_ner_entities.txt"
	# output = "../data/corpus/corpus1.txt"  # E1，E2完全匹配
	output = "../data/corpus/corpus2.txt"#E1完全，E2模糊

	sents = IOHelper.read_lines(os.path.abspath(input_ner))
	entities_sents = IOHelper.read_lines(os.path.abspath(input_entities))

	if sents == None or entities_sents == None:
		logger.info("read failed.")
		sys.exit(0)

	client = MongoClient()
	client = MongoClient('202.117.179.250', 27017)
	db = client.dbpedia  # 连接数据库
	baike_triples = db.baike_triples  # 使用集合
	logger.info("连接数据库成功")

	begin = datetime.datetime.now()

	max_size = 10
	record_count = 0
	sent_count = 0
	with open(os.path.abspath(output), 'a', encoding='utf-8') as file:
		for sent, entities in zip(sents, entities_sents):
			sent_count += 1
			begin_sent = datetime.datetime.now()

			if entities.strip() == 'None' or len(entities) < 2:
				continue
			# 一条句子
			sent = sent.strip().split('\t')
			# 一条句子中的实体
			entities = entities.strip().split('\t')
			# 一条句子中的实体对
			bgram_ners = get_bgrams_of_entities(entities)
			try:
				for a, b in bgram_ners:
					E1, b1, e1 = a
					E2, b2, e2 = b
					if len(E1) < 2 or len(E2) < 2 or len(E1) > 25 or len(E2) > 25 or (E1.isdigit() and len(E1) < 4) or (
								E2.isdigit() and len(E2) < 4):
						continue
					criteria = {}
					criteria['e1'] = E1
					criteria['e2'] = re.compile(E2)
					# criteria['e2'] = E2

					logger.info('finding for {} and {}...'.format(E1, E2))
					cursor = list(baike_triples.find(criteria).limit(max_size))

					time.sleep(2)

					if len(cursor) == 0:
						logger.info('find result is zero.')
						continue

					for row in cursor:
						rel = row['rel']
						# 关系，实体1,实体1开始、实体1结束，实体2，实体2开始，实体2结束，句子
						record = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(rel, E1, E2, b1, e1, b2, e2, sent)
						file.write(record)
						record_count += 1
						logger.info('write into file {}'.format(record_count))
				end_sent = datetime.datetime.now()
				logger.info('{} sent over in {}s.'.format(sent_count, end_sent - begin_sent))
			except Exception as e:
				logger.info(e)

	end = datetime.datetime.now()
	logger.info("finish in {}s.".format(end - begin))
