import jieba
import matplotlib.pyplot as plt


"""
固定句长函数，如果这个句子长度大于规定句长则截断，如不足就补齐<pad>
输入为一句话对应的词语及词性id
"""
def pad(x, sen_len,pad_back):
    x_len = len(x)
    if (x_len >= sen_len):
        return x[:sen_len]
    else:
        # 添加<pad>的id 和 tag_id
        if pad_back:
            x.extend([(0, 0)] * (sen_len - x_len))
        else:
            x = [(0, 0)] * (sen_len - x_len) + x
    return x

"""
显示数据总体的句子长度情况
"""
def show_lens(file_path):
    lens = []
    for line in (open(file_path, "r", encoding="UTF-8")):
        words = jieba.lcut(line)
        lens.append(len(words))
    plt.figure()
    plt.plot(lens)
    plt.ylabel("length of sentences")
    plt.show()

if __name__ == "__main__":
    show_lens("data.txt")
