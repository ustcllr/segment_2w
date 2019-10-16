"""
本项目原始词库使用jieba+baidu的63W词
本脚本对词库进行处理，去除单字，英文，数字，繁体字
处理后有44W词
再输出成JSON
"""

import json
import re


# 读取文件
read_path = '../dataset/dict_and_model/jb_bd_63w.txt'
file = open(read_path, 'r')
read_lines = file.read().splitlines()
file.close()

# 1. 字符串处理
# 定义一个变量，用于记录处理进度
manage_num = 0
# 190925一定不要删除循环中的元素，否则会大大降低运行速度
word_list = []

for word in read_lines:
    # 优先统计处理进度
    manage_num += 1
    if manage_num % 10000 == 0:
        print('manage_num =', manage_num)

    # 长度不合适，或者包含字母数字，就从词库中移除
    if len(word) < 2 or len(word) > 8 or re.match('.*[A-Za-z0-9]', word):
        continue

    # 191016由于去除繁体字经常误杀，所以暂时关闭这个功能
    # try:
    #     word.encode('big5hkscs')
    # except:
    #     continue

    word_list.append(word)

print('word_list__length =', len(word_list))

# 2. 输出成JSON文件
write_json = json.dumps(word_list)
write_path = '../dataset/dict_and_model/word_list.json'
file = open(write_path, 'w')
file.write(write_json)
file.close()
