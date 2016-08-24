from keras.models import Sequential
from keras.layers import LSTM, Activation, TimeDistributed, Dense
from keras.callbacks import BaseLogger
from properties import *

from data_generator import midi_input_generator, generate_song_array, save_array_to_midi

print "Compiling model"
model = Sequential()
model.add(LSTM(256, input_dim=input_size, return_sequences=True))
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



print "Testing saved model"
model.load_weights('net_dump.nw')

save_array_to_midi([generate_song_array(model)], 'Generated.mid')