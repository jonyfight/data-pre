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
        self.sen_len = sen_len  # self必不可少，规定的句子长度
        self.min_frq = min_frq  # 词频大小
        self.pad_back = pad_back
        self.file_path = file_path  # 文件路径
        self.dict_path = dict_path  # 字典路径

        # 读取停用词
        # stopwords = [line.strip() for line in open("stop_words.txt","r",encoding="utf-8")]  # 自己的写法
        stop_words = set()
        for line in open("stop_words.txt",encoding="utf-8"):
            stop_words.add(line.strip())  # add()方法用于给集合添加元素，如果添加的元素在集合已存在，则不执行任何操作。
        self.stopwords = stop_words

        # 读取违禁词
        prohibited_words = set()
        for line in open("prohibited_words.txt",encoding="utf-8"):
            prohibited_words.add(line.strip())
        self.prohibited_words = prohibited_words

        """
        建立word,tag字典
        """
        def create_dicts(self):
            word2id, id2word, tag2id, id2tag = {"<pad>":0,"***":1},{0:"<pad>",1:"***"},{"<pad>":0,"***":1},{0:"<pad>",1:"***"}

            # 读取文章
            # 词列表
            word_list = []  # 用来存储词
            tag_list = []  # 用来存储词性
            for line in open(self.file_path,"r",encoding="utf-8"):
                line = line.strip()
                # 判断文章内容是否为中文，是就保存字符串
                content = ""
                for i in line:
                    # \u4e00-\u9fa5是用来判断是不是中文的一个条件，采用的是unicode编码
                    if i >= u'\u4e00' and i <= '\u9fa5':
                        content += i

                # 获取分词及词性
                res = pseg.cut()  # 分词并获得词性
                for w in res:
                    if w.word in self.stop_words:  # 如果遍历文章内容出现停用词，则跳过
                        continue
                    elif w.word in self.prohibited_words:  # 如果遍历文章内容出现违禁词，则跳过
                        continue
                    else:
                        word_list.append(w.word)  # word函数获取词
                        tag_list.append(w.flag)  # flag函数获取词性

            # 词频 dict
            # 在很多使用到dict和次数的场景下，Python中用Counter来实现会非常简洁，效率也会很高
            word_frequency = Counter(word_list) # Counter()来统计每个词出现次数，是个字典形式

            # 筛掉低频词,保留频次大于1的词
            vocab_list = [word for word in word_frequency if word_frequency[word] > self.min_freq]

            # 去掉停用词、违禁词、低频词后，建立word和tag对应id的词典
            # 下面两段还没理解
            for w in vocab_list:
                if w not in word2id:
                    word2id[w] = len(word2id)  # len(word2id)求出word2id元素个数即键的总数
                    id2word[len(id2word)] = w  # len(id2word)求出id2word元素个数即键的总数

            for t in tag_list:
                if t not in tag2id:
                    tag2id[t] = len(tag2id)  # len(tag2id)求出tag2id元素个数即键的总数
                    id2tag[len(id2tag)] = t  # len(id2tag)求出id2tag元素个数即键的总数

            # 将字典存为pkl文件
            dicts = {"word2id":word2id,"id2word":id2word,"tag2id":tag2id,"id2tag":id2tag}
            pkl.dump(dicts,open(self.dict_path,"wb"))
            return

        """
        获取最终结果，为一个list，其中每一项都是固定句长的一行的list，内部分别是word_id和tag_id
        """
        def data2id(self):