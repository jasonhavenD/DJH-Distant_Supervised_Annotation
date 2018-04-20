#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:io
   Author:jasonhaven
   date:2018/4/17
-------------------------------------------------
   Change Activity:2018/4/17:
-------------------------------------------------
"""
import codecs
import os


class IOHelper():
	@classmethod
	def write(cls, file, text):
		with codecs.open(file, 'w', encoding='utf-8') as f:
			f.write(text)

	@classmethod
	def read(cls, file):
		if os.path.exists(file):
			return codecs.open(file, 'r', encoding='utf-8').read()
		else:
			return None

	@classmethod
	def read_lines(cls, file):
		if os.path.exists(file):
			return codecs.open(file, 'r', encoding='utf-8').readlines()
		else:
			return None

	@classmethod
	def write_lines(cls, file, sents):
		with codecs.open(file, 'w', encoding='utf-8') as f:
			f.writelines('\n'.join(sents))

	@classmethod
	def write_tokenses(cls, file, tokenses):
		with codecs.open(file, 'w', encoding='utf-8') as f:
			for tokens in tokenses:
				f.write('\t'.join(tokens))
				f.write("\n")

	@classmethod
	def write_tagged_tokenses(cls, file, tagged_tokenses):
		with codecs.open(file, 'w', encoding='utf-8') as f:
			for pos_tag_tokens in tagged_tokenses:
				for word_with_tag in pos_tag_tokens:
					f.write('/'.join(word_with_tag))
					f.write('\t')
				f.write("\n")


if __name__ == '__main__':
	input = "D:\github\A_DJH\DJH-OpenRE\chinese\data\\raw\chinaautonews.txt"
	output = "test2.py"

	text = IOHelper.read(input)
	print(text[:10])
