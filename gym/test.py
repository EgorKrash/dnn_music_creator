from properties import *
from model import model
from data_generator import midi_input_generator, generate_song_array, save_array_to_midi


print "Testing saved model"
model.load_weights('net_dump.nw')

save_array_to_midi([generate_song_array(model)], 'Generated.mid')