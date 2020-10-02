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
            item_emb_length = 10


        number_of_users = kwargs['number_of_users']
        if kwargs.get('user_emb_length'):
            user_emb_length = kwargs['user_emb_length']
        else:
            user_emb_length=  10




        max_history_length = kwargs['max_history_length']
        self.feature =kwargs['feature']
        user_features = kwargs['user_features']

        with  tf.variable_scope('youtube_candidate_gen'):
            self.users_embedding = tf.get_variable( 'user_embedding', [ number_of_users , user_emb_length], dtype=tf.float32)
            self.item_embedding  = tf.get_variable('item_embedding',  [ number_of_items , item_emb_length], dtype=tf.float32)
            self.feature_net_emb = {}
            for i in self.feature:
                if i['type'] =='categorical':
                    a = tf.get_variable('feature_'+i['name'], [ i['count'], i['emb_length'] ], dtype=tf.float32)
                    self.feature_net_emb.update({i['name']:a})


    def train(self, history, batchsize, epochs, sess):
        em = sess.run(self.item_embedding)
        print(em)


if __name__ == '__main__':

    # feature = [{'name': 'Job', type = 'categorical', "count":102, 'emb_length': 10},
    # {'name': 'age', 'type': 'continous', }, ...
    # ]
    #
    # user_features = [
    #     {'name': 'Job",  'length'=3, #   user may have up to least 3 jobs } ,...  ]

    params = {
        'number_of_users':10,
        'number_of_items':10,
        'max_history_length':3,
        'feature': [{'name': 'Job','type' : 'categorical', "count":102, 'emb_length': 10},
                    {'name':'age', 'type':'continous' }],

        'user_features':[{'name': 'Job', 'length':3},
                         {'name': 'age', 'length':1 }]

          }

    myModel  = model(**params)
    with tf.Session() as  sess:
        sess.run(tf.global_variables_initializer)
        myModel.train([1,2,3],4,5,sess )

