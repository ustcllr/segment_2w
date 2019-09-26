"""
190925
文本处理的支持文件
"""

import re


def sentense_extract(article):
    """提取一篇文章中可以用于分词的句子"""

    # 定义句子列表
    sentense_list = [article]

    # 按照以下符号，循环进行分割
    punctuation = '\n　！？，。“”（）：；…、《》*'
    for p in punctuation:
        # 每循环一次，获得新的句子列表
        new_list = []
        for sentense in sentense_list:
            str_list = sentense.split(p)
            new_list += str_list
        sentense_list = new_list

    # 去除相同的句子
    sentense_list = list(set(sentense_list))

    # 去除长度小于2和包含数字的句子
    new_list = []
    for sentense in sentense_list:
        if len(sentense) < 2 or re.match('.*\d', sentense):
            pass
        else:
            new_list.append(sentense)

    return new_list


def seg_encode(seg_list):
    """将分词结果转换为4分类编码"""

    code_list = []
    for seg in seg_list:
        # 将句子按照分词符号隔开，变成一个个词语
        word_list = seg.split('/')

        # 进行编码
        seg_code = ''
        for word in word_list:
            if len(word) == 1:
                seg_code += 's'
            elif len(word) == 2:
                seg_code += 'be'
            else:
                seg_code += 'b' + (len(word)-2)*'m' + 'e'

        code_list.append(seg_code)

    return code_list
