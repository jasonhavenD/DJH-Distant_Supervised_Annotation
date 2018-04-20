#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:simplify
   Author:jason
   date:2018/4/20
-------------------------------------------------
   Change Activity:2018/4/20:
-------------------------------------------------
"""
import sys

sys.path.append('./util')

from snownlp import SnowNLP
from util.io import IOHelper
from util.log import Logger
import os

logger = Logger().get_logger()

if __name__ == '__main__':
	input = "../data/raw/chinaautonews.txt"
	output = "../data/corpus/simplify.txt"
	
	text = IOHelper.read(os.path.abspath(input))
	if text == None:
		logger.info("read failed.")
		sys.exit(0)
	text = SnowNLP(text).han
	IOHelper.write(os.path.abspath(output), text)
