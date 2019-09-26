"""
将词库处理成列表，去除单字，英文，数字，繁体字
"""

import json
import re


# 读取文件
read_path = '../dataset/jb_60w.txt'
file = open(read_path, 'r')
read_lines = file.read().splitlines()
file.close()

# 1. 字符串处理
# 定义一个变量，用于记录处理进度
manage_num = 0
# 190925习惯要好，不要删除循环中的元素
word_list = []

for word in read_lines:
    # 优先统计处理进度
    manage_num += 1
    if manage_num % 10000 == 0:
        print('manage_num =', manage_num)

    # 长度小于2，或者包含字母数字，就从词库中移除
    if len(word) <= 1 or len(word) >= 8 or re.match('.*[A-Za-z0-9]', word):
        continue

    # 如果包含繁体字，也移除
    try:
        word.encode('big5hkscs')
    except:
        continue

    word_list.append(word)

print('word_list__length =', len(word_list))

# 2. 输出成JSON文件
write_json = json.dumps(read_lines)
write_path = '../dataset/word_list.json'
file = open(write_path, 'w')
file.write(write_json)
file.close()
