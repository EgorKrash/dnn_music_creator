'''Example script to generate text from Nietzsche's writings.
At least 20 epochs are required before the generated text
starts sounding coherent.
It is recommended to run this script on GPU, as recurrent
networks are quite computationally intensive.
If you try this script on new data, make sure your corpus
has at least ~100k characters. ~1M is better.
'''

from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy as np
import random
import sys
from os import listdir

from music21 import converter

maxlen = 200
step = 3

text = ''
parsed = converter.parse('midi/abide_.mid')

_dur_to_text = {'whole': 'l', 'half': 'k', 'quarter': 'h', 'eighth': 'p', '16th': 'o', '32th': 'i', 'zero': 'u','longa': 'y', 'complex': 'i'}
text_to_dur = {'l': 'whole', 'k': 'half', 'h': 'quarter', 'p': 'eighth', 'o': '16th', 'i': '32th', 'u': 'zero', 'y': 'longa'}

def dur_to_text(dur):
    if dur in _dur_to_text:
        return _dur_to_text[dur]
    else:
        return _dur_to_text['quarter']

for thisNote in parsed.recurse().notes:
    for pitch in thisNote.pitches:
        text += pitch.name+str(pitch.octave)
    text += dur_to_text(thisNote.duration.type)+'z'

print('corpus length:', len(text))

chars = sorted(list(set('ABCDEFGlkjhpoiuyz1234567890#-')))
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

generate_per_batch = 100

sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])
print('nb sequences:', len(sentences))

print('Vectorization...')
X = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        X[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1

print ('Gettng data')
def generate_text(chars):
    while True:
        files = [each for each in listdir('midi') if each.endswith('.mid')]
        for i, fi in enumerate(files):
            text = ''
            #print(fi)
            parsed = converter.parse('midi/'+fi)

            for thisNote in parsed.recurse().notes:
                for pitch in thisNote.pitches:
                    text += pitch.name + str(pitch.octave)
                text += dur_to_text(thisNote.duration.type) + 'z'

            #print('corpus length:', len(text))
            # cut the text in semi-redundant sequences of maxlen characters

            sentences = []
            next_chars = []
            for i in range(0, len(text) - maxlen, step):
                sentences.append(text[i: i + maxlen])
                next_chars.append(text[i + maxlen])
            #print('nb sequences:', len(sentences))

            #print('Vectorization...')
            X = np.zeros((generate_per_batch, maxlen, len(chars)), dtype=np.bool)
            y = np.zeros((generate_per_batch, len(chars)), dtype=np.bool)
            from_batch = 0
            for i, sentence in enumerate(sentences):
                for t, char in enumerate(sentence):
                    X[i%generate_per_batch, t, char_indices[char]] = 1
                y[i%generate_per_batch, char_indices[next_chars[i]]] = 1
                if i%generate_per_batch == generate_per_batch-1:
                    yield ([X], [y])
                    X = np.zeros((generate_per_batch, maxlen, len(chars)), dtype=np.bool)
                    y = np.zeros((generate_per_batch, len(chars)), dtype=np.bool)



# build the model: a single LSTM
print('Build model...')
model = Sequential()
model.add(LSTM(512, input_shape=(maxlen, len(chars)), return_sequences=True))
model.add(LSTM(512 ))
model.add(Dense(len(chars)))
print (len(chars))
model.add(Activation('softmax'))

optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)


def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

# train the model, output generated text after each iteration
for iteration in range(1, 11):
    print()
    print('-' * 50)
    print('Iteration', iteration)
    model.fit_generator(generate_text(chars), 1720, nb_epoch=20)

    start_index = random.randint(0, len(text) - maxlen - 1)
    for diversity in [0.2, 0.5, 1.0, 1.2]:
        print()
        print('----- diversity:', diversity)
        generated = ''
        sentence = text[start_index: start_index + maxlen]
        generated += sentence
        print('----- Generating with seed: "' + sentence + '"')
        sys.stdout.write(generated)
        for i in range(400):
            x = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(sentence):
                x[0, t, char_indices[char]] = 1.
            preds = model.predict(x, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]
            generated += next_char
            sentence = sentence[1:] + next_char
            sys.stdout.write(next_char)
            sys.stdout.flush()
        print()
