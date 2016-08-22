import numpy as np
import random
from mido import MidiFile, MidiTrack, Message
from properties import *

def input_generator():
    while True:
        inputs = np.zeros((batch_size, max_sequence_length, input_size), dtype=bool)
        targets = np.zeros((batch_size, max_sequence_length, input_size), dtype=bool)
        for i in xrange(batch_size):
            rand = random.randint(0, 40)
            for j in xrange(max_sequence_length):
                for k in xrange(input_size):
                    val = (j+k+rand)
                    if val % 6 == 0 or val % 15 == 0:
                        inputs[i, j, k] = 1
                        targets[i, j, k] = 1
            #for k in xrange(input_size):
            #    val = (max_sequence_length + k + rand)
            #    if val % 6 == 0 or val % 15 == 0:
            #        targets[i, max_sequence_length, k] = 1
        yield (inputs, targets)


def make_song_array(model):
    part = np.zeros((1, input_size))
    part[0, 5] = 1
    part[0, 14] = 1
    for i in xrange(max_sequence_length):
        val = np.array([part])
        part = np.append(part, [model.predict(val)[-1, -1]], axis=0)
    return part


def save_array_to_midi(vec, name):
    mid = MidiFile()
    mid.tracks.append(MidiTrack())
    tr = mid.tracks[0]
    notes = [False]*notes_size
    intervals = []*notes_size
    velocities = []*notes_size
    velocity = [0]*notes_size
    for tick_num, tick in enumerate(vec[0]):
        for note, val in enumerate(tick):
            if note < notes_size:
                if val >= note_on_threshold:
                    if not notes[note]:
                        intervals[note].append([tick_num])
                    notes[note] = True
                else:
                    if notes[note]:
                        intervals[note][-1].append(tick_num)
                        velocities.append(velocity[note]/(intervals[note][-1][1] - intervals[note][-1][0]))
                        velocity[note] = 0
                    notes[note] = False
            elif notes[note - notes_size]:
                velocity[note - notes_size] += val
    last_time = 0
    while len(intervals) > 0:
        min_note = -1
        min_tick = -1
        for note, interval in enumerate(intervals):
            if len(interval) == 0:
                continue
            if (min_tick == -1 and interval[0][0]!=-1) or interval[0][0] <= min_tick:
                min_tick = interval[0][0]
                min_note = note
            elif (min_tick == -1 and interval[0][1]!=-1) or interval[0][1] <= min_tick:
                min_tick = interval[1]
                min_note = note
        message = ''
        if intervals[min_note][0] != -1:
            message = Message('note_on', note=min_note, velocity=velocities[note][0], time=(min_tick-last_time)*tick_length)
            intervals[min_note][0] = -1
            del velocities[note][0]
        else:
            message = Message('note_off', note=min_note, time=(min_tick - last_time)*tick_length)
            del intervals[note][0]
        last_time = min_tick
        tr.append(message)
    mid.save(name)
