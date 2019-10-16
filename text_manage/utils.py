"""
190925
文本处理的支持文件
"""

import re


def sentense_extract(file_read):
    """提取一篇文章中可以用于分词的句子"""

    # 定义句子列表
    sentense_list = [file_read]

    # 按照以下符号，循环进行分割
    punctuation = '\n　！？，。“”（）‘’：；…、《》*,'
    for p in punctuation:
        # 每循环一次，获得新的句子列表
        new_list = []
        for sentense in sentense_list:
            str_list = sentense.split(p)
            new_list.extend(str_list)
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


def get_wuqi_seg(sentense_list, trie):
    """输入句子列表和字典树，返回无歧义句子列表和分词列表"""

    wuqi_sentense_list = []
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

        # 正反方向分词结果相同的句子就是无歧义句子，保留无歧义句子和分词结果
        if forward_res == back_res:
            wuqi_sentense_list.append(sentense)
            seg_res = '/'.join(forward_res)
            seg_list.append(seg_res)

    return wuqi_sentense_list, seg_list


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
