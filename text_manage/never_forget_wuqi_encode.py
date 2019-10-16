"""
对不忘初心，牢记使命双向匹配相同的句子进行编码，作为无歧义句子的训练集
"""

import pickle

from trie_class import TrieNode, Trie
from utils import sentense_extract, get_wuqi_seg, seg_encode


# 获得字典树模型
read_path = '../dataset/dict_and_model/trie.pkl'
file = open(read_path, 'rb')
trie = pickle.load(file)
file.close()

# 获得原始文章
read_path = '../dataset/origin/never_forget.txt'
file = open(read_path, 'r')
file_read = file.read()
file.close()

# 1. 将原始文章拆分成可以分词的句子
sentense_list = sentense_extract(file_read)

# 2. 使用双向最大长度匹配算法，如果结果一致，保留句子和分词结果
wuqi_sentense_list, seg_list = get_wuqi_seg(sentense_list, trie)

# 3. 将分词结果变成编码
code_list = seg_encode(seg_list)

# 4. 整理格式，输出文件
# 逐行写入文件
write_path = '../dataset/managed/never_forget_wuqi_encode.txt'
file = open(write_path, 'w')
for i in range(len(wuqi_sentense_list)):
    sentense = wuqi_sentense_list[i]
    segment = seg_list[i]
    seg_code = code_list[i]
    write_line = '{}\t{}\t{}'.format(sentense, segment, seg_code)
    file.write(write_line)
    file.write('\n')
file.close()
