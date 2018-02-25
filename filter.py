
# standard libraries
import pickle
import sounddevice as sd

# nonstandard libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack

# homegrown libraries

""" Main """

# load data
data = pickle.load(open('data.p','rb'))

N,T = len(data),1.0/44100.0

# data load
data = np.array(data).flatten()

# fft 
data_fft = np.fft.fft(data)
data_fft_mod = [d if 2*abs(i - N/2) < 0.99*N else 0.0 for i,d in enumerate(data_fft)]
data_mod = np.real(np.fft.ifft(data_fft_mod))

x = np.linspace(0.0, N*T, N)
xf = np.linspace(-1.0/(2.0*T), 1.0/(2.0*T), N)

print xf.shape

fig,axes = plt.subplots(4,1)
fig.set_size_inches(18.5, 10.5, forward=True)

axes[0].plot(x,data)
#axes[1].plot(xf,data_fft[:N//2])
#axes[2].plot(xf,data_fft_mod[:N//2])
axes[1].plot(xf,data_fft)
axes[2].plot(xf,data_fft_mod)
axes[3].plot(x,data_mod)

plt.show(block=False)
raw_input('Press enter to close...')
plt.close()


fs = 44100

sd.play(data, fs, blocking=True)
sd.play(data_mod, fs, blocking=True)



