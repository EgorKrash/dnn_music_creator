#!/usr/bin/python
from __future__ import print_function
from getting_midi_from_string import StringConverter
from keras.models import load_model
from text_model import generate_song
import sys
from os import system

model = load_model('model_dump.h5py')

model.load_weights('text_model_saved.h5py')

print("Generating song")
converter = StringConverter(generate_song(model))

file_path = 'out.mid'
if len(sys.argv) > 1:
    print('saving to:', sys.argv[1])
    file_path = sys.argv[1]
else:
    print("No file path given. Saving to out.mid")

tmp_path = 'tmp/' + file_path.split('/')[-1].split('.')[0]+'.mid'

if file_path.endswith('.mid'):
    converter.save(file_path)
else:
    converter.save(tmp_path)
    system('./convert_to_mp3.sh ' + tmp_path + ' ' + file_path)
