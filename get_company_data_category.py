from numpy import array
from numpy import argmax  
import pyodbc 
import pandas as pd
from numpy import array
#from tensorflow import keras
#import cv2
import numpy as np
from sklearn.model_selection import train_test_split

cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=14.63.218.34,61433;"
                        "Database=Ubob2015;"
                        "uid=ibmuser;pwd=useribm1234!")
#allData = pd.read_sql_query('select  * from (select  p.Memberid,p.companyid,p.OriRefId as Series, p.CreatedDate,ROW_NUMBER() over(PARTITION BY Memberid order by CreatedDate  ) as \'sequence\',count(*) over(PARTITION BY Memberid  ) as \'count\' from(select OriRefId,Memberid,companyid ,max(OrderForSeries.CreatedDate) as  CreatedDate from  series  join OrderForSeries on series.id = OrderForSeries.SeriesId group by  OrderForSeries.MemberId, Series.OriRefId,series.companyid )p ) t where  t.count>1 and t.count<=50 and  t.companyid=\'290C0136-12DD-4335-8A7E-F3524EECB621\'', cnxn)
#allData = pd.read_sql_query('select id, Title,OrderDate from (select m.id, s.Title, ofs.OrderDate from OrderForSeries ofs, Member m, Series s where m.CompanyId = \'2CD52164-B8EC-4CE4-BC68-3EBD1021D8CB\' and m.Id = ofs.MemberId and ofs.SeriesId = s.Id and ofs.PassStatus =\'Y\') as T  order by id, OrderDate', cnxn) #ofs.OrderDate between \'2017-01-01\' and  \'2017-12-31\'  and
#allData = pd.read_sql_query('select id, Title,CategoryPath,OrderDate from (select m.id, s.Title, ofs.CategoryPath,ofs.OrderDate from OrderForSeries ofs, Member m, Series s where m.CompanyId = \'290C0136-12DD-4335-8A7E-F3524EECB621\' and m.Id = ofs.MemberId and ofs.SeriesId = s.Id and ofs.PassStatus =\'Y\') as T  order by id, OrderDate', cnxn)
#allData = pd.read_sql_query('select id, Title, CASE WHEN CHARINDEX(\'\\\', CategoryPath, 2) > 1 THEN SUBSTRING(CategoryPath, 1, CHARINDEX(\'\\\', CategoryPath, 2) - 1) ELSE CategoryPath END ,OrderDate from (select m.id, s.Title, ofs.CategoryPath,ofs.OrderDate from OrderForSeries ofs, Member m, Series s where m.CompanyId = \'290C0136-12DD-4335-8A7E-F3524EECB621\' and m.Id = ofs.MemberId and ofs.SeriesId = s.Id and ofs.PassStatus =\'Y\') as T  order by id, OrderDate', cnxn) #Category22
#allData=pd.read_sql_query( 'select  id, Title,SeriesId, CASE WHEN CHARINDEX(\'\\\', CategoryPath, 2) > 1 THEN SUBSTRING(CategoryPath, 1, CHARINDEX(\'\\\', CategoryPath, 2) - 1) ELSE CategoryPath END ,OrderDate from (select m.id, s.Title,ofs.SeriesId, ofs.CategoryPath,ofs.OrderDate from OrderForSeries ofs, Member m, Series s where m.CompanyId = \'2CD52164-B8EC-4CE4-BC68-3EBD1021D8CB\' and m.Id = ofs.MemberId and ofs.SeriesId = s.Id and ofs.PassStatus =\'Y\') as T  order by id, OrderDate',cnxn) # 2CD52164-B8EC-4CE4-BC68-3EBD1021D8CB first Category
allData=pd.read_sql_query( 'select id,CompanyId, Title,SeriesId, CASE WHEN CHARINDEX(\'\\\', CategoryPath, 2) > 1 THEN SUBSTRING(CategoryPath, 1, CHARINDEX(\'\\\', CategoryPath, 2) - 1) ELSE CategoryPath END ,OrderDate from (select m.id,m.CompanyId, s.Title,s.orirefid as SeriesId, ofs.CategoryPath,ofs.OrderDate from OrderForSeries ofs, Member m, Series s where  m.Id = ofs.MemberId and ofs.SeriesId = s.Id and ofs.PassStatus =\'Y\') as T  order by id, OrderDate',cnxn)


