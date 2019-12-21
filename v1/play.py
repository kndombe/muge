from collections import defaultdict
from urllib.request import urlopen
import pygame
import pygame.midi as midi
import copy
import time
import os
import ast
import random
import sys
import urllib
import requests

# FastAPI


chords_folder = 'play/chords/'


class Play():
    def __init__(self, chords, instruments=[], quantize=False):
        tempo = 120
        self.bar = 60 / tempo
        # print(tempo)
        # print(self.bar)
        if self.bar < 0.2:
            quantize = False
        self.chords = []
        # print(chords)
        self.instruments = instruments
        # https://github.com/kndombe/muge/blob/master/v1/easy%20simple.chtr
        # with open(chords, 'r') as f:
        #     for line in f.readlines():
        #         self.chords.append(ast.literal_eval(line))
        for line in urlopen(chords).readlines():
            line = str(line)
            line = line.split('"')[1].split('\\')[0]
            self.chords.append(ast.literal_eval(line))
        self.met = 0
        self.current = 0
        self.quantize = quantize
        self.getchords()
        self.notes = defaultdict(dict)
        midi.init()
        self.channels = {'piano': 0, 'bass': 1, 'strings': 2,
                         'guitar': 3, 'drums_kick': 4, 'drums_snare': 5}
        self.player = midi.Output(0)
        self.player.set_instrument(0, self.channels['piano'])
        self.player.set_instrument(34, self.channels['bass'])
        self.player.set_instrument(89, self.channels['strings'])
        self.player.set_instrument(25, self.channels['guitar'])
        self.player.set_instrument(116, self.channels['drums_kick'])
        self.player.set_instrument(115, self.channels['drums_snare'])

    def getchords(self):
        self.chords_dict = {}
        chord_names = [name for name in os.listdir(chords_folder)
                       if os.path.isfile(chords_folder+name) and name.endswith('.chord')]
        for name in chord_names:
            with open(chords_folder+name) as f:
                line = f.readline()
                name = name[:-len('.chord')]
                self.chords_dict[name] = ast.literal_eval(line)

    def start(self):
        chords = copy.deepcopy(self.chords)
        # print(chords)
        chords = [(chord[0], self.quantizenote(chord[1]), self.quantizenote(chord[2]), chord[3])
                  for chord in chords]
        # print(chords)
        end = self.chords[-1][2]
        previous_chord = None
        while self.current < end:
            if self.current >= chords[0][2]:
                chords.pop(0)
                if len(chords) == 0:
                    break
            beat = chords[0][2] - chords[0][1]
            chord = chords[0][0]
            conf = chords[0][3]
            if chord != previous_chord and beat >= 0.5:
                self.noteoff_all()
                print(chord)
            previous_chord = chord if previous_chord == None else previous_chord

            # if self.quantize or True:
            if beat >= 0.5:
                self.playchord(
                    chord, chords[0][3], self.met == 0 or chord != previous_chord, self.met)
            bar = beat / 4
            self.current += bar
            self.met = (self.met+1) % 4
            time.sleep(bar)
            # else:
            #     chord_end = chords[0][2]
            #     self.playchord(chord, chords[0][3], True)
            #     time.sleep(chord_end-self.current)
            #     self.current = chord_end
            previous_chord = chord
        del self.player
        pygame.midi.quit()

    def quantizenote(self, time):
        if not self.quantize:
            return time
        # time += -.2
        best = (time, float('inf'))
        for i in range(int(time/self.bar) + 1):
            if abs(time - self.bar*i) < best[1]:
                best = (self.bar*i, abs(time-self.bar*i))
        return best[0]

    def playchord(self, chord, conf, main, met):
        main_notes = self.chords_dict[chord]['main']
        fill_notes = self.chords_dict[chord]['fill']
        if main:
            for note in main_notes:
                self.playnote(note, 90, 'piano')
                self.playnote(note, 85, 'strings')
            self.playnote(self.bass_note(main_notes[0]-12*2), 90, 'bass')
            self.playnote(50, 110, 'drums_kick')
        else:
            if met == 2:
                self.playnote(75, 90, 'drums_snare')
            for _ in range(3):
                fill = copy.deepcopy(fill_notes)
                random.shuffle(fill)
                self.playnote(fill[0], random.randint(
                    50, 90), 'piano')
            self.playnote(
                self.bass_note(main_notes[0]-12*(random.randint(1, 2))), 90, 'bass')

        self.playnote(105, 80, 'drums_snare')
        for _ in range(2):
            if random.random() < .7:
                break
            notes = copy.deepcopy(main_notes)
            random.shuffle(notes)
            self.playnote(notes[0]+12, random.randint(55, 80), 'guitar')

    def playnote(self, note, vel, player):
        instr = 'drums' if player.startswith('drums') else player
        if len(self.instruments) > 0 and not instr in self.instruments:
            return
        channel = self.channels[player]
        if note in self.notes[player]:
            self.player.note_off(note, self.notes[player][note], channel)
        self.player.note_on(note, vel, channel)
        self.notes[player][note] = vel

    def noteoff_all(self):
        for player in self.notes:
            for note in self.notes[player]:
                self.player.note_off(
                    note, self.notes[player][note], self.channels[player])

    def bass_note(self, note):
        while note < 30:
            note += 12
        return note


if __name__ == '__main__':
    if len(sys.argv) > 1:
        song_chords = sys.argv[1]
    else:
        song_chords = 'heal simple.chtr'
    instruments = sys.argv[2].split(' ') if len(sys.argv) >= 3 else []
    if not song_chords.endswith('.chtr'):
        song_chords += '.chtr'
    print('Playing from file {}'.format(song_chords))
    Play(song_chords, instruments=instruments).start()
