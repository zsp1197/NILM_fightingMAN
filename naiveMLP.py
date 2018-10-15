import pandas as pd
import tensorflow as tf
import numpy as np
from tensorflow.contrib import rnn
from NILM.Batch import Batch
import os

file_name=os.path.basename(__file__)
file_name=file_name.split('.')[0]
summary_path='/home/uftp/zhai/python/summary4tf/'
# redd_hdf5 = 'D:\SJTU\\NILMcode\python2test\\nilmtk_use\wtf.hdf5'
redd_hdf5 = '/home/uftp/zhai/data/wtf.hdf5'

redd_store = pd.HDFStore(redd_hdf5)
batch = Batch(redd_store)

batch_dict = {'fridge': 20, 'light': 25, 'microwave': 30, 'dish washer': 30, 'electric stove': 20}
batch_size = 0
n_classes = len(batch_dict)
for (name, num) in batch_dict.items():
    batch_size = batch_size + num
appliance_series_length = 12000
time_step = 40
learning_rate = 0.1
n_hidden = time_step
input_size = appliance_series_length / time_step
total_step = 100
# 判断是否为整数
if (not input_size.is_integer()):
    raise LookupError
input_size = int(input_size)
cell_size = input_size

x = tf.placeholder(dtype=tf.float32, shape=[batch_size, appliance_series_length])
y = tf.placeholder(dtype=tf.float32, shape=[batch_size, n_classes])

# each member is organized as:(name,num of units,activation function)
hidden_layers=[('hidden_1',8000,None),('hidden_2',4000,None),('hidden_3',1000,None)]

weights={}
biases={}

lastlayer=appliance_series_length
for i,var in enumerate(hidden_layers):
    with tf.name_scope(var[0]):
        weights.update({var[0]:tf.Variable(tf.random_normal([lastlayer,var[1]]))})
        biases.update({var[0]:tf.random_normal([var[1]])})
        lastlayer=var[1]
        tf.summary.histogram('MLP_weight%d'%(i+1),weights[var[0]])
        tf.summary.histogram('MLP_bias%d'%(i+1),biases[var[0]])

xx=[x]
for i,var in enumerate(hidden_layers):
    xx.append(tf.matmul(xx[-1],weights[var[0]])+biases[var[0]])
    if(var[2]!=None):
        xx[-1]=var[2](xx[-2])

with tf.name_scope('MLP_outlayer'):
    weight_out=tf.Variable(tf.random_normal([hidden_layers[-1][1],n_classes]),name='weight')
    bias_out=tf.Variable(tf.random_normal([n_classes]),name='bias')
    pred=tf.matmul(xx[-1],weight_out)+bias_out

with tf.name_scope('cost'):
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
    tf.summary.scalar('cost',cost)

with tf.name_scope('optimize'):
    optimizer=tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
    # Evaluate model
    correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
tf.summary.scalar('accuracy',accuracy)



config=tf.ConfigProto(log_device_placement=True,allow_soft_placement=True)
config.gpu_options.allow_growth = True
with tf.Session(config=config) as sess:
    writter=tf.summary.FileWriter(summary_path+file_name,sess.graph)
    merged = tf.summary.merge_all()
    sess.run(tf.global_variables_initializer())
    for step in range(0,total_step):
        batch_x, batch_y = batch.next_batch(batch_dict, length=appliance_series_length)
        feed_dict = {x: batch_x, y: batch_y}
        result, _ = sess.run([merged, optimizer], feed_dict=feed_dict)
        loss, accc = sess.run([cost, accuracy], feed_dict=feed_dict)
        writter.add_summary(result,step)
        print(accc)
