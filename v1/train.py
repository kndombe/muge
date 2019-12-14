import wave
import numpy as np
import ast
import random
import util
import tensorflow as tf
import matplotlib.pyplot as plt

x, y, xt, yt = util.load('data/data', split=.8)
# print('SURVEY SAYS')
# print(set(y))


model = tf.keras.Sequential([
    tf.keras.layers.Dense(util.CHUNK, activation='relu',
                          input_shape=(util.CHUNK,)),
    tf.keras.layers.Dense(500, activation='relu'),
    # tf.keras.layers.Dropout(0.2),
    # tf.keras.layers.Dense(300, activation='relu'),
    # tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(100, activation='relu'),
    # tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(len(set(y)), activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy',
              metrics=['sparse_categorical_accuracy'])

hist = model.fit(x, y, epochs=2)
model.evaluate(xt, yt, verbose=2)

plt.plot(hist.history['acc'])
plt.plot(hist.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.savefig('train.png')
# plt.show()


model.save('model/model')
