import tkinter as tk
from tkinter import filedialog
import os
import predict
import play
import time

window = tk.Tk()
audio_name = None
audio_label_txt = tk.StringVar()


def init():
    window.title("Music Gen")
    window.geometry('600x400')
    window.resizable(0, 0)

    browse = tk.Button(
        window, text="Load song and generate", command=openfile)
    browse.pack()

    audio_label = tk.Label(window, textvariable=audio_label_txt)
    audio_label.pack()

    # generate = tk.Button(window, text="Generate", command=genandplay)
    # generate.pack()


def openfile():
    audio_name = filedialog.askopenfilename(
        parent=window, initialdir='/', title='Choose audio file')
    audio_name = audio_name.split('/')[-1]
    audio_label_txt.set(audio_name)
    genandplay(audio_name)


def genandplay(name):
    status_txt = tk.StringVar()
    status_label = tk.Label(window, textvariable=status_txt)
    status_label.pack()
    status_txt.set("Generating...")
    time.sleep(1)
    bpm, chords = predict.getchords(name)
    status_txt.set("Music Ready!")
    time.sleep(1)
    play.Play(bpm, chords).start()


if __name__ == '__main__':
    init()
    window.mainloop()
