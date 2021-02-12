# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
dictionary=pd.read_csv('oriref_dictionary.csv', header=None)
#'serIdString' 'serIdInt'
nump=np.array(dictionary)

classname_ID_dict={}
classname_ID_dictRev={}
for i in nump:
#    classname_ID_dict.update({i[0]:i[1]})
    classname_ID_dictRev.update({i[1]:i[0]})
in_ID=input()

in_ID_split=[classname_ID_dictRev[int(i)] for i in in_ID.split()]
print(in_ID_split)

file=open('test.txt','a')
for i in in_ID_split:
    print(i)   
    file.write(i+"::")
file.write('\n')
file.close()