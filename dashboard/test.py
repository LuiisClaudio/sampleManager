#/Users/luisclaudio/Downloads/testewav.wav
from pygame import mixer
# freq = 44100     # audio CD quality
# bitsize = -16    # unsigned 16 bit
# channels = 2     # 1 is mono, 2 is stereo
# buffer = 2048    # number of samples (experiment to get best sound)
# mixer.init(freq, bitsize, channels, buffer)
mixer.init()
mixer.music.load('/Users/luisclaudio/Downloads/testemp3.mp3')
mixer.music.play()

while mixer.music.get_busy():
    time.Clock().tick(10)