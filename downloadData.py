# -*- coding: utf-8 -*-

from numpy import array
from numpy import argmax  
import pyodbc 
import pandas as pd
from numpy import array
#from tensorflow import keras
#import cv2
import numpy as np
# from sklearn.model_selection import train_test_split

cnxn = pyodbc.connect("Driver={SQL Server};"
                        "Server=14.63.218.34,61433;"
                        "Database=Ubob2015;"
                        "uid=ibmuser;pwd=useribm1234!")
#allData = pd.read_sql_query('select  * from (select  p.Memberid,p.companyid,p.OriRefId as Series, p.CreatedDate,ROW_NUMBER() over(PARTITION BY Memberid order by CreatedDate  ) as \'sequence\',count(*) over(PARTITION BY Memberid  ) as \'count\' from(select OriRefId,Memberid,companyid ,max(OrderForSeries.CreatedDate) as  CreatedDate from  series  join OrderForSeries on series.id = OrderForSeries.SeriesId group by  OrderForSeries.MemberId, Series.OriRefId,series.companyid )p ) t where  t.count>1 and t.count<=50 and  t.companyid=\'290C0136-12DD-4335-8A7E-F3524EECB621\'', cnxn)
#allData = pd.read_sql_query('select id, Title,OrderDate from (select m.id, s.Title, ofs.OrderDate from OrderForSeries ofs, Member m, Series s where m.CompanyId = \'2CD52164-B8EC-4CE4-BC68-3EBD1021D8CB\' and m.Id = ofs.MemberId and ofs.SeriesId = s.Id and ofs.PassStatus =\'Y\') as T  order by id, OrderDate', cnxn) #ofs.OrderDate between \'2017-01-01\' and  \'2017-12-31\'  and
#allData = pd.read_sql_query('select id, Title,CategoryPath,OrderDate from (select m.id, s.Title, ofs.CategoryPath,ofs.OrderDate from OrderForSeries ofs, Member m, Series s where m.CompanyId = \'290C0136-12DD-4335-8A7E-F3524EECB621\' and m.Id = ofs.MemberId and ofs.SeriesId = s.Id and ofs.PassStatus =\'Y\') as T  order by id, OrderDate', cnxn)
#allData = pd.read_sql_query('select id, Title, CASE WHEN CHARINDEX(\'\\\', CategoryPath, 2) > 1 THEN SUBSTRING(CategoryPath, 1, CHARINDEX(\'\\\', CategoryPath, 2) - 1) ELSE CategoryPath END ,OrderDate from (select m.id, s.Title, ofs.CategoryPath,ofs.OrderDate from OrderForSeries ofs, Member m, Series s where m.CompanyId = \'290C0136-12DD-4335-8A7E-F3524EECB621\' and m.Id = ofs.MemberId and ofs.SeriesId = s.Id and ofs.PassStatus =\'Y\') as T  order by id, OrderDate', cnxn) #Category22
#allData=pd.read_sql_query('select id, seriesid, Title,CategoryPath,OrderDate from (select m.id,ofs.SeriesId,s.Title, ofs.CategoryPath,ofs.OrderDate from OrderForSeries ofs, Member m, Series s where m.CompanyId = \'290C0136-12DD-4335-8A7E-F3524EECB621\' and m.Id = ofs.MemberId and ofs.SeriesId = s.Id and ofs.PassStatus =\'Y\') as T  order by id, OrderDate',cnxn) #2CD52164-B8EC-4CE4-BC68-3EBD1021D8CB
# allData=pd.read_sql_query('select id, seriesid, Title,CategoryPath,OrderDate from (select m.id,s.orirefid as  SeriesId,s.Title, ofs.CategoryPath,ofs.OrderDate from OrderForSeries ofs, Member m, Series s where m.Id = ofs.MemberId and ofs.SeriesId = s.Id and ofs.PassStatus =\'Y\') as T  order by id, OrderDate',cnxn)


allData=pd.read_sql_query('SELECT m.Id id, s.Title, s.Id Series, s.OriRefId OriRefId, so.Title as  seriesid, ofs.OrderDate FROM OrderForSeries ofs JOIN Member m ON m.Id=ofs.MemberId  JOIN Company c ON c.Id=m.CompanyId JOIN Series s ON s.Id=ofs.SeriesId JOIN Series so ON so.Id=s.OriRefId LEFT JOIN CategorySeriesRelation csr ON csr.SeriesId=s.OriRefId  LEFT JOIN Category ct ON ct.Id=csr.CategoryId  WHERE m.IsTestUser=\'N\' AND ofs.OrderDate BETWEEN \'2018-01-01\' AND \'2018-12-31 23:59:59\' AND ofs.PassStatus=\'Y\' AND s.OriRefId IN (SELECT OriRefId FROM Series WHERE CompanyId=\'2CD52164-B8EC-4CE4-BC68-3EBD1021D8CB\') ORDER BY m.Id, ofs.OrderDate',cnxn)


'''
for i in range(len(allData)):
    print(i)
    if allData.CategoryPath.loc[i]!=None:
        allData.CategoryPath.loc[i]=allData.CategoryPath.loc[i].split('\\')[1]
'''    

allData.columns=['id', 'Title', 'Series', 'OrirefId', 'Seriesid',  'OrderDate']
# allData.columns = ['id', 'Seriesid', 'Title', 'CategoryPath', 'OrderDate']

members=allData.id.unique().tolist()
series=allData.Seriesid.unique().tolist()
# Category=allData.CategoryPath.unique().tolist()

