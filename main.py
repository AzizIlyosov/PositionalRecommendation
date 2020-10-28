from models.youtube_candidate_gen import model as youtubeModel

class main:
    '''
    In this model we will candidate  generation part of
    Deep Neural Networks for YouTube Recommendations paper
    '''
    def __init__(self, history ,features  ):
        '''

        history :  dict type variable:
            key show  user id while value (list)  shows item id's
            [
                {
                    'id':2,# this should be higher  than 1
                    'hist':[2,3,4],
                    'cat_feature1':[1,3], #for example job [programmer , data scientist]
                    'cat_feature2': ...
                    'continues_featues':[1.2, 0.4 .. ]# this can be user age , ... # order of this fields shouldn't changed
                }

            ]
            means  user 2  had interaction with item 2,3,4
        ----------------------------------------------------------------------------------------------------------------
        features: list  of  dics
        {1:{'type':'categorical', }}

        users: list of the user features
          [
          {2:}
          ]

        ----------------------------------------------------------------------------------------------------------------


        '''



#if __name__ == '__main__':
import pandas as pd
import datetime

data = pd.read_csv('data\\Automotive.csv')
data = pd.read_csv('data\\Automotive.csv', header=None)
data.columns=['user','item','rating','unix_time']
data = data.sort_values(['user','unix_time'])



data = data[data.rating>3]
tt = data.groupby('user').size().reset_index(name='counts')

tt= tt[tt.counts>3] #filter users which  has  less than 3 history 
data = data[data.user.isin(list(tt.user))]

item = set(data.item)
user = set(data.user)

items_dict    = {i+1 : j for i, j in enumerate(item)}
item_rev_dict = {j : i+1 for i, j in enumerate(item)}

user_dict ={i+1:j for i,j in enumerate(user)}
user_rev_dict ={j:i+1 for i,j in enumerate(user)}

data['user_int']= data.user.apply(lambda i: user_rev_dict[i] )
data['item_int'] = data.item.apply(lambda i: item_rev_dict[i])
data['time'] = data.unix_time.apply(lambda i: datetime.datetime.utcfromtimestamp(int(i)) )
# print('group = ' , data.groupby('item').size().reset_index(name='counts'))


max_length = data.groupby('item').size().max()
print(data.sort_values(['user']))
print(data.sort_values(['user']))
n_users = max(data.user_int)
n_items = max(data.item_int)

print('hello word ... ')

#model = youtubeModel(number_of_items=n_items,
#                     number_of_users=n_users,
#                     max_history_length=max_length,
#                     feature={})

history = []
users = []
for i,j  in data.groupby('user_int'):

    history.append({'user':i, 'history':list(j['item_int'])} )


for i in history:
    print(i)







#ready_data={}
#for i, j  in data.groupby('user'):
#    print(j)
