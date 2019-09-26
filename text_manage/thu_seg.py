"""
190924
使用清华分词，将句子转换为斜杠分割的词语
对于政治类，清华分词的结果确实优于结巴分词
"""

import thulac


# 读取文件
read_path = '../dataset/people_2019/t2_ori.txt'
file = open(read_path, 'r')
read_lines = file.read().splitlines()
file.close()

# 创建一个只进行分词的分词器
seg_handler = thulac.thulac(seg_only=True)

# 循环对句子进行分词
seg_list = []
for sentense in read_lines:
    # 获得分词文本
    text = seg_handler.cut(sentense, text=True)
    # 改成斜杠分割
    seg_res = '/'.join(text.split(' '))
    seg_list.append(seg_res)

# 逐行写入文件
write_path = '../dataset/people_2019/t2_seg.txt'
file = open(write_path, 'w')
for seg in seg_list:
    file.write(seg)
    file.write('\n')
file.close()
