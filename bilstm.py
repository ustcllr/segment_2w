"""
对输入输出进行编码，并训练bilstm模型
"""

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Bidirectional

from utils import get_character_list, get_input_array, get_output_array


# 获得训练集三段
read_path = 'dataset/managed/never_forget_wuqi_encode.txt'
file = open(read_path, 'r')
file_read_train = file.read().splitlines()
file.close()

# 获得测试集三段
read_path = 'dataset/managed/people2019_01_wuqi_encode.txt'
file = open(read_path, 'r')
file_read_test = file.read().splitlines()
file.close()

# 获得汉字编码列表，要先将两个数据集合并
file_read_concat = file_read_train + file_read_test

# 获得编码列表
character_list = get_character_list(file_read_concat)

# 获得输入输出向量
input_array_train = get_input_array(file_read_train, character_list)[:5]
output_array_train = get_output_array(file_read_train)[:5]
input_array_test = get_input_array(file_read_test, character_list)
output_array_test = get_output_array(file_read_test)

# print(input_array_train.shape)
# print(output_array_train.shape)

# 创建神经网络
model = Sequential()
# 创建双向LSTM网络，反向会自动创建
model.add(Bidirectional(LSTM(10, return_sequences=True)))
model.add(Dense(4, activation='softmax'))

# 配置神经网络的梯度下降算法，成本函数和监控属性
model.compile(
    optimizer='rmsprop',
    loss='categorical_crossentropy',
    metrics=['accuracy']
    )

# 对模型进行训练，自带minibatch和batch-norm功能
model.fit(input_array_train, output_array_train, epochs=20)
model.evaluate(input_array_test, output_array_test)
