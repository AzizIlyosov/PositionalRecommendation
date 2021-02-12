import  pickle
import random

data=[]
with  open('one_company_data_new.txt','r', encoding='utf-8') as dataFile:
  for n, line in enumerate(dataFile):
    data.append([int(i)  for i in line.split(' ')])

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

categoriesDf=pd.read_csv('stuid_categoryid.csv',header=None)
categoriesDf.columns=['userIdCat','categoryid','one2']
data=seriesDf
seriesDf['category']=categoriesDf['categoryid']



# cate_list=[]
# cate_list=[0 for i in range(item_count)]
cat=data.sort_values('seriesid').groupby('seriesid')


for  i in cat:
  cate_list[i[0]]= i[1].reset_index()['category'][0]
cate_count=max(cate_list)+1

jobc_count=2
jobcode_list=[0 for  i in range(user_count)]




with open('datasetCandidate.pkl', 'wb') as f:
  pickle.dump(train_set, f, pickle.HIGHEST_PROTOCOL)
  pickle.dump(test_set, f, pickle.HIGHEST_PROTOCOL)
  pickle.dump(cate_list, f, pickle.HIGHEST_PROTOCOL)
  pickle.dump(jobcode_list, f, pickle.HIGHEST_PROTOCOL)
  pickle.dump((user_count, item_count, cate_count,jobc_count), f, pickle.HIGHEST_PROTOCOL)







