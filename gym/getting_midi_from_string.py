from music21 import chord, stream, midi, duration



class StringConverter():

    def __init__(self,inp_text):

        self.inp_text = inp_text

        self.notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

        self.text_to_dur = {'l': 'whole', 'k': 'half', 'h': 'quarter', 'p': 'eighth',
                       'o': '16th', 'i': '32th', 'u': 'zero', 'y': 'longa'}

    def fix(self, inp_crd):
        out_text = ''
        was_special = False
        was_note = -1
        special = ''
        letter = 0

        duration = self.text_to_dur[inp_crd[-1]]

        while letter < len(inp_crd):
            if inp_crd[letter] in self.notes:
                was_note = letter
                # print(was_note,inp_text[was_note])

            elif was_note >= 0 and (inp_crd[letter] is '-' or inp_crd[letter] is '#'):
                # print(inp_text[letter])
                if not was_special:
                    if inp_crd[letter] is '-':
                        special = '-'
                        was_special = True
                    else:
                        special = '#'
                        was_special = True

            elif inp_crd[letter].isdigit():
                # print('isdig')
                if was_note >= 0:

                    place = inp_crd[was_note] + special + inp_crd[letter] + ' '
                    # print(inp_text[was_note])
                    out_text += place

                    was_note = -1
                    special = ''
                    was_special = False
                else:
                    letter += 1
                    continue

            else:
                letter += 1
                continue

            letter += 1

        return out_text.rstrip(' '), duration


    def save(self,path_to_save):

        string = self.inp_text

        stream1 = stream.Stream()
        # print(st)
        for crd in string.split('z'):
            crd = crd.lstrip('-')
            crd = crd.lstrip('#')

            cr, dur = self.fix(crd)

            d = duration.Duration(dur)
            # print cr,dur, d
            stream1.append(chord.Chord(cr.split(), duration=d))

        midi_file = midi.translate.streamToMidiFile(stream1)
        midi_file.open(path_to_save, 'wb')
        midi_file.write()
        midi_file.close()

