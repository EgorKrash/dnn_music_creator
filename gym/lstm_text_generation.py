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
i = 0
for generator in generate_text(chars):
    i+=1
    print()
    print('-' * 50)
    for i in xrange(20):
        model.reset_states()
        try:
            model.fit_generator(generator, 100000, nb_epoch=1)
        except BaseException:
            continue
        model.save_weights('text_model_saved.h5py')
    if i % 20 == 0:
        for divercity in [0.2, 0.5, 1, 1.2]:
            generate_song_stateful(divercity)
