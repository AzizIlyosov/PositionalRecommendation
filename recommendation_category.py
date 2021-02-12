# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from keras.models import load_model
#from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import pandas as pd
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
model=load_model('lstm_model.h5')

while (1):
    input_history=input('please input the category history, and the commas should be input between the each category,if you want finish recommendation, please input \'q\':\n')
    if input_history=='q':
        break
    else:
        input_history_array=input_history.split(',')
        category_to_number=[]
        for i in range(4):
            for j in range(n_vocab):
                if input_history_array[i]==category_dictionary.iloc[j][0]:
                    category_to_number.append(str(category_dictionary.iloc[j][1]))
                    break
        test_x=[]
        test_x.append([char_to_int[char] for char in list(category_to_number)])
        test_x=np.reshape(test_x,(1,4,1))    
        test_x=test_x/float(n_vocab)
        predict_result=model.predict(test_x)
        int_result=result_top(predict_result[0],4,char_to_int[category_to_number[-1]])
        char_result=[]
        char_result.append([int_to_char[char] for char in int_result])
        category_result=[]
        for i in range(4):
            for j in range(n_vocab):
                if char_result[0][i]==str(category_dictionary.iloc[j][1]):
                    category_result.append(category_dictionary.iloc[j][0])
        print ('the recommedation result is:\n {}'.format(category_result))
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                