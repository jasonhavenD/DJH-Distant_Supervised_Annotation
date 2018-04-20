#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:sents_tokenize
   Author:jasonhaven
   date:2018/4/19
-------------------------------------------------
   Change Activity:2018/4/19:
-------------------------------------------------
"""
import sys

sys.path.append('./util')

from util.io import IOHelper
from util.log import Logger
import os
import datetime
from sents_tokenize import *

from stanfordcorenlp import StanfordCoreNLP

logger = Logger().get_logger()


def word_tokenize(sents, nlp):
	tokenses = []
	for sent in sents:
		tokenses.append(nlp.word_tokenize(sent))
	return tokenses


import time

if __name__ == '__main__':
	input = "../data/corpus/sents.txt"
	output = "../data/corpus/words.txt"
	output_feedback = "../data/corpus/sents_feedback.txt"

	nlp = StanfordCoreNLP("c:/stanford-corenlp-full-2018-02-27", lang='zh')
	# nlp = StanfordCoreNLP('http://corenlp.run', port=80, lang='zh')

	begin = datetime.datetime.now()

	sents = IOHelper.read_lines(os.path.abspath(input))

	if sents == None:
		logger.info("read failed.")
		sys.exit(0)

	wordses = []
	error_lines = []
	cnt = 0
	for sent in sents:
		cnt += 1  # 从1开始
		try:
			words = nlp.word_tokenize(sent.strip())
			wordses.append(words)
			logger.info('{} has been added!'.format(cnt))
		except Exception as e:
			error_lines.append(cnt)
			continue

	IOHelper.write_tokenses(os.path.abspath(output), wordses)

	print(len(sents), len(wordses), len(error_lines))

	time.sleep(2)

	# feedback
	if error_lines != []:
		for i in reversed(error_lines):  # 动态调整，从大到小删除正确
			sents.pop(i-1)# 从1开始
		save_lines(sents, output_feedback)

	end = datetime.datetime.now()
	logger.info('finish in {}s'.format(end - begin))

	nlp.close()
