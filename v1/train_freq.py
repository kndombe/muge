import tensorflow as tf
import numpy as np
import util
import ast


# def filtereddata(x, y):
#     new_x = []
#     new_y = []
#     for i, y_p in enumerate(y):
#         chord_name = i2c[y_p]
#         base = chord_name.split('_')[0]
#         chord = chord_name.split('_')[1]
#         notes = list(frequencies.keys())
#         start = notes.index(base+'2')
#         for i in range(1, 12):
#             index = i+start
#             note = notes[index]
#             freq = frequencies[note]
#             isPlayed = 1*(i in chords[chord])
#             new_x.append([(p, freq) for p in x[i]])
#             new_y.append(isPlayed)
#     return np.array(new_x), np.array(new_y)


def getchordarrays(y):
    new_y = []
    print('Getting chord arrays')
    for i, y_p in enumerate(y):
        chord_name = i2c[y_p]
        base = chord_name.split('_')[0]
        chord = chord_name.split('_')[1]
        notes = list(frequencies.keys())
        start = notes.index(base+'2')
        margin = start - notes.index('C2')
        chord_array = [0, ]*12
        for i in range(0, 12):
            index = i+start
            note = notes[index]
            freq = frequencies[note]
            isPlayed = 1*(i in chords[chord])
            chord_array[(i+margin) % 12] = isPlayed
        new_y.append(chord_array)
        util.showprogress((i+1)/len(y))
        # print(chord_name, chord_array)
    return np.array(new_y)


print("Starting training...")
chords = util.getchords()
frequencies = util.getfrequencies()
i2c = {}
with open('data/i2c3', 'r') as f:
    i2c = ast.literal_eval(f.readline())
print('Getting data...')
x, y, xt, yt = util.load('data/data3', split=.8)
x = util.smoothsamples(x, window=util.SMOOTHING)
y = getchordarrays(y)
xt = util.smoothsamples(xt, window=util.SMOOTHING)
yt = getchordarrays(yt)
print("Got data!")


# inputs = tf.keras.Input(shape=(util.CHUNK-util.SMOOTHING,))
# hidden = tf.keras.layers.Dense(50, activation='relu')(inputs)
# # hidden = tf.keras.layers.Dense(1000, activation='relu')(hidden)
# # hidden = tf.keras.layers.Dense(800, activation='relu')(hidden)
# # hidden = tf.keras.layers.Dense(500, activation='relu')(hidden)
# # hidden = tf.keras.layers.Dense(120, activation='relu')(hidden)
# # hidden = tf.keras.layers.Dense(100, activation='relu')(hidden)
# outputs = []
# for i in range(12):
#     outputs.append(tf.keras.layers.Dense(2, activation='softmax')(hidden))
# model = tf.keras.Model(inputs=inputs, outputs=outputs)

# model.compile(optimizer='adam', loss=['sparse_categorical_crossentropy', ]*12,
#               metrics=['accuracy', ]*12)

# # print('HELLO GOVNAR')
# # print(np.shape(y))
# print(np.shape(x))
# model.fit(x, [y[:, i] for i in range(12)], epochs=1)
# model.evaluate(xt, [yt[:, i] for i in range(12)], verbose=2)
# model.save('model/model3')


for i in range(12):
    print('Training model {}'.format(i+1))
    inputs = tf.keras.Input(shape=(util.CHUNK-util.SMOOTHING,))
    hidden = tf.keras.layers.Dense(400, activation='relu')(inputs)
    # hidden = tf.keras.layers.Dense(1000, activation='relu')(hidden)
    # hidden = tf.keras.layers.Dense(500, activation='relu')(hidden)
    hidden = tf.keras.layers.Dense(50, activation='relu')(hidden)
    outputs = tf.keras.layers.Dense(2, activation='softmax')(hidden)
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    model.fit(x, y[:, i], epochs=2)
    model.evaluate(xt, yt[:, i], verbose=2)
    model.save('models/model_{}'.format(i))

# new_x, s = util.splitdata(x, util.notefrequency(0))
# print(np.shape(new_x))
# print(np.shape(x))
# print(s)
# for i in range(12):
#     print('Training model {}'.format(i+1))
#     new_x, new_y, size = util.splitdata(x, util.notefrequency(i), y)
#     new_xt, new_yt, _ = util.splitdata(xt, util.notefrequency(i), yt)
#     inputs = tf.keras.Input(shape=(size,))
#     hidden = tf.keras.layers.Dense(1000, activation='relu')(inputs)
#     hidden = tf.keras.layers.Dense(520, activation='relu')(hidden)
#     hidden = tf.keras.layers.Dense(100, activation='relu')(hidden)
#     outputs = tf.keras.layers.Dense(2, activation='softmax')(hidden)
#     model = tf.keras.Model(inputs=inputs, outputs=outputs)
#     model.compile(optimizer='adam', loss='sparse_categorical_crossentropy',
#                   metrics=['accuracy'])
#     model.fit(new_x, new_y[:, i], epochs=2)
#     model.evaluate(new_xt, new_yt[:, i], verbose=2)
#     model.save('models/model_{}'.format(i))