#allData=pd.read_sql_query('select id, seriesid, Title,CategoryPath,OrderDate from (select m.id,ofs.SeriesId,s.Title, ofs.CategoryPath,ofs.OrderDate from OrderForSeries ofs, Member m, Series s where m.CompanyId = \'290C0136-12DD-4335-8A7E-F3524EECB621\' and m.Id = ofs.MemberId and ofs.SeriesId = s.Id and ofs.PassStatus =\'Y\') as T  order by id, OrderDate',cnxn) #bigest company
#allData=pd.read_sql_query('select id, seriesid, Title,CategoryPath,OrderDate from (select m.id,ofs.SeriesId,s.Title, ofs.CategoryPath,ofs.OrderDate from OrderForSeries ofs, Member m, Series s where m.CompanyId = \'2CD52164-B8EC-4CE4-BC68-3EBD1021D8CB\' and m.Id = ofs.MemberId and ofs.SeriesId = s.Id and ofs.PassStatus =\'Y\') as T  order by id, OrderDate',cnxn)
'''
for i in range(len(allData)):
    print(i)
    if allData.CategoryPath.loc[i]!=None:
        allData.CategoryPath.loc[i]=allData.CategoryPath.loc[i].split('\\')[1]
'''    
allData.columns = ['MemberId','CompanyId','SeriesTitle', 'SeriesId', 'FirstCategory', 'OrderDate']

Members_Id=allData.MemberId.unique().tolist()
Company_Id=allData.CompanyId.unique().tolist()
Series_Id=allData.SeriesId.unique().tolist()
Series_Title=allData.SeriesTitle.unique().tolist()
First_Category=allData.FirstCategory.unique().tolist()

membersDf=pd.DataFrame({'memIdString':Members_Id, 'memIdInt':range(1,len(Members_Id)+1)})
companyDf=pd.DataFrame({'companyIdString':Company_Id,'comIdInt':range(1,len(Company_Id)+1)})
seriesDf=pd.DataFrame({'serIdString':Series_Id, 'serIdInt':range(1,len(Series_Id)+1)})
FirstCategoryDf=pd.DataFrame({'cateIdString':First_Category,'cateIdInt':range(1,len(First_Category)+1)})
seriesDf.to_csv('series_dictionary.csv',index=False,header=False)
FirstCategoryDf.to_csv('firstCategory_dictionary.csv',index=False,header=False)  
new_allData1=pd.merge(allData,membersDf,left_on='MemberId',right_on='memIdString',how='left')
new_allData2=pd.merge(new_allData1,seriesDf,left_on='SeriesId',right_on='serIdString',how='left')

new_allData3=pd.merge(new_allData2,FirstCategoryDf,left_on='FirstCategory',right_on='cateIdString',how='left')


    
#new_allData3=pd.DataFrame(new_allData3,columns=['MemberId','SeriesTitle','SeriesId','FirstCategory','cateIdInt','rating'])
new_allData3['rating']=1
new_allData4=pd.DataFrame(new_allData3,columns=['memIdInt','serIdInt','cateIdInt','rating'])

new_allData5=new_allData4.drop_duplicates(subset=None,keep='first',inplace=False)


data_stuId_serId=new_allData5[['memIdInt','serIdInt','rating']]
data_stuId_CategoryId=new_allData5[['memIdInt','cateIdInt','rating']]
#data_stuId_serId.to_csv("orginal_data.csv",index=False,header=False)
data_stuId_serId.to_csv("stuid_stuserid.csv",index=False,header=False)
data_stuId_CategoryId.to_csv("stuid_categoryid.csv",index=False,header=False)

#for i in range():
    
    

result=[]
value_list=[]


for i in range(len(data_stuId_CategoryId)-1):
    print(i)
    value_list.append(data_stuId_CategoryId.iloc[i].cateIdInt)
    if data_stuId_CategoryId.iloc[i].memIdInt+1==data_stuId_CategoryId.iloc[i+1].memIdInt:
        result.append(value_list)
        value_list=[]
'''       
new_allData2=pd.DataFrame(new_allData2,columns=['memIdInt','memIdString','id','Title','OrderDate','serIdInt','serIdString','rating'])
new_allData2.rating=1
new_allData2[['memIdInt','serIdInt','rating']].to_csv("data.csv",index=False,header=False)
'''       
     
file=open('stuid_categoryid_new.txt','a')
for i in range(len(result)):
    s=str(result[i]).replace('[','').replace(']','')
    s=s.replace('{','').replace('}','').replace(',','')+'\n'
    file.write(s)
file.close()