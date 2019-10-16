"""
项目中需要用到的重要工具
"""

import re
import numpy as np


def get_character_list(file_read):
    """输入已编码的文章，输出按照字频倒序排列的文字列表"""

    # 创建字频字典
    fre_dict = {}
    for line in file_read:
        # 提取句子。编码按照制表符隔开，句子是第一部分
        sentense = line.split('\t')[0]
        for character in sentense:
            if character in fre_dict:
                fre_dict[character] += 1
            else:
                fre_dict[character] = 1

    # 将字典转换为kv元组列表，并按字频倒序排列
    reverse_tup_li = sorted(fre_dict.items(), key=lambda x:x[1], reverse=True)

    # 提取倒序列表中的字，创建文字列表
    character_list = []
    for tup in reverse_tup_li:
        character_list.append(tup[0])

    # 返回文字列表
    return character_list


def get_input_array(file_read, character_list):
    """对文章中的句子进行编码，如果不足32位则补全至32位，如果超出32位则截取至32位"""

    total_sentense = []
    for line in file_read:
        # 提取句子。编码按照制表符隔开，句子是第一部分
        sentense = line.split('\t')[0]

        # 对句子进行编码
        sen_code_list = []
        for character in sentense:
            sen_code_list.append(character_list.index(character))

        # 截取至32位
        sen_code_list = sen_code_list[:32]

        # 补全至32位
        sen_code_list.extend([0] * (32-len(sen_code_list)))

        # 添加进编码列表
        total_sentense.append(sen_code_list)

    # 最后转成numpy数组
    input_array = np.array(total_sentense).astype('float32').reshape(-1, 32, 1)
    return input_array


def get_output_array(file_read):
    """根据文本编码中的第3段，获得输出向量"""

    code_list = []
    for line in file_read:
        # 提取编码
        seg_code = line.split('\t')[2]

        # 截取至32位
        seg_code = seg_code[:32]

        # 补全至32位
        seg_code += '0' * (32-len(seg_code))

        # 进行one-hot编码
        hot_list = []
        for alphabet in seg_code:
            if alphabet == 's':
                hot_list.append([1, 0, 0, 0])
            elif alphabet == 'b':
                hot_list.append([0, 1, 0, 0])
            elif alphabet == 'e':
                hot_list.append([0, 0, 1, 0])
            elif alphabet == 'g':
                hot_list.append([0, 0, 0, 1])
            else:
                hot_list.append([0, 0, 0, 0])

        # 添加进编码列表
        code_list.append(hot_list)

    # 最后转成numpy数组
    output_array = np.array(code_list)

    return output_array
