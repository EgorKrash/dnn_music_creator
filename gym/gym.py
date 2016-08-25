from model import model
from properties import *
from keras.callbacks import BaseLogger, ModelCheckpoint

from data_generator import midi_input_generator, generate_song_array, save_array_to_midi

print "Training model"

#print generate_song_array(model)
#save_array_to_midi([generate_song_array(model)], 'Generated_zero.mid')
cp = ModelCheckpoint(model_check_point_file, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
model.fit_generator(midi_input_generator(), num_seq_in_epoch, nb_epoch=num_epochs, callbacks=[BaseLogger(), cp])

model.save_weights('net_dump.nw')

save_array_to_midi([generate_song_array(model)], 'Generated.mid')