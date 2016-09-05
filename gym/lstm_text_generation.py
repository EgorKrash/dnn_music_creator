'''Example script to generate text from Nietzsche's writings.
At least 20 epochs are required before the generated text
starts sounding coherent.
It is recommended to run this script on GPU, as recurrent
networks are quite computationally intensive.
If you try this script on new data, make sure your corpus
has at least ~100k characters. ~1M is better.
'''

from __future__ import print_function
from net import *
from os.path import isfile

if isfile('text_model_saved.h5py'):
    model.load_weights('text_model_saved.h5py')

# train the model, output generated text after each iteration
for iteration in range(1, 110):
    print()
    print('-' * 50)
    print('Iteration', iteration)
    model.fit_generator(generate_text(chars), 1500, nb_epoch=20)
    model.save_weights('text_model_saved.h5py')
    for divercity in [0.2, 0.5, 1, 1.2]:
        generate_song_stateful(divercity)
