from __future__ import print_function
import numpy as np
from random import choice
from mido import MidiFile, MidiTrack, Message
from properties import *
from operations import MidiParser
from os import listdir


def midi_input_generator():
    while True:
        files = [each for each in listdir('midi') if each.endswith('.mid')]
        for f in files:
            parser = MidiParser(midi_folder+f)
            input_gen = parser.Parse(tick_length)
            batches = np.zeros((num_seq_to_generate+1, sequence_length+1, input_size), dtype='float32')
            batches_fill = 0
            i = 0
            for val in input_gen:
                batches[batches_fill, i % (sequence_length + 1)] = val
                #print(val)
                if i % (sequence_length+1) == sequence_length:
                    batches_fill += 1
                    if batches_fill == num_seq_to_generate+1:
                        yield (batches[:][:-1][:], batches[:][1:][:])
                        batches = np.zeros((num_seq_to_generate+1, sequence_length+1, input_size), dtype='float32')
                        batches_fill = 0
                    continue
                i += 1


def __sample(a, temperature=1.0):
    #print(a)

    a = np.log(a) / temperature
    #print(a)

    a = (np.exp(a) - max(a)) / np.sum(np.exp(a) - max(a))
    return np.argsort(np.random.multinomial(1, a, 1))[0][:max_notes_together]


def generate_song_array(model):
    part = np.zeros((1, input_size), dtype='float32')
    f = choice([each for each in listdir(midi_folder) if each.endswith('.mid')])
    parser = MidiParser(midi_folder+f)
    print ('Generating song array from', f)
    gen = parser.Parse(tick_length)
    i = 0
    for p in gen:
        i += 1
        part = np.append(part, [p], axis=0)
        if i == sequence_length:
            break
    print ('', end='')
    res = np.zeros((out_sequence_length, input_size), dtype=float)
    for i in xrange(out_sequence_length):
        print('\r', i, 'of', out_sequence_length, end='')
        val = np.array([part])
        part = np.append(part, [model.predict(val)[-1, -1]], axis=0)
        is_on = [0.0]*notes_size
        for j in xrange(notes_size):
            if part[-1][j] < note_on_threshold:
                part[-1][j] = 0.01
        pl = __sample(part[-1][:notes_size], 0.01)
        part[-1] = np.zeros(input_size)
        print(pl)
        for j in pl:
            part[-1][j] = 1
        #print (' started ', pl, 'asdf')
        if part.shape[0] > sequence_length:
            part = part[1:]
        res[i] = part[-1]
    return res


def is_empty(intervals):
    for el in intervals:
        if len(intervals[el]) > 0:
            return False
    return True


def save_array_to_midi(vec, name):
    mid = MidiFile()
    mid.tracks.append(MidiTrack())
    tr = mid.tracks[0]
    tr.append(Message('program_change', program=0, time=0))
    notes = [False]*notes_size
    intervals = {}
    velocities = {}
    for i in xrange(notes_size):
        intervals[i] = []
        velocities[i] = []

    velocity = [0]*notes_size
    for tick_num, tick in enumerate(vec[0]):
        for note, val in enumerate(tick):
            if note < notes_size:
                if val >= note_on_threshold:
                    if not notes[note]:
                        intervals[note].append((tick_num, -1))
                    notes[note] = True
                else:
                    if notes[note]:
                        intervals[note][-1] = (intervals[note][-1][0], tick_num)
                        if (intervals[note][-1][1] - intervals[note][-1][0]) != 0:
                            velocities[note].append(velocity[note]/(intervals[note][-1][1] - intervals[note][-1][0]))
                        else:
                            velocities[note].append(velocity[note])
                        velocity[note] = 0
                    notes[note] = False
            elif notes[note - notes_size]:
                velocity[note - notes_size] += val
    last_time = 0
    for i in xrange(128):
        if len(intervals[i]) > 0 and intervals[i][-1][1] == -1:
            del intervals[i][-1]
        assert len(intervals[i]) == len(velocities[i])
    while not is_empty(intervals):
        min_note = -1
        min_tick = -1
        for note in intervals:
            interval = intervals[note]
            if len(interval) == 0:
                continue
            if (min_tick == -1 or interval[0][0] <= min_tick) and interval[0][0] != -1:
                min_tick = interval[0][0]
                min_note = note
            elif (min_tick == -1 or interval[0][1] <= min_tick) and interval[0][1] != -1:
                min_tick = interval[0][1]
                min_note = note
        #if min_note == -1:
            #print intervals
        message = ''
        if min_note == -1:
            break
        if intervals[min_note][0][0] != -1:
            #message = Message('note_on', note=min_note, velocity=int(min(round(velocities[min_note][0]*127), 127)), time=(min_tick-last_time)*tick_length)
            message = Message('note_on', note=min_note, velocity=64, time=(min_tick-last_time)*tick_length)
            intervals[min_note][0] = (-1, intervals[min_note][0][1])
            del velocities[min_note][0]
        else:
            message = Message('note_off', note=min_note, time=(min_tick - last_time)*tick_length)
            del intervals[min_note][0]
        last_time = min_tick
        tr.append(message)
    mid.save(name)