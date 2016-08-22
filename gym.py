from keras.models import Sequential
from keras.layers import LSTM, Activation, TimeDistributed, Dense
from keras.callbacks import BaseLogger
from properties import *

from data_generator import input_generator, make_song_array

print "Compiling model"
model = Sequential()
model.add(LSTM(200, input_dim=input_size, return_sequences=True))
model.add(TimeDistributed(Dense(input_size)))
model.compile(optimizer='rmsprop', loss='mse')

print "Generating data"
arr = list()
for i in xrange(1000):
    a = [0]*input_size
    for j in xrange(input_size):
        if j % 6 == 0 or j % 15 == 0:
            a[j] = 1
    arr.append(a)
target = arr[1:]
arr = arr[:-1]



print "Training model"


model.fit_generator(input_generator(), 500, nb_epoch=num_epochs, callbacks=[BaseLogger()])

print make_song_array(model)