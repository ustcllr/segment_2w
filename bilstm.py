"""
将元数据转换为输入输出向量，并训练bilstm+CRF模型
"""

import numpy as np
# 191028从今天起，为了keras的扩展性，不再使用原生TF的模块
from keras.models import Sequential
from keras.layers import Dense, LSTM, Bidirectional
from keras_contrib.layers import CRF
from keras_contrib.losses import crf_loss
from keras_contrib.metrics import crf_viterbi_accuracy

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
input_array_train = get_input_array(file_read_train, character_list)
output_array_train = get_output_array(file_read_train)
input_array_test = get_input_array(file_read_test, character_list)
output_array_test = get_output_array(file_read_test)

# 创建神经网络
model = Sequential()
# 创建双向LSTM网络，反向会自动创建
# 由于加了CRF后学习能力很强，所以这里10个单元就够了
model.add(Bidirectional(LSTM(10, return_sequences=True)))
# 创建CRF层，特征函数和转移概率会自动根据训练数据计算
# 如果使用了one-hot，那就必须设置sparse_target
model.add(CRF(4, sparse_target=True))
# model.add(Dense(4, activation='softmax'))

# 配置神经网络的梯度下降算法，成本函数和监控属性
model.compile(
    optimizer='rmsprop',
    loss=crf_loss,
    metrics=[crf_viterbi_accuracy]
    )

# 对模型进行训练，自带minibatch和batch-norm功能
# 由于CRF有明确的约束条件，所以模型的学习速度很快，10个纪元就完全足够了
model.fit(input_array_train, output_array_train, epochs=10)

# 通过测试集，验证模型的预测能力
loss, accuracy = model.evaluate(input_array_test, output_array_test)
print('\n' + '-' * 70)
print('crf_loss =', loss)
print('crf_viterbi_accuracy =', accuracy)
