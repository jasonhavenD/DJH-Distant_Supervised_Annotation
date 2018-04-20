#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:test
   Author:jasonhaven
   date:2018/4/20
-------------------------------------------------
   Change Activity:2018/4/20:
-------------------------------------------------
"""
import os
import sys
from util.io import IOHelper

if __name__ == '__main__':
	f1 = "../data/corpus/words.txt"
	f2 = "../data/corpus/words_tagged.txt"
	f3 = "../data/corpus/words_ner.txt"
	f4 = "../data/corpus/sents_feedback.txt"
	f5="../data/corpus/words_feedback_from_ner.txt"

	sent1 = IOHelper.read_lines(f1)
	sent2 = IOHelper.read_lines(f2)
	sent3 = IOHelper.read_lines(f3)
	sent4 = IOHelper.read_lines(f4)
	sent5 = IOHelper.read_lines(f5)
	print(len(sent1), len(sent2), len(sent3), len(sent4),len(sent5))
