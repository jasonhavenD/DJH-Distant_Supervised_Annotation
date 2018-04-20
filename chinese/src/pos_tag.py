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

if __name__ == '__main__':
	input = "../data/corpus/words.txt"
	output = "../data/corpus/words_tagged.txt"
	
	nlp = StanfordCoreNLP("c:/stanford-corenlp-full-2018-02-27",lang='zh')
	# nlp = StanfordCoreNLP('http://corenlp.run', port=80, lang='zh')
	
	wordses = IOHelper.read_lines(os.path.abspath(input))
	
	if wordses == None:
		logger.info("read failed.")
		sys.exit(0)
	
	wordses_tagged = []
	
	for line in wordses[:3]:
		if line.strip() == '':
			continue
		line_tagged = nlp.pos_tag(line.split('\t'))
		print(line_tagged)
		# wordses_tagged.append(line_tagged)
	
	# IOHelper.write_tokenses(wordses_tagged)
	
	nlp.close()
