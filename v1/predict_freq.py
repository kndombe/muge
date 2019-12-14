import tensorflow as tf
import util
import numpy as np


def averagepred(pred):
    chords = []
    window = 50
    for index in range(window, len(pred[0])):
        note_pred = []
        for i in range(12):
            raw_pred = pred[i]
            # print(np.shape(raw_pred))
            raw_pred = raw_pred[index-window: index]
            # print(raw_pred, index)
            # p = sum(raw_pred[:])/len(raw_pred)
            p = sum(raw_pred[:, 1])/len(raw_pred)
            # p = [sum(raw_pred[:, i])/len(raw_pred)
            #      for i in range(len(raw_pred[0]))]
            # p = [sum(raw_pred[:, 0])/len(raw_pred),
            #      sum(raw_pred[:, 1])/len(raw_pred)]
            note_pred.append(p)
        chords.append(note_pred)
    return np.array(chords)

def samplepred(pred):
    count = int(len(pred)/window)
    sample = []
    for i in range(window):
        bottom = (i-window) * count
        top = count * window
        sample.append(sum(pred[bottom:top, 1]) / count)
    return np.array(sample)

window = 10

chords_array = ['C', 'C#', 'D', 'D#', 'E',
                'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
fs, d = util.getdata('cM.wav')
d = util.smoothsamples(d)
# print(d)
# model = tf.keras.models.load_model('model/model3')
# models = []
pred = np.empty(shape=(12, len(d), 2))
# pred = np.empty(shape=(12, window))
for i in range(12):
    print('Prediciting for note {}'.format(chords_array[i]))
    model = tf.keras.models.load_model('models/model_{}'.format(i))
    # print(np.shape(d))
    pred[i] = model.predict(d)
    # note_pred = model.predict(util.splitdata(d, util.notefrequency(i)))
    # pred[i] = samplepred(note_pred)

# pred = model.predict(d)

print('Prediction!')
pred = averagepred(pred)
print(pred)
# for i, p in enumerate(pred):
#     print('{}'.format(p))
