"""
190920实现双向最大长度匹配算法
"""

import pickle
import json
import datetime

from dict_manage.build_trie import TrieNode, Trie
from text_manage.utils import sentense_extract, seg_encode


# 获得原始文章
read_path = 'dataset/never_forget.txt'
file = open(read_path, 'r')
file_read = file.read()
file.close()

# 获得字典树模型
read_path = 'dataset/trie.pkl'
file = open(read_path, 'rb')
trie = pickle.load(file)
file.close()

# 1. 将原始文章拆分成可以分词的句子
sentense_list = sentense_extract(file_read)

# 2. 使用双向最大长度匹配算法，如果结果一致，保留句子和分词结果
available_sen = []
seg_list = []
for sentense in sentense_list:

    # 计算正向最大长度匹配的分词结果
    forward_res = []
    input = sentense
    # 进行分词，分到字符串为空为止
    while input:
        cut = input
        # 寻找当前剩余部分最大长度的词，找到就进行分割
        while cut:
            # 单字也是一个词语，可分割
            if trie.search(cut) or len(cut) == 1:
                forward_res.append(cut)
                input = input.split(cut, 1)[-1]
                break
            else:
                cut = cut[:-1]

    # 计算反向最大长度匹配的分词结果
    back_res = []
    input = sentense
    # 进行分词，分到字符串为空为止
    while input:
        cut = input
        # 寻找当前剩余部分最大长度的词，找到就进行分割
        while cut:
            # 单字也是一个词语，可分割
            if trie.search(cut) or len(cut) == 1:
                # 确保最先分出来的词排在最后
                back_res.insert(0, cut)
                # 与正向不同，分割后取前面的部分
                split_list = input.split(cut)
                input = cut.join(split_list[:-1])
                break
            else:
                # 长度-1，但与正向方向相反
                cut = cut[1:]

    # 如果正反方向分词结果相同，保留句子和分词结果
    if forward_res == back_res:
        available_sen.append(sentense)
        seg_res = '/'.join(forward_res)
        seg_list.append(seg_res)
        # print('/'.join(forward_res))
        # print('/'.join(back_res))
        # print('-'*50)


# 3. 将分词结果变成编码
code_list = seg_encode(seg_list)

# 4. 整理格式，输出文件
# 逐行写入文件
write_path = 'dataset/never_forget_done.txt'
file = open(write_path, 'w')
for i in range(len(available_sen)):
    sentense = available_sen[i]
    seg_res = seg_list[i]
    code_res = code_list[i]
    write_line = '{}\t{}\t{}'.format(sentense, seg_res, code_res)
    file.write(write_line)
    file.write('\n')
file.close()

# print(len(sentense_list))
# print(len(available_sen))
# print(len(seg_list))
