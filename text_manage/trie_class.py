"""
191016
完全抄袭字典树的类，用于读取字典树文件
"""

import re


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
