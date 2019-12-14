import wave
import matplotlib.pyplot as plt
import numpy as np

step = 5


def get(path):
    signal = wave.open(path, 'r')
    signal = np.fromstring(signal.readframes(-1), 'Int16')
    return smooth(signal)


def smooth(signal):
    signal = signal[::step]
    window = 10
    output = []
    bottom = 0
    for top in range(window, len(signal)):
        add = sum(signal[bottom:top])/window
        output.append(add)
        bottom += 1
    return np.array(output)


# c5 = get('notes/c5.wav')
# c5p = get('notes/c5p.wav')
# a5v = get('notes/a5v.wav')
# a5p = get('notes/a5p.wav')
# a5pl = get('notes/a5pl.wav')
# a34 = get('notes/a34.wav')
# a3 = get('notes/a3.wav')
a4 = get('notes/a4.wav')
# a4c5 = get('notes/a4c5.wav')
# a4c5e5 = get('notes/a4c5e5.wav')
# ce5 = get('notes/ce5.wav')
# aminor = get('notes/a minor.wav')
# amajor = get('notes/amajor.wav')
# amajorp = get('notes/amajor p.wav')
# aminor2 = get('notes/aminor2.wav')
# a2 = get('notes/a2.wav')
period = 44100*2/abs(440.00)
# print(a4[5:210])
xwind = 1500
plt.plot(a4)
# plt.plot(ce5)
# plt.plot(a5p)
# plt.plot(a5v)
# plt.plot(c5p)
# plt.plot(aminor)
# plt.plot(aminor2)
# plt.plot(amajor)
# plt.plot(amajorp)
# plt.plot(a4)
# plt.plot(c5)
# plt.plot(a4c5)
# plt.plot(a5pl)
# plt.ylim(-2000, 2000)
plt.xlim(0+xwind, period*1/step+xwind)
# plt.show()
plt.savefig('plot.png')