membersDf=pd.DataFrame({'memIdString':members, 'memIdInt':range(1,len(members)+1)})
seriesDf=pd.DataFrame({'serIdString':series, 'serIdInt':range(1,len(series)+1)})
seriesDf.to_csv('dictionary.csv',index=False)
# print(seriesDf)
# # exit()
# CategoryDf=pd.DataFrame({'cateIdString':Category,'cateIdInt':range(1,len(Category)+1)})
  
new_allData1=pd.merge(membersDf,allData,left_on='memIdString',right_on='id')
new_allData3=pd.merge(new_allData1,seriesDf,left_on='Seriesid',right_on='serIdString',how='left')
# new_allData3=pd.merge(new_allData2,CategoryDf,left_on='CategoryPath',right_on='cateIdString',how='left')


    
new_allData3=pd.DataFrame(new_allData3,columns=['memIdInt','id','Title','serIdInt','OrderDate','rating'])
new_allData3.rating=1
new_allData4=pd.DataFrame(new_allData3,columns=['memIdInt','serIdInt','cateIdInt','rating'])

new_allData5=new_allData4.drop_duplicates(subset=None,keep='first',inplace=False)


data_stuId_serId=new_allData5[['memIdInt','serIdInt','rating']]
data_stuId_CategoryId=new_allData5[['memIdInt','cateIdInt','rating']]
#data_stuId_serId.to_csv("orginal_data.csv",index=False,header=False)
data_stuId_serId.to_csv("stuid_stuserid.csv",index=False,header=False)

#print(data_stuId_serId)
#exit()

#for i in range():
    
    
#
# result=[]
# value_list=[]
#
#
# for i in range(len(data_stuId_CategoryId)-1):
#     print(i)
#     value_list.append(data_stuId_CategoryId.iloc[i].cateIdInt)
#     if data_stuId_CategoryId.iloc[i].memIdInt+1==data_stuId_CategoryId.iloc[i+1].memIdInt:
#         result.append(value_list)
#         value_list=[]
# '''
# new_allData2=pd.DataFrame(new_allData2,columns=['memIdInt','memIdString','id','Title','OrderDate','serIdInt','serIdString','rating'])
# new_allData2.rating=1
# new_allData2[['memIdInt','serIdInt','rating']].to_csv("data.csv",index=False,header=False)
# '''
#
# file=open('stuid_categoryid_new.txt','a')
# for i in range(len(result)):
#     s=str(result[i]).replace('[','').replace(']','')
#     s=s.replace('{','').replace('}','').replace(',','')+'\n'
#     file.write(s)
# file.close()


##############MAKE TXT FILE  ######################

import  pandas  as  pd

df=pd.read_csv('stuid_stuserid.csv',header=None,delim_whitespace=False)
#print('this is  df \n',df)
df.columns=['userid','itemid','one']
max1=df.userid.max()
print(max1 )
# exit()
users=[[] for i in range(max1)]


data=[]
with open('stuid_stuserid.csv', 'r') as f:
    for  line  in f:
        data= ([int(i) for i in line.split(',')])
        users[data[0]-1].append(data[1])
# print(users)


with open('one_company_data_new.txt','w') as f:
    for l,el in enumerate(users):
        #print(el)

        string = ' '.join(map(str,el))
        #print(str(el))
        #exit()
        #f.write(str(el))
        for item in string:
            f.write(item)
        f.write('\n')
################################################################




#################  BUILD  DATASET ##############################

del data
import  pickle
import random

data=[]
# print(max([1,2,3,4,5,6,56,78,23]))
with  open('one_company_data_new.txt','r', encoding='utf-8') as dataFile:
  for n, line in enumerate(dataFile):
    data.append([int(i) for i in line.split(' ')])

#
# for i in data:
#     print(type(i[0]))
#     print(max(i))


item_count=max([max(i) for i in data])+1
user_count=len(data)
test_set=[]
train_set=[]

for n, line in enumerate(data):
  if(len(line)<2):continue
  userId=n
  def gen_neg():
    neg = line[0]
    while neg in line:
      neg = random.randint(0, item_count - 1)
    return neg


  neg_list = [gen_neg() for i in range(len(line))]

  if n<=user_count*0.2:
    hist=line[0:len(line)-1]
    pred=line[-1]
    test_set.append([userId,hist,(pred,neg_list[-1])])

    line=line[0:len(line)-1]
    neg_list=neg_list[0:len(neg_list)-1]

  while(len(line)>=2):
    hist = line[0:len(line) - 1]
    pred = line[-1]
    train_set.append([userId, hist, (pred,neg_list[-1])])
    line = line[0:len(line) - 1]
    neg_list = neg_list[0:len(neg_list) - 1]


random.shuffle(train_set)
random.shuffle(test_set)

import  pandas  as pd

seriesDf    =pd.read_csv('stuid_stuserid.csv',header=None)
seriesDf.columns=['userid','seriesid','one']
item_count=max(seriesDf['seriesid'])+1

data=seriesDf



jobc_count=2
jobcode_list=[0 for  i in range(user_count)]




with open('datasetCandidate.pkl', 'wb') as f:
  pickle.dump(train_set, f, pickle.HIGHEST_PROTOCOL)
  pickle.dump(test_set, f, pickle.HIGHEST_PROTOCOL)
  pickle.dump(jobcode_list, f, pickle.HIGHEST_PROTOCOL)
  pickle.dump((user_count, item_count, jobc_count), f, pickle.HIGHEST_PROTOCOL)




###############################
