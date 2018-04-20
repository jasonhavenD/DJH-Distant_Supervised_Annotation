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

from nltk import pos_tag
from nltk.chunk import conlltags2tree, tree2conllstr
from stanfordcorenlp import StanfordCoreNLP
import sys

sys.path.append('./util')

from util.io import IOHelper
from util.log import Logger
import os
import codecs

from stanfordcorenlp import StanfordCoreNLP

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
	input = "../data/corpus/sents.txt"
	output = "../data/corpus/ner.txt"
	
	nlp = StanfordCoreNLP("c:/stanford-corenlp-full-2018-02-27", lang='zh')
	# nlp = StanfordCoreNLP('http://corenlp.run', port=80, lang='zh')
	
	sents = IOHelper.read_lines(os.path.abspath(input))
	
	if sents == None:
		logger.info("read failed.")
		sys.exit(0)
	
	with open(output, 'w', encoding='utf-8') as f:
		for sent in sents:
			ner_sent = nlp.ner(sent)
			for word_with_tag in stanfordNE2BIO(ner_sent):
				f.write('/'.join(word_with_tag))
				f.write(delimiter)
			f.write("\n")
	
	nlp.close()

# https://www.e-learn.cn/content/wangluowenzhang/168232
