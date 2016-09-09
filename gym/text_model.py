import random
import sys
from os import listdir

import numpy as np
from music21 import converter, stream, note, chord

from stateful_net import get_st_model

maxlen = 1
step = 1
batch_size = 1000

text = ''
parsed = converter.parse('midi/abide_.mid')

_dur_to_text = {'whole': 'l', 'half': 'k', 'quarter': 'h', 'eighth': 'p', '16th': 'o', '32th': 'i', 'zero': 'u','longa': 'y', 'complex': 'i'}
text_to_dur = {'l': 'whole', 'k': 'half', 'h': 'quarter', 'p': 'eighth', 'o': '16th', 'i': '32th', 'u': 'zero', 'y': 'longa'}

def dur_to_text(dur):
    if dur in _dur_to_text:
        return _dur_to_text[dur]
    else:
        return _dur_to_text['quarter']

instruments = ['Violin', 'Piano', 'Saxophone', 'Guitar', 'Harpsicord']

for part in parsed:
    for voice in part.getElementsByClass(stream.Voice):
        if voice.getInstrument().instrumentName in instruments:
            for thisNote in [n for n in voice if (isinstance(n,note.Note) or isinstance(n,chord.Chord))]:
                for pitch in thisNote.pitches:
                    text += pitch.name+str(pitch.octave)
                text += dur_to_text(thisNote.duration.type)+'z'

'''
for thisNote in parsed.stream:
    for pitch in thisNote.pitches:
        text += pitch.name+str(pitch.octave)
    text += dur_to_text(thisNote.duration.type)+'z'
'''
print('corpus length:', len(text))

chars = sorted(list(set('ABCDEFGlkjhpoiuyz1234567890#-')))
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

generate_per_batch = batch_size

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


def get_song_ds_generator(fi):
    text = ''
    print(fi)
    parsed = converter.parse('midi/' + fi)
    for p in parsed:
        for voice in p.getElementsByClass(stream.Voice):
            if voice.getInstrument().instrumentName in instruments:
                for thisNote in [n for n in voice if (isinstance(n, note.Note) or isinstance(n, chord.Chord))]:
                    for pitch in thisNote.pitches:
                        text += pitch.name + str(pitch.octave)
                    text += dur_to_text(thisNote.duration.type) + 'z'
    if len(text)< batch_size:
        return
    # print('corpus length:', len(text))
    # cut the text in semi-redundant sequences of maxlen characters
    sentences = []
    next_chars = []
    for i in range(0, len(text) - maxlen, step):
        sentences.append(text[i: i + maxlen])
        next_chars.append(text[i + maxlen])
    # print('nb sequences:', len(sentences))
    while True:
        print 'looping'
        # print('Vectorization...')
        X = np.zeros((generate_per_batch, maxlen, len(chars)), dtype=np.bool)
        y = np.zeros((generate_per_batch, len(chars)), dtype=np.bool)
        from_batch = 0
        for i, sentence in enumerate(sentences):
            for t, char in enumerate(sentence):
                X[i % generate_per_batch, t, char_indices[char]] = 1
            y[i % generate_per_batch, char_indices[next_chars[i]]] = 1
            if i % generate_per_batch == generate_per_batch - 1:
                yield ([X], [y])
                X = np.zeros((generate_per_batch, maxlen, len(chars)), dtype=np.bool)
                y = np.zeros((generate_per_batch, len(chars)), dtype=np.bool)

def generate_text(chars):
    files = [each for each in listdir('midi') if each.endswith('.mid')]
    while True:
        fi = random.choice(files)
        yield get_song_ds_generator(fi)



def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def generate_song(model, diversity=1.0, length=1000):
    start_index = random.randint(0, len(text) - maxlen - 1)
    print()
    print('----- diversity:', diversity)
    generated = ''
    sentence = text[start_index: start_index + maxlen]
    generated += sentence
    print('----- Generating with seed: "' + sentence + '"')
    sys.stdout.write(generated)
    for i in range(length):
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
    return generated


def generate_song_stateful(diversity=1.0, length=5000, starting_length=200):
    st = get_st_model()
    start_index = random.randint(0, len(text) - starting_length - 1)
    print('----- diversity:', diversity)
    generated = ''
    sentence = text[start_index: start_index + starting_length]
    generated += sentence
    print('----- Generating with seed: "' + sentence + '"')
    sys.stdout.write(generated)

    x = np.zeros((starting_length, maxlen, len(chars)))
    for t, char in enumerate(sentence):
        x[t, 0, char_indices[char]] = 1.
    for i in xrange(x.shape[1]):
        st.predict(np.array([[x[0, i]]]))
    sentence = sentence[-1:]
    for i in range(length):
        x = np.zeros((1, 1, len(chars)))
        for t, char in enumerate(sentence):
            x[0, 0, char_indices[char]] = 1.
        preds = st.predict(x, verbose=0)[0]
        next_index = sample(preds, diversity)
        next_char = indices_char[next_index]
        generated += next_char
        sentence = '' + next_char
        sys.stdout.write(next_char)
        sys.stdout.flush()
    print()
    return generated


