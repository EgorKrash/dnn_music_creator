from keras.models import Sequential
from keras.layers import LSTM, Activation, TimeDistributed, Dense
from properties import *
import keras.backend as K
import theano.tensor as T
from keras.objectives import kullback_leibler_divergence

def squared_error(y_true, y_pred):
    return K.sum(K.square(y_pred - y_true), axis=-1)# / T.add(K.sum(y_pred, axis=-1), 0.001)


print "Compiling model"
model = Sequential()
model.add(LSTM(512, input_dim=input_size, return_sequences=True))
model.add(TimeDistributed(Dense(input_size)))
model.compile(optimizer='rmsprop', loss=squared_error)