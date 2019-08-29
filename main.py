"""
describe:
@project: 智能广告项目
@author: Jony
@create_time: 2019-07-09 12:21:10
@file: dd.py
"""

from collections import Counter
import pickle as pkl
import os
import jieba.posseg as pseg
import utils_

"""
1. 负责清洗数据的类，根据配置删除停用词、低频词、特殊符号，空行等等只保留中文文本信息
2. 并转化成对应的id和词标签id号，固定句长，短补长接
"""

class Datapre:
    """
    初始化，对应参数分别为：固定句子长度，删去词的词频，补齐的方向，读取word文档的路径
    """
    def __int__(self, sen_len, min_frq=1, pad_back=True, file_path="data.txt",dict_path="dicts.pkl"):
        self.sen_len = sen_len
        self.min_frq = min_frq
        self.pad_back = pad_back
        self.file_path = file_path
        self.dict_path = dict_path

        # 读取停用词
        # stopwords = [line.strip() for line in open("stop_words.txt","r",encoding="utf-8")]  # 自己的写法
        stop_words = set()
        for line in open(file_path):
            stop_words.add(line.strip())
        self.stopwords = stop_words