import util
import tensorflow as tf
import ast


def getchords(file):
    precision = 15
    window = 30 * precision
    fs, d = util.getdata(file, precision)
    i2c = {}
    with open('data/i2c', 'r') as f:
        i2c = ast.literal_eval(f.readline())

    print('Loading model...')
    model = tf.keras.models.load_model('model/model')
    print('Predicting chords with model...')
    pred = model.predict(d)
    bottom = 0
    chords = []
    print('Reading chords...')
    for top in range(window, len(pred)):
        part = pred[bottom:top]
        probs = [(i, sum(part[:, i]) / len(part)) for i in range(len(part[0]))]
        probs.sort(key=lambda x: x[1], reverse=True)
        chord_i, prob = probs.pop(0)
        chord = i2c[chord_i]
        chords.append((chord, prob))
        bottom += 1
        util.showprogress((top+1)/len(pred))

    timed_chords = []
    base = (util.CHUNK / 2) / fs
    start_time = 0
    floor = .6
    current_chord = None
    current_prob = 0
    print('Timing chords...')
    for i, chord in enumerate(chords):
        end_time = base*i + (util.CHUNK/44100 * (window + 1) / 2)
        if current_chord == None:
            current_chord, current_prob = chord
        elif (current_chord != chord[0] and end_time-start_time > floor and chord[1] >= 0.0) or i == len(chords)-1:
            timed_chords.append(
                (current_chord, round(start_time/precision, 2), round(end_time/precision, 2), chord[1]))
            current_chord, current_prob = chord
            start_time = end_time
        util.showprogress((i+1)/len(chords))
    # elapse = 0
    # if len(timed_chords) > 1:
    #     elapse = min([abs(timed_chords[i][1] - timed_chords[i][2])
    #                   for i in range(len(timed_chords))])

    # bpm = round(4*60 / elapse, 3)
    # print(bpm)
    # for c in timed_chords:
    #     print(c)
    print("Prediction done!")
    return timed_chords
