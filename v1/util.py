import ast
import numpy as np
import scipy.io.wavfile as wf
import wave
import random
import os
import sys
import copy
import math

CHUNK = 4410  # Assumption: the audios will be sampled at 44100 hz
SMOOTHING = 0


def load(path, split=.7):
    x_train = []
    x_test = []
    y_train = []
    y_test = []
    with open(path, 'r') as f:
        lines = f.readlines()
        random.shuffle(lines)
        threshold = int(len(lines)*split)
        print('Loading data...')
        for i, line in enumerate(lines):
            data = ast.literal_eval(line)
            if i < threshold:
                x_train.append(data['signal'])
                y_train.append(data['chord'])
            else:
                x_test.append(data['signal'])
                y_test.append(data['chord'])
            showprogress((i+1)/len(lines))
            # if (i+1)/len(lines) > .05:break
    return np.array(x_train, dtype='float'), np.array(y_train), np.array(x_test, dtype='float'), np.array(y_test)


def getdata(path, precision=1, split=True):
    signal = wave.open(path, 'r')
    fs = signal.getframerate()
    signal = np.fromstring(signal.readframes(-1), 'Int16')
    b = 0
    d = []
    print('Extracting data from file {}...'.format(path))
    if split:
        while True:
            t = b + CHUNK
            showprogress((t+1)/(signal.size))
            if t >= signal.size:
                break
            d.append(list(signal[b:t]))
            b += int(CHUNK/precision)
        print('Extracted {} parts from audio file.'.format(len(d)))
    else:
        d.append(list(signal))
        print('Extracted 1 list of {} sample points.'.format(len(signal)))
    return fs, np.array(d)


def getfrequencies():
    freq = {}
    with open('notes/frequencies.JSON', 'r') as f:
        freq = ast.literal_eval(''.join(f.readlines()))
        f.close()
    return freq


def getchords():
    chords = {}
    with open('notes/chords.JSON', 'r') as f:
        chords = ast.literal_eval(''.join(f.readlines()))
        f.close()
    return chords


def showprogress(percentage):
    length = 30
    percentage = percentage if percentage < 1 else 1
    done = int(length*percentage)
    left = length - done
    arrow = 0
    if done < length:
        done -= 1 if done > 0 else 0
        arrow = 1
    sys.stdout.write('\r[{}{}{}] {}%'.format(
        '='*done, '>'*arrow, '.'*left, int(round(percentage, 2)*100)))
    if percentage == 1:
        print('')


def smooth(signal, window=10, step=1):
    signal = signal[::step]
    output = []
    bottom = 0
    for top in range(window, len(signal)):
        add = sum(signal[bottom:top])/window
        output.append(add)
        bottom += 1
    return np.array(output)


def smoothsamples(samples, window=SMOOTHING):
    if window == 0:
        return samples
    new_samples = []
    print('Smoothing...')
    for i, sample in enumerate(samples):
        new_samples.append(smooth(sample, window))
        showprogress((i+1)/len(samples))
    new_samples = np.array(new_samples)
    # print("Stuff happen {}\n {}".format(samples, new_samples))
    return new_samples

def genchordsfilename(song_name):
    if song_name.endswith('.wav'):
        song_name = song_name[:-4]
    chords_file = song_name + '.chtr'
    return chords_file

def makechordsfile(chords_file, chords):
    with open(chords_file, 'w') as f:
        for chord in chords:
            f.write(str(chord)+'\n')
    return chords_file

def splitdata(x, freq, y=[]):
    # TODO: assumption: always sampled at 44100hz
    chunk = int(44100*2/freq)*2
    new_x = []
    new_y = []
    for i,d in enumerate(x):
        top = chunk
        while top <= len(d):
            new_x.append(d[top-chunk:top])
            if len(y) > 0: new_y.append(y[i])
            top += int(chunk/2)
    return np.array(new_x), np.array(new_y), chunk

def notefrequency(index):
    return [130.81,138.59,146.83,155.56,164.81,174.61,185,196,207.65,220,233.08,246.94][index]


if __name__ == '__main__':
    pass
