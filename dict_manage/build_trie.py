"""
将词库建立字典树，并存成文件
"""

import json
import pickle


class TrieNode(object):
    """字典树的节点"""

    def __init__(self):
        # 孩子节点用字典进行存储
        self.children = dict()
        # 是否构成一个完成的单词
        self.is_word = False


class Trie(object):
    """字典树"""

    def __init__(self):
        self.root = TrieNode()

    def add(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True

    def search(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_word


if __name__ == '__main__':
    # 读取文件
    read_path = '../dataset/word_list.json'
    file = open(read_path, 'r')
    file_read = file.read()
    file.close()

    # 将词语嵌入到一个字典树中
    word_list = json.loads(file_read)
    trie = Trie()
    for word in word_list:
        trie.add(word)

    # 将对象序列化并存成一个二进制文件
    write_path = '../dataset/trie.pkl'
    with open(write_path, 'wb') as f:
        picklestring = pickle.dump(trie, f)
