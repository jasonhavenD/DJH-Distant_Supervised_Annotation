#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:entity_recognize
   Author:jasonhaven
   date:2018/4/19
-------------------------------------------------
   Change Activity:2018/4/19:
-------------------------------------------------
"""

import sys
import time

sys.path.append('./util')

import os
import datetime
from stanfordcorenlp import StanfordCoreNLP
from util.io import IOHelper
from util.log import Logger
from sents_tokenize import *
from nltk import ngrams

logger = Logger().get_logger()


def stanfordNE2BIEO(tagged_sent):
	tagged_sent.insert(0, ('sent', 'O'))
	tri_ners = ngrams(tagged_sent, 3)
	bieo_words = []
	entities = []
	flag = False
	for i, item in enumerate(tri_ners):
		pre, cur, next = item
		w_pre, t_pre = pre
		w_cur, t_cur = cur
		w_next, t_next = next
		if t_cur == 'O':
			bieo_words.append((w_cur, t_cur))
		else:
			if t_pre == 'O':
				bieo_words.append((w_cur, 'B-' + t_cur))
				if t_next == 'O':  # 单实体
					entities.append([t_cur, i, i])
				else:
					entities.append([t_cur, i, i])
					flag = True
			else:
				if t_pre == t_cur:
					if t_next == t_cur:
						bieo_words.append((w_cur, 'I-' + t_cur))
					else:
						bieo_words.append((w_cur, 'E-' + t_cur))
						if flag:
							entities[-1][2] = i  # 多实体结束
							flag = False

				else:
					bieo_words.append((w_cur, 'B-' + t_cur))
					if t_next == 'O':  # 单实体
						entities.append([t_cur, i, i])
					else:
						entities.append([t_cur, i, i])
						flag = True

	return bieo_words, entities


delimiter = '\t'

if __name__ == '__main__':
	input = "../data/small/words.txt"
	output = "../data/small/words_ner.txt"
	output_entities = "../data/small/words_ner_entities.txt"
	output_feedback = "../data/small/words_feedback_from_ner.txt"

	nlp = StanfordCoreNLP("c:/stanford-corenlp-full-2018-02-27", lang='zh')
	# nlp = StanfordCoreNLP('http://corenlp.run', port=80, lang='zh')

	begin = datetime.datetime.now()

	sents = IOHelper.read_lines(os.path.abspath(input))

	if sents == None:
		logger.info("read failed.")
		sys.exit(0)

	ner_sents = []
	ner_entities = []
	error_lines = []
	cnt = 0
	for line in sents[:20000]:
		cnt += 1  # 从1开始
		try:
			ner_sent, entities = stanfordNE2BIEO(nlp.ner(line))
			ner_sents.append(ner_sent)
			ner_entities.append(entities)
			logger.info('{} has been added!'.format(cnt))
		except Exception as e:
			logger.info('filter {}'.format(cnt))
			error_lines.append(cnt)
			continue

	IOHelper.write_tagged_tokenses(os.path.abspath(output), ner_sents)
	IOHelper.write_entities(os.path.abspath(output_entities), ner_entities)

	time.sleep(2)

	# feedback
	if error_lines != []:
		for i in reversed(error_lines):  # 动态调整，从大到小删除正确
			sents.pop(i - 1)  # 从1开始
		save_lines(sents, output_feedback)

	end = datetime.datetime.now()
	logger.info('finish in {}s'.format(end - begin))

	nlp.close()
