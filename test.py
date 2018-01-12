
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

duration = 5.0 
fs = 44100 
channels = 2

pitch = 440

myarray = np.sin(2*np.pi*pitch*np.arange(int(duration*fs))/fs)


sd.play(myarray)
print 'Starting...'
sd.wait()
print 'Ending.'

