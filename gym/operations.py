from mido import Message, MidiTrack
import numpy as np
from mido import MidiFile
from time import clock

import numpy as np

class MidiParser():
    
    def __init__(self,path_to_file):
        self.song = MidiFile(path_to_file)
        
    #===========================================================================    
    
    
    def checking_note_offs(self):
        for track in self.song.tracks:
            for message in track:
                if message.type is 'note_off':
                    return True
                
        return False
    
    #===========================================================================
    def null_vel_to_note_off(self):
        if not self.checking_note_offs():

            for track in self.song.tracks:
                for index,message in enumerate(track):
                    if message.type is 'note_on' and message.velocity is 0:
                        time = message.time
                        channel = message.channel
                        velocity = message.velocity
                        note = message.note
                        
                        track.remove(message)
                        track.insert(index,Message('note_off', channel=channel, note=note, velocity=velocity,time=time))
            return self.song
        else:
            return self.song
            
    #===========================================================================
    
    def unique_notes(self):
        unique_notes = []
        for track in self.song.tracks:
            for message in track:
                try:
                    if message.note in unique_notes:
                        continue
                    else:
                        unique_notes.append(message.note)
                except:
                    continue
                    
        return len(unique_notes)
    
    #============================================================================
    
    def get_length(self): 
        
        lengths = []

        for track in self.song.tracks:
            len_of_track = 0
            for message in track:
                if message.type is 'note_on' or message.type is 'note_off':
                    len_of_track += message.time
            lengths.append(len_of_track)

        return max(lengths)

    #============================================================================
    def sorting_by_value(self,dic):
        for key in dic:
            dic[key].sort()

        return dic

    #============================================================================
    
    def find_start(self):
        lengths = []
        for track in self.song.tracks:
            time = 0
            for message in track:

                time += message.time
                if message.type == 'note_on':
                    lengths.append(time) 
                    break

        return min(lengths)
    
    #===========================================================================
    
    def get_durations_and_velocities(self):
        velocities = {}
        durations = {}
        notes = {}
        current_time = 0
        for track in self.song.tracks[1:]:
            is_noted = False
            for message in track:
                current_time += message.time 
                if message.type is 'note_on' and message.velocity > 0:
                    is_noted = True
                    if message.note in notes:
                        continue
                    else:
                        notes[message.note] = [current_time]
                        if message.note in velocities:
                            velocities[message.note].append(message.velocity)
                        else:
                            velocities[message.note] = [message.velocity]

                elif message.type is 'note_off' or (message.type is 'note_on' and message.velocity is 0):
                    try:
                        notes[message.note].append(current_time)
                        if message.note in durations:
                            durations[message.note].append(notes[message.note])
                        else:
                            durations[message.note] = [notes[message.note]]
                        del notes[message.note]

                    except KeyError:
                        continue
            if is_noted:
                break
            current_time = 0
        return durations,velocities
    
    #================================================================================
    
    def Parse(self, tick):
        dic, velocities = self.get_durations_and_velocities()
        sorted_dic = self.sorting_by_value(dic)
        current_time = self.find_start()
        len_of_song = self.get_length() 
        result = []
        while current_time < len_of_song:
            vec = np.array([0]*128,dtype='float32')
            vec_velocities  = np.array([0]*128,dtype='float32')
            for note in sorted_dic:
                for i,interval in enumerate(sorted_dic[note]):
                    on_tick = interval[0]
                    off_tick = interval[1]
                    #note_duration = off_tick - on_tick
                    if current_time < on_tick:
                        break

                    elif off_tick+tick < current_time:
                        continue

                    else:
                        if current_time > off_tick:
                            vec[note] = ((current_time-off_tick)/tick)
                            vec_velocities[note] = velocities[note][i]/127
                            del sorted_dic[note][i]
                        else:
                            vec[note] = min((current_time-on_tick)/tick,1)
                            vec_velocities[note] = velocities[note][i]/127


            #result.append(np.append(vec, vec_velocities))
            current_time += tick
            yield np.append(vec, vec_velocities)
    
