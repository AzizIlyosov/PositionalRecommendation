# -*- coding: utf-8 -*-

import  pandas  as pd
import pickle
import random
import numpy as np
import tensorflow as tf
from candidateModel import CandidateModel
from input import DataInput, DataInputTest

import numpy as np
from keras.models import Sequential
from keras.models import load_model
random.seed(1234)
np.random.seed(1234)
tf.set_random_seed(1234)

with open('datasetCandidate.pkl', 'rb') as f:
    train_set = pickle.load(f)
    test_set = pickle.load(f)
    jobcode_list = pickle.load(f)
    (user_count, item_count, jobc_count) = pickle.load(f)


def getUIJ_for_1(j):
    data = ([j[0]],  # UserId
            [j[2][0]],  # i
            [j[2][1]],  # j
            [j[1]],  # History
            [len(j[1])]
            )
    return data


def getUIJ_for_hist(j):
    data = ([0],  # UserId
            [0],  # i
            [0],  # j
            [j],  # History
            [len(j)]
            )
    return data


train_batch_size = 32
test_batch_size = 512
best_auc = 0.0


dictionary=pd.read_csv('oriref_dictionary.csv', header=None)
#'serIdString' 'serIdInt'
nump=np.array(dictionary)

classname_ID_dict={}
classname_ID_dictRev={}
for i in nump:
    classname_ID_dict.update({i[0]:i[1]})
    classname_ID_dictRev.update({i[1]:i[0]})
#testLength=len(test_set)
    
    
orirefid_cateid_dictionary=pd.read_csv('orirefid_cateid_dictionary.csv', header=None)
#'serIdString' 'serIdInt'
orirefid_cateid_dictionary_nump=np.array(orirefid_cateid_dictionary)

orirefid_cateid_dict={}
cateid_orirefid_dictRev={}
for i in orirefid_cateid_dictionary_nump:
    orirefid_cateid_dict.update({i[0]:i[1]})
#    cateid_orirefid_dictRev.update({i[1]:i[0]})




###################################################################
def result_top(input_array,n,last_category):
    result=[]
    result.append(last_category)
    input_array[last_category]=0
    for i in range(n-1):
        top=np.argmax(input_array)
        input_array[top]=0
        result.append(top)   
    return result

fr_read_char_to_int=open('char_to_int.txt','r+')
char_to_int=eval(fr_read_char_to_int.read())
fr_read_char_to_int.close()
fr_read_int_to_char=open('int_to_char.txt','r+')
int_to_char=eval(fr_read_int_to_char.read())
fr_read_int_to_char.close()

category_dictionary=pd.read_csv('category_dictionary.csv',header=None)
seq_length=4
x=[]
y=[]
n_vocab=len(category_dictionary)


model=Sequential()


###################################################################





with  tf.Session() as  sess:
    candiModel = CandidateModel(user_count, item_count,  jobc_count, jobcode_list, batchsize=32)
    sess.run(tf.global_variables_initializer())
    sess.run(tf.local_variables_initializer())
    candiModel.restore(sess, 'SavePathCandidate/candModel')
    
    
    while(1):
        print('Please  Input  history  of  the  member\n !Note  pls split name  of  courses by \'::\' not  by  space !   ')
        a = input()
        a_slilt=a.split('::')
        
        memHist= [classname_ID_dict[i] for i in a.split('::') if i in classname_ID_dict.keys()]
        if len(memHist)<4:
            print('the input effective history length should be more than 4')
            continue
        
        memHist_last=memHist[-4:]
        
        category_ID=[orirefid_cateid_dict[i] for i in memHist_last]
        #################################################################
        test_x=[]
        test_x.append([char_to_int[str(char)] for char in category_ID])
        test_x=np.reshape(test_x,(1,4,1))    
        test_x=test_x/float(n_vocab)
        model=load_model('lstm_model.h5')
        predict_result=model.predict(test_x)
        
        
        int_result=result_top(predict_result[0],4,char_to_int[str(category_ID[-1])])
        
        category_id_result=[]
        category_id_result.append([int_to_char[char] for char in int_result])
#        print('recommendation category result {}'.format(category_id_result[0]))
        
        
        #################################################################
        
        
        
        
        
        
#        print('input the history: {}'.format(memHist))
#        print('recommendation categoyr id: {}'.format(category_ID))
        cands = candiModel.predict(sess, getUIJ_for_hist(memHist))
        
        recommendation_result=[]
        a=np.zeros(20)


        for i in cands[0]:
            if i in memHist:
                continue
            else:
                if len(category_id_result[0])>0:
                    if str(orirefid_cateid_dict[i]) in category_id_result[0]:
                        recommendation_result.append(i)
                        a[orirefid_cateid_dict[i]]=a[orirefid_cateid_dict[i]]+1
                        if a[orirefid_cateid_dict[i]]==2:
                            category_id_result[0].remove(str(orirefid_cateid_dict[i]))
                else:
                    break
#        print('recommendation result: {}'.format(recommendation_result))
        print('Recommending  Item:')
        for m in range(len(recommendation_result)):
            print(classname_ID_dictRev.get(recommendation_result[m]))   
            
#        print('Recommending  Item:'.format(classname_ID_dictRev.get(recommendation_result[0]),classname_ID_dictRev.get(recommendation_result[1]),classname_ID_dictRev.get(recommendation_result[2]),classname_ID_dictRev.get(recommendation_result[3])))
        print('If you want to quit clik q :')
        print('If  you want to continue click  any key')
        option= input()
        if option=="q" or option=="Q":
            print('------------------------')
            exit(2)



