#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:sents_tokenize
   Author:jason
   date:2018/4/20
-------------------------------------------------
   Change Activity:2018/4/20:
-------------------------------------------------
"""

import os

# 设置分句的标志符号
cutlist = "。！？…!?"
punct_pair_str = "《》“”‘’{}（）()【】\"\""
punct_pair_hm = {}

sent_count = 0


# 检查某字符是否分句标志符号的函数；如果是，返回True， 否则返回False
def FindTok(char):
	global cutlist
	if char in cutlist:
		return True
	else:
		return False


def CutSent(cut_str):
	sent_list = []
	sent = []
	
	punct_pair = []
	
	for ch in cut_str:
		AddPunct(punct_pair, ch)
		if FindTok(ch):
			sent.append(ch)
			if len(punct_pair) == 0:
				sent_list.append(''.join(sent))
				sent = []
				punct_pair = []
		else:
			sent.append(ch)
	
	if len(sent) != 0:
		sent_list.append(''.join(sent))
	return sent_list


def ConstPunctPair():
	global punct_pair_str, punct_pair_hm
	
	for index in range(0, len(punct_pair_str), 2):
		punct_pair_hm[punct_pair_str[index + 1]] = punct_pair_str[index]


def AddPunct(punct_pair, ch):
	global punct_pair_str, punct_pair_hm
	
	if ch not in punct_pair_str:
		return punct_pair
	
	if len(punct_pair_hm) == 0:
		ConstPunctPair()
	
	if ch not in punct_pair_hm:
		punct_pair.append(ch)
		return punct_pair
	
	hasMatch = False
	pair_ch = punct_pair_hm[ch]
	for index in range(len(punct_pair) - 1, -1, -1):
		if punct_pair[index] == pair_ch:
			del punct_pair[index]
			hasMatch = True
			break
	if not hasMatch:
		punct_pair.append(ch)
	
	return punct_pair


def handle_file(input_path, output_path):
	global sent_count
	
	fpw = open(output_path, 'w', encoding='utf-8')
	
	for line in open(input_path, 'r', encoding='utf-8').readlines():
		new_line = line[:-1]
		
		sent_list = CutSent(new_line)
		for sent in sent_list:
			sent_count += 1
			fpw.write(sent + "\n")
	fpw.close()



if __name__ == "__main__":
	input = "../data/corpus/simplify.txt"
	output = "../data/corpus/sents.txt"
	handle_file(input, output)
