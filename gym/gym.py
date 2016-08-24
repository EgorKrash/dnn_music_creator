from model import model
from properties import *
from keras.callbacks import BaseLogger

from data_generator import midi_input_generator, generate_song_array, save_array_to_midi

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

#print generate_song_array(model)
#save_array_to_midi([generate_song_array(model)], 'Generated_zero.mid')
model.fit_generator(midi_input_generator(), num_sec_in_epoch, nb_epoch=num_epochs, callbacks=[BaseLogger()])

model.save_weights('net_dump.nw')

save_array_to_midi([generate_song_array(model)], 'Generated.mid')