import warnings
warnings.filterwarnings('ignore')


import os
import time
import pickle
import random
import numpy as np
import tensorflow as tf
from  candidateModel import CandidateModel
from input import DataInput, DataInputTest
import warnings
warnings.filterwarnings('ignore')
random.seed(1234)
np.random.seed(1234)
tf.set_random_seed(1234)


tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


with open('datasetCandidate.pkl', 'rb') as f:
    train_set =    pickle.load(f)
    test_set =     pickle.load(f)
    jobcode_list = pickle.load(f)
    (user_count, item_count,  jobc_count)= pickle.load(f)


length=len(train_set)
print('Count of  Items: ',item_count)
print('length of testing  data: ',length)

# exit()

train_batch_size   = 32
test_batch_size    = 512

config = tf.ConfigProto(
        device_count = {'GPU': 0}
    )
print('lenght  of  testing  data: ',len(test_set))
with  tf.Session(   ) as  sess:
    candiModel=CandidateModel(user_count, item_count, jobc_count,jobcode_list, batchsize=32)
    sess.run(tf.global_variables_initializer())
    sess.run(tf.local_variables_initializer())


    for epoch in range(50):

        random.shuffle(train_set)

        epoch_size = round(len(train_set) / train_batch_size)
        loss_sum = 0.0
        for _, uij in DataInput(train_set, train_batch_size):
            loss = candiModel.train(sess, uij)
            loss_sum += loss
        print('epoch', epoch,  'loss:', loss_sum / len(train_set))
        acc1=acc5=acc10=0
        for  _, uij in DataInputTest(test_set, train_batch_size):
            acc=candiModel.eval(sess, uij)
            acc1+=acc[0]
            acc5+=acc[1]
            acc10+=acc[2]
        print('acc1 ', acc1/len(test_set), ' acc5: ', acc5/(len(test_set) *5), 'acc10:' ,acc10/(len(test_set)*10))

        if  epoch==24:
            candiModel.save(sess,'SavePathCandidate/candModel')
            exit()

