# import pygame.midi as midi
# import time

# midi.init()
# p = midi.Output(0)
# p.set_instrument(115)
# p.note_on(75, 100)
# time.sleep(1)
# # for i in range(48, 84):
# #     print(i)
# #     p.note_on(i, 90)
# #     time.sleep(0.5)
# #     p.note_off(i, 90)
# # for i in range(30, 115):
# #     print(i)
# #     p.set_instrument(i)
# #     p.note_on(64, 100)
# #     time.sleep(1.2)
# #     p.note_off(64, 100)
# del p

import os
os.system('python play.py "heal simple.chtr"')
