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

logger = Logger().get_logger()


def stanfordNE2BIO(tagged_sent):
	bio_tagged_sent = []
	prev_tag = "O"
	for token, tag in tagged_sent:
		if tag == "O":  # O
			bio_tagged_sent.append((token, tag))
			prev_tag = tag
			continue
		if tag != "O" and prev_tag == "O":  # Begin NE
			bio_tagged_sent.append((token, "B-" + tag))
			prev_tag = tag
		elif prev_tag != "O" and prev_tag == tag:  # Inside NE
			bio_tagged_sent.append((token, "I-" + tag))
			prev_tag = tag
		elif prev_tag != "O" and prev_tag != tag:  # Adjacent NE
			bio_tagged_sent.append((token, "B-" + tag))
			prev_tag = tag

	return bio_tagged_sent


delimiter = '\t'

if __name__ == '__main__':
	input = "../data/corpus/words.txt"
	output = "../data/corpus/words_ner.txt"
	output_feedback = "../data/corpus/words_feedback_from_ner.txt"

	nlp = StanfordCoreNLP("c:/stanford-corenlp-full-2018-02-27", lang='zh')
	# nlp = StanfordCoreNLP('http://corenlp.run', port=80, lang='zh')

	begin = datetime.datetime.now()

	sents = IOHelper.read_lines(os.path.abspath(input))

	if sents == None:
		logger.info("read failed.")
		sys.exit(0)

	ner_sents = []
	error_lines = []
	cnt = 0
	for line in sents:
		cnt += 1  # 从1开始
		try:
			ner_sent = stanfordNE2BIO(nlp.ner(line))
			ner_sents.append(ner_sent)
			logger.info('{} has been added!'.format(cnt))
		except Exception as e:
			error_lines.append(cnt)
			continue

	IOHelper.write_tagged_tokenses(os.path.abspath(output), ner_sents)

	time.sleep(2)

	# feedback
	if error_lines != []:
		for i in reversed(error_lines):  # 动态调整，从大到小删除正确
			sents.pop(i - 1)# 从1开始
		save_lines(sents, output_feedback)

	end = datetime.datetime.now()
	logger.info('finish in {}s'.format(end - begin))

	nlp.close()
