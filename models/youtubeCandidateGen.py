# reference  https://dl.acm.org/doi/abs/10.1145/2959100.2959190
import tensorflow as tf
class model:
    '''
    In this model we candidate  generation model of
    Deep Neural Networks for YouTube Recommendations paper
    will be implemented
    '''
    def __init__(self, **kwargs):
        '''
            init varables are used for initializing model
        number_of_users
        number_of_items
        max_history_length # 'maximum length of all histories '

        feature= [{'name':'Job', type='categorical',  "count":102, 'emb_length':10},
        {'name':'age', 'type':'continous', }, ...
        ]

        user_features=[
        {'name':'Job",  'length'=3, #   user may have up to least 3 jobs } ,...  ]

        '''

        number_of_items = kwargs['number_of_items']
        if kwargs.get('item_emb_length'):
            item_emb_length = kwargs['item_emb_length']
        else:
            item_emb_length = kwargs['item_emb_length']


        number_of_users = kwargs['number_of_users']
        if kwargs.get('user_emb_length'):
            user_emb_length = kwargs['user_emb_length']
        else:
            user_emb_length=  10




        max_history_length = kwargs['max_history_length']
        feature =kwargs['feature']
        user_features = kwargs['user_features']
        users_embedding = tf.get_variable( [ number_of_users , user_emb_length],dtype=tf.float32, name='user_embedding')
        item_embedding  = tf.get_variable([ number_of_items ,item_emb_length], dtype=tf.float32, name='item_embedding')
        feature_net = {}
        for i in feature:
            if i['type'] =='categorical':
                a = tf.get_variable([ i['count'], i['emb_length'] ], dtype=tf.float32, name=i['name'])
                feature_net.update({i['name']:a})

if __name__ == '__main__':

    # feature = [{'name': 'Job', type = 'categorical', "count":102, 'emb_length': 10},
    # {'name': 'age', 'type': 'continous', }, ...
    # ]
    #
    # user_features = [
    #     {'name': 'Job",  'length'=3, #   user may have up to least 3 jobs } ,...  ]

    params = {'number_of_users':10,
        'number_of_items':10,
        'max_history_length':3,
        'feature': [{'name': 'Job', 'type' : 'categorical', "count":102, 'emb_length': 10}],
        'user_features':[{'name': 'Job', 'length':3 },]
          }

    myModel  = model()


