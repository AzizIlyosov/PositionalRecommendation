
import  tensorflow  as  tf

class CandidateModel(object):
    def __init__(self, user_count, item_count, jobc_count, jobcode_list, batchsize=1):
        with tf.variable_scope('candidModel'):
            self.item_count = item_count
            self.u = tf.placeholder(tf.int32, [None, ])  # [B]#index of user
            self.i = tf.placeholder(tf.int32, [None, ])  # [B]#index of  positive  item
            self.y = tf.placeholder(tf.int32, [None, ])  # [B]#output value 0 or  1
            self.hist_i = tf.placeholder(tf.int32, [None, None])  # [B, T]#history of  user
            self.sl = tf.placeholder(tf.int32, [None, ])  # [B]#list of length histories
            self.batchsize = batchsize
            hidden_units = 128
            user_emb_w = tf.get_variable("user_can_emb_w", [user_count, hidden_units])
            item_emb_w = tf.get_variable("item_can_emb_w", [item_count, hidden_units ])
            # in followiing  lines  features of  items  and  users
            # for example  categories=[9,7,5,6,8,2] , items =[2,4,1](items  explaines  order  or  items )
            # tf.gather(categories,items) = [5,8,7]

            uj = tf.gather(jobcode_list, self.u)  # user jobcode
            h_emb = tf.concat([  # histories and  categories  embeddings
                tf.nn.embedding_lookup(item_emb_w, self.hist_i)
            ], axis=2)
            # -- sum begin -------
            mask = tf.sequence_mask(self.sl, tf.shape(h_emb)[1], dtype=tf.float32)  # [B, T]
            mask = tf.expand_dims(mask, -1)  # [B, T, 1]
            mask = tf.tile(mask, [1, 1, tf.shape(h_emb)[2]])  # [B, T, H]
            h_emb *= mask  # [B, T, H]
            hist = h_emb
            print("this  is  history shape ", hist)
            hist = tf.reduce_sum(hist, 1)
            hist = tf.div(hist, tf.cast(tf.tile(tf.expand_dims(self.sl, 1), [1, hidden_units]), tf.float32))
            print(h_emb.get_shape().as_list())
            # -- sum end ---------

            hist = tf.layers.batch_normalization(inputs=hist)

            # -- fcn begin -------
            din_i = tf.concat([hist], axis=-1)
            din_i = tf.layers.batch_normalization(inputs=din_i, name='bCan1')
            d_layer_1_i = tf.layers.dense(din_i, hidden_units,     activation=tf.nn.relu, name='fCan1')
            d_layer_2_i = tf.layers.dense(d_layer_1_i,hidden_units-10,     activation=tf.nn.relu, name='fCan2')
            d_layer_3_i = tf.layers.dense(d_layer_2_i, hidden_units//2, activation=tf.nn.relu, name='fCan3')

            self.logits=tf.layers.dense(d_layer_3_i,  units=item_count,activation=None,name='logitCan' )
            self.Prob, self.topk=tf.nn.top_k(tf.nn.softmax(self.logits),k=1000)
            self.global_step = tf.Variable(0, trainable=False, name='global_step')
            self.global_epoch_step = \
                tf.Variable(0, trainable=False, name='global_epoch_step')
            self.global_epoch_step_op = \
                tf.assign(self.global_epoch_step, self.global_epoch_step + 1)
            self.loss=tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits_v2( logits=self.logits,labels=tf.one_hot(self.y,item_count)))

            trainable_params = tf.trainable_variables()
            self.opt = tf.train.GradientDescentOptimizer(learning_rate=0.02)
            gradients = tf.gradients(self.loss, trainable_params)
            clip_gradients, _ = tf.clip_by_global_norm(gradients, 5)
            self.train_op = self.opt.apply_gradients(
                zip(clip_gradients, trainable_params), global_step=self.global_step)

    def train(self, sess, uij):

        loss, _, preds= sess.run([self.loss, self.train_op, self.topk], feed_dict={
            self.y: uij[1],  # positive  item
            self.hist_i: uij[3],  # history of  user  filled with zero
            self.sl: uij[4] ,  # Length of histories  length
        })
        return loss

    def  getItemEmbedding(self,sess):
        return  sess.run('candidModel/item_can_emb_w:0')



    def eval(self, sess, uij):
        topk=  sess.run(self.topk, feed_dict={
            self.hist_i: uij[3],  # history of  user
            self.sl: uij[4]  # length of  history length
        })

        acc1=acc5=acc10=0
        for  i,ans in zip(uij[1], topk):
            if i==ans[0]:
                acc1+=1
            if i in list(ans[0:5]):
                acc5+=1
            if i in  list(ans[0:10]):
                acc10+=1
        return acc1,acc5,acc10




    def predict(self, sess, uij, topN=20):
        preditions= sess.run(self.topk, feed_dict={
            self.hist_i:uij[3],
            self.sl:uij[4]
        })
        return preditions
    
    def getProb(self, sess, uij, topN=20):
        preditions= sess.run(self.Prob, feed_dict={
            self.hist_i:uij[3],
            self.sl:uij[4]

        })
        return preditions

    def save(self, sess, path):
        saver = tf.train.Saver(tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, 'candidModel'))
        saver.save(sess, save_path=path)

    def restore(self, sess, path):
        saver = tf.train.Saver(tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, 'candidModel'))
        saver.restore(sess, save_path=path)


def extract_axis_1(data, ind):
    batch_range = tf.range(tf.shape(data)[0])
    indices = tf.stack([batch_range, ind], axis=1)
    res = tf.gather_nd(data, indices)
    return res

