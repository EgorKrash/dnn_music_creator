#!/usr/bin/python
from __future__ import print_function
from getting_midi_from_string import StringConverter
from keras.models import load_model
from text_model import generate_song
import sys
import getopt

model = load_model('model_dump.h5py')

model.load_weights('text_model_saved.h5py')

print("Generating song")
converter = StringConverter(generate_song(model))

file_path = 'generated.mid'
if len(sys.argv) > 0:
    print('saving to:', sys.argv[0])
    file_path = sys.argv[0]
else:
    print('No file path given. Saving to out.mid')
converter.save(file_path)
