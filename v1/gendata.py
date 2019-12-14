import util
import os
import wave
import numpy as np


def savedata(root='data/', data_path='data', raw_folders=['raw/'], c2i_path='c2i', i2c_path='i2c', split=True):
    data = []
    c2i = {}
    i2c = {}
    for raw_folder in raw_folders:
        path = root+raw_folder
        chords = [chord for chord in os.listdir(
            path) if os.path.isdir(path+chord)]
        c2i.update({chord: i for i, chord in enumerate(chords)})
        i2c.update({i: chord for i, chord in enumerate(chords)})
        for chord in chords:
            print('Reading folder {}...'.format(chord))
            chord_data = [audio for audio in os.listdir(
                path+chord) if os.path.isfile(path+chord+'/'+audio) and audio.endswith('.wav')]
            for audio in chord_data:
                signal = wave.open(path+chord+'/'+audio, 'r')
                signal = np.fromstring(signal.readframes(-1), 'Int16')
                if split:
                    # signal = signal[int(len(signal)*0.2):int(len(signal)*8)]
                    bottom = 0
                    # for top in range(util.CHUNK, len(signal)):
                    #     d = {'chord': c2i[chord],
                    #          'signal': list(signal[bottom:top])}
                    #     data.append(d)
                    #     bottom += 1
                    #     print(top, len(signal))
                    #     # util.showprogress(top/len(signal))
                    while True:
                        top = bottom + util.CHUNK
                        if top >= signal.size:
                            break
                        d = {'chord': c2i[chord],
                             'signal': list(signal[bottom:top])}
                        data.append(d)
                        bottom += int(util.CHUNK)
                else:
                    data.append({'chord': c2i[chord], 'signal': list(signal)})
    with open(root+data_path, 'w') as f:
        print('Generating data file with {} samples...'.format(len(data)))
        for i, d in enumerate(data):
            f.write(str(d)+'\n')
            util.showprogress((i+1)/len(data))
        f.close()
    with open(root+i2c_path, 'w') as f:
        print('Writing index_to_chord map file...')
        f.write(str(i2c))
        f.close()
    with open(root+c2i_path, 'w') as f:
        print('Writing chord_to_index map file...')
        f.write(str(c2i))
        f.close()
    print('Done!')


# savedata()
