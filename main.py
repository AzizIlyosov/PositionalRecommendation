
class main:
    '''
    In this model we will candidate  generation part of
    Deep Neural Networks for YouTube Recommendations paper
    '''
    def __init__(self, history ,users  ):
        '''
        history :  dict type variable:
            key show  user id while value (list)  shows item id's
            [
                {2:[2,3,4]}
            ] means  user 2  had interaction with item 2,3,4
        ----------------------------------------------------------------------------------------------------------------

        users: list of the user features
          [
          {2:}
          ]

        ----------------------------------------------------------------------------------------------------------------


        '''