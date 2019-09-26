"""
190918对比字典树和列表，哪一个读取速度快
"""

import pickle
import json
import datetime

from build_trie import TrieNode, Trie


# 从文件中获得字典树对象
read_path = '../dataset/trie.pkl'
file = open(read_path, 'rb')
trie = pickle.load(file)
file.close()

# 从文件中获得词语列表，用于做速度对比
read_path = '../dataset/word_list.json'
file = open(read_path, 'r')
file_read = file.read()
word_list = json.loads(file_read)
file.close()

# 创建测试数据列表，由原列表中，每40个位置取一个词
test_word = word_list[::40]

# 打印字典树方法delta
t1 = datetime.datetime.now()
for word in test_word:
    trie.search(word)
t2 = datetime.datetime.now()
delta = t2 - t1
print(delta)

# 打印列表方法delta
t1 = datetime.datetime.now()
for word in test_word:
    word in word_list
t2 = datetime.datetime.now()
delta = t2 - t1
print(delta)
