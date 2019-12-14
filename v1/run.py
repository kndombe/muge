import predict
import play


song = 'heal simple.wav'
chords = predict.getchords(song)
chords_file = song[:-4]+'.chtr'
with open(chords_file, 'w') as f:
    for chord in chords:
        f.write(str(chord)+'\n')
play.Play(chords_file, quantize=False).start()
