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
import codecs
from stanfordcorenlp import StanfordCoreNLP

if __name__ == '__main__':
	input = "../data/raw/chinaautonews.txt"
	output = "../data/corpus/sents.txt"

	nlp=StanfordCoreNLP("F:\BiShe\stanford-corenlp-full-2018-02-27")



