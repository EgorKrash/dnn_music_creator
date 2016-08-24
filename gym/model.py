from keras.models import Sequential
from keras.layers import LSTM, Activation, TimeDistributed, Dense
from properties import *

print "Compiling model"
model = Sequential()
model.add(LSTM(256, input_dim=input_size, return_sequences=True))
model.add(LSTM(256, return_sequences=True))
model.add(TimeDistributed(Dense(input_size)))
model.compile(optimizer='rmsprop', loss='mse')