from keras.models import Sequential
from keras.layers import LSTM, Activation, TimeDistributed, Dense
from properties import *
import keras.backend as K


def squared_error(y_true, y_pred):
    return K.sum(K.square(y_pred - y_true), axis=-1)  # / T.add(K.sum(y_pred, axis=-1), 0.001)


print "Compiling model"
model = Sequential()
model.add(LSTM(100, input_dim=input_size, return_sequences=True))
model.add(TimeDistributed(Dense(input_size)))
model.add(Activation('sigmoid'))
model.compile(optimizer='rmsprop', loss=squared_error)
