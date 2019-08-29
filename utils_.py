"""
describe:
@project: 智能广告项目
@author: Jony
@create_time: 2019-07-09 12:21:10
@file: dd.py
"""

import jieba
import matplotlib.pyplot as plt

"""
1. 固定句子长度，如果大于阈值就截掉，小于阈值则<pad>补齐。
2. 输入为一句话对应的词语与词性id
"""

def pad(x, sen_len, pad_back):
    x_len = len(x)
    # 句子长度大于阈值
    if x_len >= sen_len:
        return x[:sen_len]
    # 句子小于阈值
    else:
        if pad_back:
            # extend() 函数用于在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
            # id不变
            x.extend([(0,0)] * (sen_len - x_len))
        else:
            x = [(0,0)] * (sen_len - x_len) + x  # 和extend()函数功能一样，但是id会改变
    return x

"""
显示数据总体句子长度的情况
"""
def show_lens(file_path):
    lens = []  # 建一个列表放置分句后的句子长度
    for line in open(file_path,"r",encoding="utf-8"):
        words = jieba.lcut(line)  # 精确模式，返回一个列表类型，建议使用
        lens.append(len(words))
    plt.figure()  # 创建一个图形实例
    plt.plot(lens)
    plt.ylabel("Length of sentences")
    plt.show()

# 程序入口
if __name__=="__main__":
    show_lens("data.txt")