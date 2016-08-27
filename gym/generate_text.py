from text_model import *
from getting_midi_from_string import StringConverter

model.load_weights('text_model.h5py')


converter = StringConverter(generate_song(1))

converter.save('test.mid')
