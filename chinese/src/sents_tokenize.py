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

if __name__ == '__main__':
	input = "../data/raw/chinaautonews.txt"
	output = "../data/corpus/sents.txt"


	text = "中国汽车新闻网讯4月17日，Jeep家族最新的七座中型SUV——大指挥官已于今日正式上市，售价区间为27.98-40.98万元。新车外观基本还原了云图概念车的设计，内饰采用典型的Jeep设计风格。动力传动系统搭载2.0T+9AT组合。Jeep大指挥官的外观基本还原了云图概念车的设计。"
	# with codecs.open(input, 'r', encoding='utf-8') as f:
	# 	text = f.read()

	print(sents)
	# with codecs.open(output, 'w', encoding='utf-8') as f:
	# 	f.writelines('\n'.join(sents))

