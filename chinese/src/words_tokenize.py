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
import codecs

from stanfordcorenlp import StanfordCoreNLP

logger = Logger().get_logger()


def word_tokenize(sents, nlp):
	tokenses = []
	for sent in sents:
		tokenses.append(nlp.word_tokenize(sent))
	return tokenses


if __name__ == '__main__':
	input = "../data/corpus/sents.txt"
	output = "../data/corpus/words.txt"
	
	# nlp = StanfordCoreNLP("c:/stanford-corenlp-full-2018-02-27",lang='zh')
	nlp = StanfordCoreNLP('http://corenlp.run', port=80, lang='zh')
	
	sents = IOHelper.read_lines(os.path.abspath(input))
	
	if sents == None:
		logger.info("read failed.")
		sys.exit(0)
	
	wordses = []
	for sent in sents:
		words = nlp.word_tokenize(sent.strip())
		wordses.append(words)
	
	IOHelper.write_tokenses(wordses)
	
	nlp.close()
