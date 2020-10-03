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

        feature= {'Job':{ type='categorical',  "count":102, 'emb_length':10},
        {'name':'age', 'type':'continous', }, ...# since in some datasets feature can be common
                                                    between users and items we splitted user feature and feature
        }


        user_features=[
        {'name':'Job",  'length'=3, } ,...  ]  #    this means user may have up to least 3 jobs(in
                                               #    practice you my use as much as you want)


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
        self.user_features = kwargs['user_features']

        with  tf.variable_scope('youtube_candidate_gen'):
            self.users_embedding = tf.get_variable( 'user_embedding', [ number_of_users , user_emb_length], dtype=tf.float32)
            self.item_embedding  = tf.get_variable('item_embedding',  [ number_of_items , item_emb_length], dtype=tf.float32)
            self.feature_net_emb = {}
            for i in self.feature:
                if self.feature[i]['type'] == 'categorical':
                    a = tf.get_variable('feature_'+i, [ self.feature[i]['count'], self.feature[i]['emb_length'] ], dtype=tf.float32)
                    self.feature_net_emb.update({i:a})

            self.user_id = tf.placeholder(dtype=tf.int32, shape=[None, ],    name = 'user_id')
            self.history = tf.placeholder(dtype=tf.int32, shape=[None, max_history_length ], name='item_id')

            self.user_feature_placeholder={}
            self.mask_features={}

            for i in self.user_features:
                if self.feature_net_emb.get(i): # this means feature is categorical because there
                                                # is embedding for this feature

                    a = tf.placeholder( dtype=tf.int32,   shape = [None, self.user_features[i]['length']] ,name='feature_id_'+i  )
                else:
                    a = tf.placeholder( dtype=tf.float32, shape = [None, self.user_features[i]['length']] ,name='feature_id_'+i  )

                self.user_feature_placeholder.update({i:a})

            # before getting average of features , 0 embedding should be  removed
            # firstly,  indexes are turned into bool,
            # then they are converted to int again





            user_feature_emb_gather={}
            for i in self.feature_net_emb:
                user_feature_emb_gather.update({i:tf.gather(params=self.feature_net_emb[i], indices=self.user_feature_placeholder[i], name='gather_'+i )})








            for i in user_feature_emb_gather:
                user_feature_emb_gather[i] = tf.reduce_mean( user_feature_emb_gather[i] , axis=1, name='mean_feature_'+i)








    def train(self, history, batchsize, epochs, sess):
        print('model is  being traned ....')
        # em = sess.run( # self.user_feature_placeholder['Job'],
        #               feed_dict={
        #
        #               })
        print(em)
        print('model has trained ....')


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
        'feature': {'Job':{ 'type' : 'categorical', "count":102, 'emb_length': 10},
                    'age':{ 'type':'continous' }},

        'user_features':{'Job':{ 'length':3},
                         'age':{ 'length':1 }},
        'users_features':{
            #this  is feed  data  for  network
            1 : [1,2,3],
            2 : [0,0,3],

                          }
    }

    myModel  = model(**params)
    with tf.Session() as  sess:
        sess.run(tf.initialize_all_variables())
        myModel.train([1,2,3],4,5, sess )

