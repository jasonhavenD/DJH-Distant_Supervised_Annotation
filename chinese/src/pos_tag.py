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
import time
from stanfordcorenlp import StanfordCoreNLP
import datetime

logger = Logger().get_logger()

if __name__ == '__main__':
	input = "../data/corpus/words.txt"
	output = "../data/corpus/words_tagged.txt"
	output_feedback = "../data/corpus/words_feedback_from_pos.txt"

	nlp = StanfordCoreNLP("c:/stanford-corenlp-full-2018-02-27", lang='zh')
	# nlp = StanfordCoreNLP('http://corenlp.run', port=80, lang='zh')

	begin = datetime.datetime.now()

	sents = IOHelper.read_lines(os.path.abspath(input))

	if sents == None:
		logger.info("read failed.")
		sys.exit(0)

	pos_sents = []

	error_lines = []
	cnt = 0

	for line in sents:
		cnt += 1  # 从1开始
		try:
			line_tagged = nlp.pos_tag(line)
			pos_sents.append(line_tagged)
			logger.info('{} has been added!'.format(cnt))
		except Exception as e:
			error_lines.append(i)
			continue

	IOHelper.write_tagged_tokenses(os.path.abspath(output), pos_sents)

	time.sleep(2)

	# feedback
	if error_lines != []:
		for i in reversed(error_lines):  # 动态调整，从大到小删除正确
			sents.pop(i - 1)# 从1开始
		save_lines(sents, output_feedback)

	end = datetime.datetime.now()
	logger.info('finish in {}s'.format(end - begin))

	nlp.close()
