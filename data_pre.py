from collections import Counter
import pickle as pkl
import os
import jieba.posseg as pseg
import utils

"""
负责清洗数据的类，根据配置删去低频词，停用词，标点符号，空行等等只保留中文文本信息并转化
成对应的id号和词标签id号，固定句长，短补长截。
"""
class DataPre:
    """
    初始化，对应参数分别为：固定句子长度，删去词的词频，补齐的方向，读取word文档的路径
    """
    def __init__(self, sen_len=10, min_freq=1, pad_back=True, file_path="data.txt",dict_path="dicts.pkl"):
        self.sen_len = sen_len
        self.min_freq = min_freq
        self.pad_back = pad_back
        self.file_path = file_path
        self.dict_path = dict_path

        # 读取停用词
        stop_words = set()
        for line in open("stop_words.txt", encoding="UTF-8"):
            stop_words.add(line.strip())
        self.stop_words = stop_words

        # 读取违禁词
        prohibited_words = set()
        for line in open("prohibited_words.txt", encoding="UTF-8"):
            prohibited_words.add(line.strip())
        self.prohibited_words = prohibited_words

    """
    建立word,tag字典
    """
    def create_dicts(self):
        # 中文词word对应id,中文词的词性tag对应id
        word2id, id2word, tag2id, id2tag = {"<pad>":0,"***":1}, {0:"<pad>",1:"***"}, {"<pad>":0,"***":1}, {0:"<pad>",1:"***"}

        # 读取文章
        # 词列表
        word_list = []
        tag_list = []
        for line in open(self.file_path,"r",encoding="UTF-8"):
            line = line.strip()
            content = ""
            for i in line:
                if i >= u'\u4e00' and i <= u'\u9fa5':
                    content += i

            #获取分词及词性
            res = pseg.cut(content)
            for w in res:
                if w.word in self.stop_words:
                    continue
                elif w.word in self.prohibited_words:
                    continue
                else:
                    word_list.append(w.word)
                    tag_list.append(w.flag)

        # 词频 dict
        word_frequency = Counter(word_list)

        # 筛掉低频词
        vocab_list = [word for word in word_frequency if word_frequency[word] > self.min_freq]

        # 建立word 和 tag 对应id的词典
        for w in vocab_list:
            if w not in word2id:
                word2id[w] = len(word2id)
                id2word[len(id2word)] = w

        for t in tag_list:
            if t not in tag2id:
                tag2id[t] = len(tag2id)
                id2tag[len(id2tag)] = t

        #将字典存为pkl文件
        dicts = {"word2id":word2id,"id2word":id2word,"tag2id":tag2id,"id2tag":id2tag}
        pkl.dump(dicts, open(self.dict_path, "wb"))

        return


    """
    获取最终结果，为一个list，其中每一项都是固定句长的一行的list，内部分别是word_id和tag_id
    """
    def data2id(self):
        result = []
        #加载字典
        dicts = self.load_dicts()
        word2id, tag2id = dicts["word2id"], dicts["tag2id"]
        for line in open(self.file_path,"r",encoding="UTF-8"):
            line = line.strip()
            ids, sen=[], ""
            # 去除空行及除中文以外的符号
            if(line == ""):
                continue
            for i in line:
                if i >= u'\u4e00' and i <= u'\u9fa5':
                    sen += i
            #遍历每一句话的词及词性
            res = pseg.cut(sen)
            for w in res:
                # 如果该词为违禁词
                if w.word in self.prohibited_words:
                    ids.append((word2id["***"],tag2id["***"]))
                elif w.word in word2id:
                    ids.append((word2id[w.word],tag2id[w.flag]))
                else:
                    # 这些都是低频词/停用词，不需要处理，直接pass
                    pass

            # 进行长度控制
            ids = utils.pad(ids,self.sen_len,self.pad_back)
            # 添加每个sentence的list到结果的list里面
            result.append(ids)
        return result

    """
    将结果解析回中文词和词性
    """
    def id2data(self,result):
        data = []
        #加载字典
        dicts = self.load_dicts()
        id2word, id2tag = dicts["id2word"], dicts["id2tag"]

        for ids in result:
            data.append([(id2word[word_id],id2tag[tag_id]) for (word_id,tag_id) in ids])
        return data

    """
    加载字典
    """
    def load_dicts(self):
        if os.path.exists(self.dict_path):
            dicts = pkl.load(open(self.dict_path, "rb"))
        else:
            self.create_dicts()
            dicts = pkl.load(open(self.dict_path, "rb"))
        return dicts


if __name__ == "__main__":
    c = DataPre()
    print(c.data2id())
