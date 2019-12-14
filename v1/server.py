from fastapi import FastAPI
from typing import List
from play import Play
import predict
import util
import os
import os.path
import subprocess

app = FastAPI()


@app.get('/play/')
def play(song: str, instruments: str = '', recreate: bool = False):
    song += '.wav'
    chords_file = util.genchordsfilename(song)
    if recreate or not os.path.isfile(chords_file):
        chords = predict.getchords(song)
        util.makechordsfile(chords_file, chords)
    else:
        print("Chord file detected for {}, skipping generation".format(song))
    # subprocess.Popen(['python', 'play.py', f'{chords_file}', f'{instruments}'])
    # os.system('python play.py "{}" "{}"'.format(chords_file, instruments))
    Play(chords_file, instruments).start()
    return {'Status': 'Done!'}
