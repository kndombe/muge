import tensorflow as tf
import util
import wave
import os
import numpy as np
import ast
import random


def getreferences():
    freq = {}
    chords = {}
    with open('notes/frequencies.JSON', 'r') as f:
        freq = ast.literal_eval(''.join(f.readlines()))
        f.close()
    with open('notes/chords.JSON', 'r') as f:
        chords = ast.literal_eval(''.join(f.readlines()))
        f.close()
    return chords, freq


def load():
    root = 'data/chords/'
    folders = [folder for folder in os.listdir(
        root) if os.path.isdir(root+folder)]

    data = []
    for i, folder in enumerate(folders):
        print('Loading folder {}...'.format(folder))
        audios = os.listdir(root+folder)
        for j, audio in enumerate(audios):
            signal = wave.open(root+folder+'/'+audio, 'r')
            signal = np.fromstring(signal.readframes(-1), 'Int16')
            data.append({'folder': folder, 'signal': signal})
    return data


def genpair(data, freq, label):
    freq = int(44100*2/freq)
    i = 0
    pairs = []
    while i+2*freq <= len(data):
        # print(freq)
        sub = np.array(data[i:i+2*freq])
        mid = int(len(sub)/2)
        x = (sub[0:mid], sub[mid:mid*2])
        pair = (np.array(x), label)
        pairs.append(np.array(pair))
        i += 2*freq
    return pairs


def chordnotes(chord_name, signal):
    base = chord_name.split('_')[0]
    chord = chord_name.split('_')[1]
    notes = list(frequencies.keys())
    start = notes.index(base+'2')
    xy = []
    for i in range(1, 12):
        index = i+start
        note = notes[index]
        freq = frequencies[note]
        isPlayed = 1*(i in chords[chord])
        xy += genpair(signal, freq, isPlayed)
    return xy


def extractdata(rawdata, split=.7):
    xy = []
    for i, sample in enumerate(rawdata):
        chord_name = sample['folder']
        signal = sample['signal']
        xy += chordnotes(chord_name, signal)
    divide = int(len(xy)*split)
    random.shuffle(xy)
    train = np.array(xy)[0:divide]
    test = np.array(xy)[divide:]
    x_train = train[:, 0]
    y_train = train[:, 1]
    x_test = test[:, 0]
    y_test = test[:, 1]
    return x_train, y_train, x_test, y_test


chords, frequencies = getreferences()
data = load()
x, y, xt, yt = extractdata(data)
# print(x)
# print(y)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(500, activation='relu', input_shape=(1,)),
    tf.keras.layers.Dense(2, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy',
              metrics=['sparse_categorical_accuracy'])

model.fit(x, y, epochs=2)

# print(chordnotes('D_m9'))

# d = load()
# print(d)
# freq = 44100*2/440

# print(pairs)
# print(getfrequencies())


# x, y, xt, yt = util.load('data/chords/data')
