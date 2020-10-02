
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